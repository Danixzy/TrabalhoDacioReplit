from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from Model.Despesa import Despesa
import controler as ctl
from html import escape


def _esc(v):
    return escape("" if v is None else str(v))


comTrole = ctl.Controler(True)
itens_list = comTrole.Get_Despesas()
bancos = comTrole.get_Bancos_List()


class DespesaController(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        elif self.path == "/menu":
            with open("View_and_Interface/menu.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/cadastrar_despesa":
            with open("View_and_Interface/visao.html", "r",
                      encoding="utf-8") as f:
                conteudo = f.read()

            opcoes = ""
            for banco in bancos:
                opcoes += f"<option value='{banco}'>{banco}</option>"

            conteudo = conteudo.replace("<!--BANCOS-->", opcoes)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        # ============================================================================
        # ROTAS GET PARA LIVROS - Equipe 2
        # ============================================================================
        
        elif self.path == "/menu_livros":
            # Menu principal de livros
            livros = comTrole.Ctr_Lista_Livros()
            disponiveis = comTrole.Ctr_Filtrar_Livros_Por_Status("disponível")
            emprestados = comTrole.Ctr_Filtrar_Livros_Por_Status("emprestado")
            
            with open("View_and_Interface/menu_livros.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            
            conteudo = conteudo.replace("<!--TOTAL_LIVROS-->", str(len(livros)))
            conteudo = conteudo.replace("<!--DISPONIVEIS-->", str(len(disponiveis)))
            conteudo = conteudo.replace("<!--EMPRESTADOS-->", str(len(emprestados)))
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))
        
        elif self.path == "/cadastrar_livro":
            # Formulário de cadastro de livro
            with open("View_and_Interface/cadastrar_livro.html", "rb") as f:
                conteudo = f.read()
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)
        
        elif self.path.startswith("/listar_livros"):
            # Listagem de livros com filtros
            from urllib.parse import urlparse, parse_qs as parse_query_string
            parsed = urlparse(self.path)
            params = parse_query_string(parsed.query)
            
            status = params.get("status", [None])[0]
            autor = params.get("autor", [None])[0]
            
            livros = comTrole.Ctr_Lista_Livros(autor, status)
            
            with open("View_and_Interface/listar_livros.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            
            # Gerar linhas da tabela
            if livros:
                linhas_html = ""
                for i, livro in enumerate(livros):
                    status_class = "status-disponivel" if livro.get_status() == "disponível" else "status-emprestado"
                    linhas_html += f"""
                    <tr>
                        <td>{i+1}</td>
                        <td>{_esc(livro.get_nome())}</td>
                        <td>{_esc(livro.get_autor())}</td>
                        <td>{livro.get_estoque()}</td>
                        <td><span class="status-badge {status_class}">{_esc(livro.get_status())}</span></td>
                        <td class="actions">
                            <a href="/editar_livro?indice={i}" class="btn-edit">✏️ Editar</a>
                            <button onclick="confirmarRemocao({i}, '{_esc(livro.get_nome())}')" class="btn-delete">🗑️ Remover</button>
                        </td>
                    </tr>
                    """
                conteudo = conteudo.replace("<!--LIVROS-->", linhas_html)
            else:
                conteudo = conteudo.replace("<!--LIVROS-->", "")
                conteudo = conteudo.replace('id="empty-state" class="empty-state" style="display: none;"', 
                                           'id="empty-state" class="empty-state"')
            
            # Lista de autores únicos para filtro
            todos_livros = comTrole.Ctr_Lista_Livros()
            autores = sorted(set(livro.get_autor() for livro in todos_livros))
            opcoes_autores = ""
            for a in autores:
                opcoes_autores += f'<option value="{_esc(a)}">{_esc(a)}</option>'
            conteudo = conteudo.replace("<!--AUTORES-->", opcoes_autores)
            
            # Total de livros
            conteudo = conteudo.replace("<!--TOTAL-->", str(len(livros)))
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))
        
        elif self.path.startswith("/editar_livro?"):
            # Formulário de edição de livro
            from urllib.parse import urlparse, parse_qs as parse_query_string
            parsed = urlparse(self.path)
            params = parse_query_string(parsed.query)
            
            indice = int(params.get("indice", ["0"])[0])
            livros = comTrole.Ctr_Lista_Livros()
            
            if indice < len(livros):
                livro = livros[indice]
                
                with open("View_and_Interface/editar_livro.html", "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                conteudo = conteudo.replace("<!--INDICE-->", str(indice))
                conteudo = conteudo.replace("<!--NOME-->", _esc(livro.get_nome()))
                conteudo = conteudo.replace("<!--AUTOR-->", _esc(livro.get_autor()))
                conteudo = conteudo.replace("<!--ESTOQUE-->", str(livro.get_estoque()))
                conteudo = conteudo.replace("<!--STATUS-->", _esc(livro.get_status()))
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>Livro nao encontrado</h1><a href='/listar_livros'>Voltar</a>")
        
        elif self.path.startswith("/remover_livro?"):
            # Remover livro
            from urllib.parse import urlparse, parse_qs as parse_query_string
            parsed = urlparse(self.path)
            params = parse_query_string(parsed.query)
            
            indice = int(params.get("indice", ["0"])[0])
            sucesso, mensagem = comTrole.Ctr_Remove_Livro(indice)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            if sucesso:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .success {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #27ae60; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="success">
                        <h2>✅ {mensagem}</h2>
                        <a href="/listar_livros">Ver Livros</a>
                        <a href="/menu_livros">Menu Livros</a>
                    </div>
                </body>
                </html>
                """
            else:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .error {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #e74c3c; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="error">
                        <h2>❌ Erro ao remover livro</h2>
                        <p>{mensagem}</p>
                        <a href="/listar_livros">Voltar</a>
                    </div>
                </body>
                </html>
                """
            
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/listar_despesas":
            resposta = ""
            for i, d in enumerate(itens_list, start=1):
                valor_fmt = f"R$ {d.get('valor', 0):.2f}".replace('.', ',')
                descricao = _esc(d.get("descricao", ""))
                resposta += ('<a href="/detalhe_despesa?id={i}" class="item">'
                             '<span class="valor">{valor_fmt}</span>'
                             '<span class="descricao">{descricao}</span>'
                             '</a>')
            with open("View_and_Interface/visao_despesa.html",
                      "r",
                      encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--itens-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_conta":
            with open("View_and_Interface/cadastrar_banco.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

    def do_POST(self):
        if self.path == "/cadastrar":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            despesa = {
                "data": params.get("dat_despesa", [""])[0],
                "valor": float(params.get("valor", [0])[0]),
                "categoria": params.get("cat_despesa", [""])[0],
                "descricao": params.get("descricao", [""])[0],
                "tag": params.get("tag", [""])[0],
                "forma_pgmt": params.get("forma_pgmt", [""])[0],
                "banco": params.get("banco", [""])[0]
            }

            comTrole.Ctr_Adiciona_Despesa(despesa)
            item_formatado = (
                f"<p><span class='label'>Data:</span> {_esc(despesa.get('data'))}</p>"
                f"<p><span class='label'>Valor:</span> {_esc(despesa.get('valor'))}</p>"
                f"<p><span class='label'>Categoria:</span> {_esc(despesa.get('categoria'))}</p>"
                f"<p><span class='label'>Descrição:</span> {_esc(despesa.get('descricao'))}</p>"
                f"<p><span class='label'>Tag:</span> {_esc(despesa.get('tag'))}</p>"
                f"<p><span class='label'>Forma de Pagamento:</span> {_esc(despesa.get('forma_pgmt'))}</p>"
                f"<p><span class='label'>Banco:</span> {_esc(despesa.get('banco'))}</p>"
            )
            with open("View_and_Interface/visao_cadastrada.html",
                      "r",
                      encoding="utf-8") as f:
                conteudo = f.read()

            conteudo = conteudo.replace("<!--DADO-->", item_formatado)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/calcular_total":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)
            mes = params.get("mes", [""])[0]

            total = comTrole.Get_Total_Mensal(mes)
            resposta = f"""
            <h1>Total do mês {mes}: R$ {total:.2f}</h1>
            <a href="/">Voltar ao Menu</a>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/login":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            user = params.get("user", [""])[0]
            senha = params.get("senha", [""])[0]

            if comTrole.Atutenticar(user, senha):
                # Login OK → manda para menu
                self.send_response(302)
                self.send_header("Location", "/menu")
                self.end_headers()
            else:
                # Login falhou → recarrega tela com erro
                with open("View_and_Interface/login.html",
                          "r",
                          encoding="utf-8") as f:
                    conteudo = f.read()
                conteudo = conteudo.replace(
                    "<!--MENSAGEM_ERRO-->",
                    "<p class='erro'>Usuário ou senha incorretos.</p>")
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_conta":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = dict(x.split("=") for x in post_data.split("&"))

            bank = params.get("bank", "")
            ag = params.get("ag", "")
            cc = params.get("cc", "")
            tipo = params.get("tipo", "")

            vet_dados = [bank, ag, cc, tipo]

            bancos.append(vet_dados)
            comTrole.Ctr_Cadastra_Conta(bank, ag, cc, tipo)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h3>Conta bancaria cadastrada com sucesso!</h3>")
            self.wfile.write(b'<a href="/menu">Voltar ao menu</a>')

        # ============================================================================
        # ROTAS PARA GERENCIAMENTO DE LIVROS - Equipe 2
        # ============================================================================
        
        elif self.path == "/cadastrar_livro":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)

            livro_dados = {
                "nome": params.get("nome", [""])[0],
                "autor": params.get("autor", [""])[0],
                "estoque": int(params.get("estoque", ["0"])[0]),
                "status": params.get("status", [""])[0]
            }

            sucesso, mensagem = comTrole.Ctr_Adiciona_Livro(livro_dados)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            if sucesso:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .success {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #27ae60; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="success">
                        <h2>✅ Livro cadastrado com sucesso!</h2>
                        <p>{mensagem}</p>
                        <a href="/listar_livros">Ver Livros</a>
                        <a href="/menu_livros">Menu Livros</a>
                    </div>
                </body>
                </html>
                """
            else:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .error {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #e74c3c; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="error">
                        <h2>❌ Erro ao cadastrar livro</h2>
                        <p>{mensagem}</p>
                        <a href="/cadastrar_livro">Tentar Novamente</a>
                        <a href="/menu_livros">Menu Livros</a>
                    </div>
                </body>
                </html>
                """
            
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/editar_livro":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)

            indice = int(params.get("indice", ["0"])[0])
            livro_atualizado = {
                "nome": params.get("nome", [""])[0],
                "autor": params.get("autor", [""])[0],
                "estoque": int(params.get("estoque", ["0"])[0]),
                "status": params.get("status", [""])[0]
            }

            sucesso, mensagem = comTrole.Ctr_Edita_Livro(indice, livro_atualizado)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            if sucesso:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .success {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #3498db; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="success">
                        <h2>✅ Livro atualizado com sucesso!</h2>
                        <p>{mensagem}</p>
                        <a href="/listar_livros">Ver Livros</a>
                        <a href="/menu_livros">Menu Livros</a>
                    </div>
                </body>
                </html>
                """
            else:
                resposta = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial; background: #f0f0f0; padding: 40px; text-align: center; }}
                        .error {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        h2 {{ color: #e74c3c; }}
                        a {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
                        a:hover {{ background: #5568d3; }}
                    </style>
                </head>
                <body>
                    <div class="error">
                        <h2>❌ Erro ao atualizar livro</h2>
                        <p>{mensagem}</p>
                        <a href="/listar_livros">Voltar</a>
                    </div>
                </body>
                </html>
                """
            
            self.wfile.write(resposta.encode("utf-8"))
