from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
import controler as ctl


def _esc(v):
    """Escapa valores HTML para evitar XSS"""
    return escape("" if v is None else str(v))


comTrole = ctl.Controler(True)


class BibliotecaView(BaseHTTPRequestHandler):
    """
    Servidor HTTP que controla todas as telas do SGBU via Python.
    Equipe 2 - CRUD de Livros
    """

    def do_GET(self):
        """Trata requisicoes GET - exibe paginas"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Redireciona raiz para livros
        if path == '/' or path == '/livros':
            self.render_livros()
        
        # Formulário de novo livro
        elif path == '/livros/novo':
            self.render_form_livro()
        
        # Editar livro
        elif path.startswith('/livros/editar'):
            params = parse_qs(parsed_path.query)
            indice = int(params.get("indice", ["0"])[0])
            self.render_form_editar_livro(indice)
        
        # Remover livro
        elif path.startswith('/livros/remover'):
            params = parse_qs(parsed_path.query)
            indice = int(params.get("indice", ["0"])[0])
            self.remover_livro(indice)
        
        else:
            self.send_error(404, "Pagina nao encontrada")

    def do_POST(self):
        """Trata requisicoes POST - processa formularios"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(body)
        
        # Converte para dict simples
        data = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
        
        if path == '/livros/salvar':
            self.processar_livro(data)
        elif path == '/livros/editar':
            self.processar_edicao_livro(data)
        else:
            self.send_error(404)
    
    # ========== RENDERIZACAO - MODULO LIVROS (EQUIPE 2) ==========
    
    def render_livros(self):
        """Renderiza pagina de catalogo de livros com listagem"""
        with open("View_and_Interface/listar_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # Buscar livros via controler
        livros = comTrole.Ctr_Lista_Livros()
        
        # Gerar linhas da tabela
        linhas_html = ""
        if livros:
            for i, livro in enumerate(livros):
                status_badge = "✅ Disponível" if livro.get_status() == "disponível" else "📕 Emprestado"
                linhas_html += f"""
                <tr>
                    <td>{i+1}</td>
                    <td>{_esc(livro.get_nome())}</td>
                    <td>{_esc(livro.get_autor())}</td>
                    <td>{livro.get_estoque()}</td>
                    <td>{status_badge}</td>
                    <td>
                        <a href="/livros/editar?indice={i}" class="btn-edit">Editar</a>
                        <a href="/livros/remover?indice={i}" class="btn-delete" onclick="return confirm('Deseja remover o livro {_esc(livro.get_nome())}?')">Remover</a>
                    </td>
                </tr>
                """
        
        # Substituir placeholders no HTML
        html = html.replace("<!--LIVROS-->", linhas_html)
        html = html.replace("<!--TOTAL-->", str(len(livros)))
        
        self.send_html(html)
    
    def render_form_livro(self):
        """Renderiza formulario de cadastro de livro"""
        with open("View_and_Interface/cadastrar_livro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        self.send_html(html)
    
    def render_form_editar_livro(self, indice):
        """Renderiza formulario de edicao de livro"""
        with open("View_and_Interface/editar_livro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        livros = comTrole.Ctr_Lista_Livros()
        
        if indice < len(livros):
            livro = livros[indice]
            
            # Substituir os placeholders no HTML
            html = html.replace("<!--INDICE-->", str(indice))
            html = html.replace("<!--NOME-->", _esc(livro.get_nome()))
            html = html.replace("<!--AUTOR-->", _esc(livro.get_autor()))
            html = html.replace("<!--ESTOQUE-->", str(livro.get_estoque()))
            html = html.replace("<!--STATUS-->", _esc(livro.get_status()))
            
            self.send_html(html)
        else:
            html = '''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Erro</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                    .message { background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
                    h2 { color: #e74c3c; }
                    a { display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="message">
                    <h3>Livro não encontrado</h3>
                    <a href="/livros">Voltar para catálogo</a>
                </div>
            </body>
            </html>
            '''
            self.send_html(html)
    
    def processar_livro(self, data):
        """Processa formulario de livro e salva via controler"""
        livro_dados = {
            "nome": data.get('nome', ''),
            "autor": data.get('autor', ''),
            "estoque": int(data.get('estoque', 0)),
            "status": data.get('status', '')
        }
        
        sucesso, mensagem = comTrole.Ctr_Adiciona_Livro(livro_dados)
        
        if sucesso:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="2;url=/livros">
                <title>Sucesso</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #27ae60; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>✅ Livro cadastrado com sucesso!</h2>
                    <p><strong>Título:</strong> {_esc(data.get('nome'))}</p>
                    <p><strong>Autor:</strong> {_esc(data.get('autor'))}</p>
                    <p><strong>Estoque:</strong> {data.get('estoque')}</p>
                    <p><strong>Status:</strong> {_esc(data.get('status'))}</p>
                    <p>Redirecionando em 2 segundos...</p>
                    <a href="/livros">Ver Catálogo Agora</a>
                </div>
            </body>
            </html>
            '''
        else:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Erro</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #e74c3c; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>❌ Erro ao cadastrar livro</h2>
                    <p>{_esc(mensagem)}</p>
                    <a href="/livros/novo">Tentar Novamente</a>
                    <a href="/livros">Voltar</a>
                </div>
            </body>
            </html>
            '''
        
        self.send_html(html)
    
    def processar_edicao_livro(self, data):
        """Processa edicao de livro"""
        indice = int(data.get('indice', 0))
        livro_atualizado = {
            "nome": data.get('nome', ''),
            "autor": data.get('autor', ''),
            "estoque": int(data.get('estoque', 0)),
            "status": data.get('status', '')
        }
        
        sucesso, mensagem = comTrole.Ctr_Edita_Livro(indice, livro_atualizado)
        
        if sucesso:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="2;url=/livros">
                <title>Sucesso</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #3498db; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>✅ Livro atualizado com sucesso!</h2>
                    <p>Redirecionando em 2 segundos...</p>
                    <a href="/livros">Ver Catálogo Agora</a>
                </div>
            </body>
            </html>
            '''
        else:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Erro</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #e74c3c; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>❌ Erro ao atualizar livro</h2>
                    <p>{_esc(mensagem)}</p>
                    <a href="/livros">Voltar</a>
                </div>
            </body>
            </html>
            '''
        
        self.send_html(html)
    
    def remover_livro(self, indice):
        """Remove um livro do catalogo"""
        sucesso, mensagem = comTrole.Ctr_Remove_Livro(indice)
        
        if sucesso:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="2;url=/livros">
                <title>Sucesso</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #27ae60; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>✅ {_esc(mensagem)}</h2>
                    <p>Redirecionando em 2 segundos...</p>
                    <a href="/livros">Ver Catálogo Agora</a>
                </div>
            </body>
            </html>
            '''
        else:
            html = f'''
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Erro</title>
                <style>
                    body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .message {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
                    h2 {{ color: #e74c3c; }}
                    a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="message">
                    <h2>❌ Erro ao remover livro</h2>
                    <p>{_esc(mensagem)}</p>
                    <a href="/livros">Voltar</a>
                </div>
            </body>
            </html>
            '''
        
        self.send_html(html)
    
    # ========== METODOS AUXILIARES ==========
    
    def send_html(self, html):
        """Envia resposta HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Log das requisicoes HTTP"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Inicia o servidor HTTP na porta especificada"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibliotecaView)
    print(f"Servidor SGBU iniciado em http://localhost:{port}")
    print(f"Acesse: http://localhost:{port}/livros")
    print(f"Pressione Ctrl+C para encerrar")
    print()
    print("Equipe 2 - CRUD de Livros implementado com TDD")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
