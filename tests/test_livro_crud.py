"""
[TDD red] Testes unitários CRUD para o módulo de Livros
Equipe 2 - Biblioteca TecLearn TABAJARA
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model import model as md
from Model.Livro import Livro


class TestLivroCRUD:
    """Classe para testes unitários de CRUD de Livros"""

    def setup_method(self):
        """Limpa a lista de livros antes de cada teste"""
        md.livros_list.clear()

    def test_cadastrar_livro_com_sucesso(self):
        """
        [TDD red] Teste 1: Cadastrar um livro com todos os dados válidos
        """
        livro_dados = {
            "nome": "Clean Code",
            "autor": "Robert Martin",
            "estoque": 5,
            "status": "disponível"
        }
        
        md.adicionar_livro(livro_dados)
        
        assert len(md.livros_list) == 1
        assert md.livros_list[0].get_nome() == "Clean Code"
        assert md.livros_list[0].get_autor() == "Robert Martin"
        assert md.livros_list[0].get_estoque() == 5
        assert md.livros_list[0].get_status() == "disponível"

    def test_cadastrar_livro_sem_nome(self):
        """
        [TDD red] Teste 2: Tentar cadastrar um livro sem nome deve gerar erro
        """
        livro_dados = {
            "nome": "",
            "autor": "Autor Teste",
            "estoque": 3,
            "status": "disponível"
        }
        
        with pytest.raises(ValueError, match="Nome do livro é obrigatório"):
            md.adicionar_livro(livro_dados)
        
        assert len(md.livros_list) == 0

    def test_cadastrar_livro_sem_autor(self):
        """
        [TDD red] Teste 3: Tentar cadastrar um livro sem autor deve gerar erro
        """
        livro_dados = {
            "nome": "Livro Teste",
            "autor": "",
            "estoque": 3,
            "status": "disponível"
        }
        
        with pytest.raises(ValueError, match="Autor do livro é obrigatório"):
            md.adicionar_livro(livro_dados)
        
        assert len(md.livros_list) == 0

    def test_cadastrar_livro_com_estoque_negativo(self):
        """
        [TDD red] Teste 4: Tentar cadastrar um livro com estoque negativo deve gerar erro
        """
        livro_dados = {
            "nome": "Livro Teste",
            "autor": "Autor Teste",
            "estoque": -1,
            "status": "disponível"
        }
        
        with pytest.raises(ValueError, match="Estoque não pode ser negativo"):
            md.adicionar_livro(livro_dados)
        
        assert len(md.livros_list) == 0

    def test_cadastrar_livro_com_estoque_tipo_invalido(self):
        """
        [TDD red] Teste 5: Tentar cadastrar um livro com estoque não inteiro deve gerar erro
        """
        livro_dados = {
            "nome": "Livro Teste",
            "autor": "Autor Teste",
            "estoque": "cinco",
            "status": "disponível"
        }
        
        with pytest.raises(TypeError, match="Estoque deve ser um número inteiro"):
            md.adicionar_livro(livro_dados)
        
        assert len(md.livros_list) == 0

    def test_editar_livro_com_sucesso(self):
        """
        [TDD red] Teste 6: Editar um livro existente com sucesso
        """
        # Cadastrar um livro primeiro
        livro_dados = {
            "nome": "Python Básico",
            "autor": "João Silva",
            "estoque": 10,
            "status": "disponível"
        }
        md.adicionar_livro(livro_dados)
        
        # Editar o livro
        livro_editado = {
            "nome": "Python Avançado",
            "autor": "João Silva Jr.",
            "estoque": 15,
            "status": "disponível"
        }
        md.editar_livro(0, livro_editado)
        
        assert md.livros_list[0].get_nome() == "Python Avançado"
        assert md.livros_list[0].get_autor() == "João Silva Jr."
        assert md.livros_list[0].get_estoque() == 15

    def test_remover_livro_disponivel_com_sucesso(self):
        """
        [TDD red] Teste 7: Remover um livro que está disponível
        """
        # Cadastrar um livro
        livro_dados = {
            "nome": "Livro para Remover",
            "autor": "Autor Teste",
            "estoque": 5,
            "status": "disponível"
        }
        md.adicionar_livro(livro_dados)
        assert len(md.livros_list) == 1
        
        # Remover o livro
        md.remover_livro(0)
        
        assert len(md.livros_list) == 0

    def test_remover_livro_emprestado_deve_falhar(self):
        """
        [TDD red] Teste 8: Tentar remover um livro emprestado deve gerar erro
        """
        # Cadastrar um livro emprestado
        livro_dados = {
            "nome": "Livro Emprestado",
            "autor": "Autor Teste",
            "estoque": 0,
            "status": "emprestado"
        }
        md.adicionar_livro(livro_dados)
        
        # Tentar remover
        with pytest.raises(ValueError, match="Não é possível remover livros emprestados"):
            md.remover_livro(0)
        
        assert len(md.livros_list) == 1

    def test_listar_todos_livros(self):
        """
        [TDD red] Teste 9: Listar todos os livros cadastrados
        """
        # Cadastrar múltiplos livros
        livros = [
            {"nome": "Livro 1", "autor": "Autor 1", "estoque": 5, "status": "disponível"},
            {"nome": "Livro 2", "autor": "Autor 2", "estoque": 3, "status": "emprestado"},
            {"nome": "Livro 3", "autor": "Autor 3", "estoque": 10, "status": "disponível"},
        ]
        
        for livro in livros:
            md.adicionar_livro(livro)
        
        lista = md.listar_livros()
        
        assert len(lista) == 3
        assert lista[0].get_nome() == "Livro 1"
        assert lista[1].get_nome() == "Livro 2"
        assert lista[2].get_nome() == "Livro 3"

    def test_filtrar_livros_por_status(self):
        """
        [TDD red] Teste 10: Filtrar livros por status (disponível/emprestado)
        """
        # Cadastrar livros com diferentes status
        livros = [
            {"nome": "Livro Disponível 1", "autor": "Autor 1", "estoque": 5, "status": "disponível"},
            {"nome": "Livro Emprestado 1", "autor": "Autor 2", "estoque": 0, "status": "emprestado"},
            {"nome": "Livro Disponível 2", "autor": "Autor 3", "estoque": 3, "status": "disponível"},
            {"nome": "Livro Emprestado 2", "autor": "Autor 4", "estoque": 0, "status": "emprestado"},
        ]
        
        for livro in livros:
            md.adicionar_livro(livro)
        
        # Filtrar por disponíveis
        disponiveis = md.filtrar_livros_por_status("disponível")
        assert len(disponiveis) == 2
        assert all(livro.get_status() == "disponível" for livro in disponiveis)
        
        # Filtrar por emprestados
        emprestados = md.filtrar_livros_por_status("emprestado")
        assert len(emprestados) == 2
        assert all(livro.get_status() == "emprestado" for livro in emprestados)
