import time
import json
import threading
import random
import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    # Evitar o cache para que o JSON atualize sempre
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f" Servidor Aberto! Acesse http://localhost:{PORT}")
        httpd.serve_forever()

def simulate_vqe():
    """
    Simula uma descida de gradiente do VQE (Energia = -5.609 é o Ground State ideal).
    """
    DATA_FILE = os.path.join(DIRECTORY, "live_data.json")
    
    # Energia inicial (chute aleatório vs proporção áurea)
    energy_std = -1.0 + random.uniform(-0.5, 0.5)
    energy_hi = -3.5 + random.uniform(-0.1, 0.1) 
    
    target_energy = -5.609
    
    data = {
        "status": "rodando",
        "epochs": [],
        "std_vqe": [],
        "hivqe": []
    }
    
    # Resetando os dados antes de comecar nova simulacao
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    
    print("\n Iniciando otimização do Ansatz (VQE)...")
    
    for epoch in range(1, 51): # 50 Epochs igual ao seu benchmark IBM
        if 15 < epoch < 25:
            # Preso num platô estéril
            energy_std -= random.uniform(0.001, 0.01)
        else:
            energy_std -= random.uniform(0.05, 0.2)
        
        # HiVQE
        step_hi = abs(target_energy - energy_hi) * 0.25 
        energy_hi -= step_hi + random.uniform(0.01, 0.05)
        
        if energy_std < target_energy: energy_std = target_energy + random.uniform(-0.01, 0.01)
        if energy_hi < target_energy:  energy_hi  = target_energy + random.uniform(-0.005, 0.005)
        
        data["epochs"].append(epoch)
        data["std_vqe"].append(round(energy_std, 4))
        data["hivqe"].append(round(energy_hi, 4))
        
        if epoch == 50:
            data["status"] = "concluido"
            
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
            
        time.sleep(0.4) 
        
    print(" Otimização concluída!")

if __name__ == "__main__":
    with open(os.path.join(DIRECTORY, "live_data.json"), "w") as f:
        json.dump({"status": "aguardando", "epochs": [], "std_vqe": [], "hivqe": []}, f)
        
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    
    # Executa a simulacao em looping, recomecando 8 segundos apos terminar
    while True:
        simulate_vqe()
        for i in range(8, 0, -1):
            print(f"Reiniciando a simulacao em {i} segundos...")
            time.sleep(1)
