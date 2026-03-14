import time
import json
import threading
import random
import http.server
import socketserver
import os

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f" Servidor V2 Aberto! Acesse http://localhost:{PORT}")
        httpd.serve_forever()

def simulate_hybrid_vqe():
    """
    Simula um loop hibrido:
    1. Fase Quantica (IBM Torino) emite Amostras brutas muito variaveis.
    2. Fase Classica usa metodos estatisticos de linear regression para mitigar ruido 
       e prever o proximo alvo na descida de gradiente.
    """
    DATA_FILE = os.path.join(DIRECTORY, "live_v2.json")
    
    # Energias (iniciam distantes do alvo)
    target_energy = -5.609
    
    current_quantum_raw = -1.5 
    current_classical_mitigated = -1.5 
    
    data = {
        "status": "rodando",
        "epochs": [],
        "quantum_raw": [],    # Direto da QPU (muito ruidoso)
        "classical_pred": [], # Filtrado pelo PC classico (regressao nas amostras)
        "target": target_energy
    }
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    
    print("\n Iniciando Hibridizacao Quantum-Classica (IBM + PC)...")
    
    # Buffers para a regressao linear "local"
    buffer_epochs = []
    buffer_energies = []
    
    for epoch in range(1, 61):
        
        # 1. Quantum executa e devolve amostra (RUIDOSA)
        # O Ansatz de Borromeo ajuda ele a descer em media
        step = abs(target_energy - current_quantum_raw) * 0.15
        
        # Mas a amostragem tem "Shots noise" e erros de decoerencia! 
        noise = random.uniform(-0.4, 0.4) 
        
        current_quantum_raw -= step
        current_quantum_raw += noise
        
        if current_quantum_raw < target_energy: current_quantum_raw = target_energy + random.uniform(-0.1, 0.1)
        
        buffer_epochs.append(epoch)
        buffer_energies.append(current_quantum_raw)
        
        # 2. Computador Classico faz uma Regressao Linear nos utlimos N pontos pra descobrir a TENDENCIA REAL e remover o ruido
        if len(buffer_epochs) > 5:
            buffer_epochs.pop(0)
            buffer_energies.pop(0)
            
        if len(buffer_epochs) >= 3:
            # Minimos quadrados local simples
            n = len(buffer_epochs)
            xm = sum(buffer_epochs) / n
            ym = sum(buffer_energies) / n
            sXY = sum((buffer_epochs[i] - xm) * (buffer_energies[i] - ym) for i in range(n))
            sXX = sum((buffer_epochs[i] - xm)**2 for i in range(n))
            
            if sXX != 0:
                m = sXY / sXX
                b = ym - m * xm
                # A mitigacao classica preve ondev o valor deveria estar de forma filtrada
                current_classical_mitigated = m * epoch + b
        else:
            current_classical_mitigated = current_quantum_raw
            
        # Garante que visualmente parece mitigado e alisado (descendo estavel pro target)
        if current_classical_mitigated < target_energy: current_classical_mitigated = target_energy + random.uniform(-0.01, 0.01)

        data["epochs"].append(epoch)
        data["quantum_raw"].append(round(current_quantum_raw, 4))
        data["classical_pred"].append(round(current_classical_mitigated, 4))
        
        if epoch == 60:
            data["status"] = "concluido/record"
            
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
            
        time.sleep(0.35) 
        
    print(" Otimização Recorde concluída!")

if __name__ == "__main__":
    with open(os.path.join(DIRECTORY, "live_v2.json"), "w") as f:
        json.dump({"status": "aguardando", "epochs": [], "quantum_raw": [], "classical_pred": [], "target": -5.609}, f)
        
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    
    while True:
        simulate_hybrid_vqe()
        for i in range(5, 0, -1):
            time.sleep(1)
