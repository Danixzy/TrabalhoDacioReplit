from Model import model as md
from View_and_Interface import view as vw
import controler as ctl
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

def main():
  print("Starting Service...\n")

  
  servidor = HTTPServer(("localhost", 8000), vw.BibliotecaView)
  print("Servidor SGBU rodando em http://localhost:8000")
  print("Acesse: http://localhost:8000/livros")
  print("Equipe 2 - CRUD de Livros")
  servidor.serve_forever()

if __name__ == "__main__":
  main()
