"""
[TDD red] Testes de contrato/integridade para o módulo de Livros
Equipe 2 - Biblioteca TecLearn TABAJARA
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.Livro import Livro


class TestLivroContrato:
    """Classe para testes de contrato e integridade do modelo Livro"""

    def test_contrato_livro_possui_todos_campos_obrigatorios(self):
        """
        [TDD red] Teste 1: Verifica se o objeto Livro possui todos os campos obrigatórios
        """
        livro = Livro("Python para Iniciantes", "João Silva", 10, "disponível")
        
        assert hasattr(livro, 'nome'), "Livro deve ter atributo 'nome'"
        assert hasattr(livro, 'autor'), "Livro deve ter atributo 'autor'"
        assert hasattr(livro, 'estoque'), "Livro deve ter atributo 'estoque'"
        assert hasattr(livro, 'status'), "Livro deve ter atributo 'status'"

    def test_contrato_serializacao_para_dict(self):
        """
        [TDD red] Teste 2: Verifica se o Livro pode ser serializado corretamente para dict
        """
        livro = Livro("Clean Code", "Robert Martin", 5, "disponível")
        livro_dict = livro.to_dict()
        
        assert isinstance(livro_dict, dict), "to_dict() deve retornar um dicionário"
        assert "nome" in livro_dict, "Dicionário deve conter 'nome'"
        assert "autor" in livro_dict, "Dicionário deve conter 'autor'"
        assert "estoque" in livro_dict, "Dicionário deve conter 'estoque'"
        assert "status" in livro_dict, "Dicionário deve conter 'status'"
        assert livro_dict["nome"] == "Clean Code"
        assert livro_dict["autor"] == "Robert Martin"
        assert livro_dict["estoque"] == 5
        assert livro_dict["status"] == "disponível"

    def test_contrato_desserializacao_de_dict(self):
        """
        [TDD red] Teste 3: Verifica se o Livro pode ser criado a partir de um dict
        """
        dados = {
            "nome": "Domain-Driven Design",
            "autor": "Eric Evans",
            "estoque": 3,
            "status": "disponível"
        }
        
        livro = Livro.from_dict(dados)
        
        assert livro.get_nome() == "Domain-Driven Design"
        assert livro.get_autor() == "Eric Evans"
        assert livro.get_estoque() == 3
        assert livro.get_status() == "disponível"

    def test_contrato_validacao_campo_nome_obrigatorio(self):
        """
        [TDD red] Teste 4: Verifica se o campo 'nome' é obrigatório
        """
        with pytest.raises(ValueError, match="Nome do livro é obrigatório"):
            Livro("", "Autor Teste", 5, "disponível")
        
        with pytest.raises(ValueError, match="Nome do livro é obrigatório"):
            Livro(None, "Autor Teste", 5, "disponível")

    def test_contrato_validacao_campo_autor_obrigatorio(self):
        """
        [TDD red] Teste 5: Verifica se o campo 'autor' é obrigatório
        """
        with pytest.raises(ValueError, match="Autor do livro é obrigatório"):
            Livro("Livro Teste", "", 5, "disponível")
        
        with pytest.raises(ValueError, match="Autor do livro é obrigatório"):
            Livro("Livro Teste", None, 5, "disponível")
