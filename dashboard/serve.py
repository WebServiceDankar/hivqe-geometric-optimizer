"""
Servidor HTTP local para o Dashboard de Telemetria.

Responsabilidade:
  - Servir os arquivos estáticos do dashboard (HTML/CSS/JS).
  - Servir o live_data.json com headers anti-cache.

Referência: CLAUDE.MD → seção "dashboard/serve.py"
"""
import http.server
import socketserver
import os


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP que desativa cache para garantir dados frescos."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


def create_server(port, directory):
    """
    Cria um servidor HTTP local.

    Args:
        port: Porta TCP (use 0 para auto-selecionar).
        directory: Diretório raiz para servir arquivos.

    Returns:
        Instância de TCPServer (não-iniciada, chamar .serve_forever()).
    """

    class Handler(NoCacheHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("", port), Handler)
    return server


def main():
    """Entrypoint: serve da raiz do projeto para acessar /dashboard/ e /results/."""
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(dashboard_dir)
    port = 8081

    server = create_server(port=port, directory=project_root)
    print(f"Dashboard: http://localhost:{port}/dashboard/index.html")
    print(f"Servindo de: {project_root}")
    print("Ctrl+C para parar.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.shutdown()


if __name__ == "__main__":
    main()
