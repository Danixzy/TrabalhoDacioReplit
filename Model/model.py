from Model import Despesa as dsp
from Model import Bancario as bn
from Model import Livro as lv
import configparser



# @Alunos --> moc de implementação correta para versões futuras;
bancos = []
bancos.append(bn.Bancario("Banco do Brasil", "0001", "123456-7", "Conta Corrente"))
bancos.append(bn.Bancario("Caixa Econômica Federal", "0002", "654321-8", "Conta Poupança"))
bancos.append(bn.Bancario("Itaú", "0003", "123456-7", "Conta Salário"))

desepesa = []
desepesa.append(dsp.Despesa("01/01/2023", 100.0, "Alimentação", "Supermercado", "Compras", "Cartão de Crédito", "BB"))

class Model(bn.Bancario, dsp.Despesa ):
  def __init__(self, bank, ag, cc, tipo, dat_despesa, valor, cat_despesa, descricao, tag, forma_pgmt, conta):    
    pass

# @Alunos --> moc de implementação correta para versões futuras;

despesas_list = []
bancos_list = [["Banco do Brasil", "0001", "123456-7",], ["Caixa Econômica Federal", "0002", "654321-8",], ["Itaú", "0003", "123456-7",],]
categorias_list = ["Alimentação", "Transporte", "Moradia", "Educação", "Saúde", "Lazer", "Compras online" "Outros"]
config = configparser.ConfigParser()
config.read("user.data", encoding="utf-8")

def adiocionar_despesa(despesa):
  dsp_new = dsp.Despesa(despesa["data"], despesa["valor"], despesa["categoria"], despesa["descricao"], despesa["tag"], despesa["forma_pgmt"], despesa["banco"])
  desepesa.append(dsp_new)

def adiocionar_conta(conta):
    bancos_list.append(conta)

def adiocionar_categoria(categoria):
    categorias_list.append(categoria)

def remover_despesa(despesa):
    despesas_list.remove(despesa)

def clac_total_mensal(competencia):
  total = 0
  for i in range(len(desepesa)):
      data = desepesa[i].get_dat_despesa()
      
  return total

def get_Usuario_data():
  user = config["credenciais"]["user"]
  senha = config["credenciais"]["senha"]
  return user, senha


# ============================================================================
# MÓDULO CRUD DE LIVROS - Biblioteca TecLearn TABAJARA - Equipe 2
# [TDD green] Implementação das funcionalidades de gerenciamento de livros
# ============================================================================

# Lista global para armazenar os livros cadastrados
livros_list = []


def adicionar_livro(livro_dados):
    """
    [TDD green] Cadastra um novo livro no sistema
    
    Args:
        livro_dados (dict): Dicionário com os dados do livro
            - nome (str): Nome do livro
            - autor (str): Autor do livro
            - estoque (int): Quantidade em estoque
            - status (str): Status do livro ('disponível' ou 'emprestado')
    
    Raises:
        ValueError: Se algum campo obrigatório estiver vazio ou inválido
        TypeError: Se o tipo do campo estoque não for inteiro
    """
    # Validação de campos obrigatórios
    if not livro_dados.get("nome") or livro_dados.get("nome") is None:
        raise ValueError("Nome do livro é obrigatório")
    
    if not livro_dados.get("autor") or livro_dados.get("autor") is None:
        raise ValueError("Autor do livro é obrigatório")
    
    # Validação de tipo do estoque
    if not isinstance(livro_dados.get("estoque"), int):
        raise TypeError("Estoque deve ser um número inteiro")
    
    # Validação de estoque negativo
    if livro_dados.get("estoque") < 0:
        raise ValueError("Estoque não pode ser negativo")
    
    # Validação de status
    status_validos = ["disponível", "emprestado"]
    if livro_dados.get("status") not in status_validos:
        raise ValueError("Status deve ser 'disponível' ou 'emprestado'")
    
    # Criar novo livro e adicionar à lista
    novo_livro = lv.Livro(
        nome=livro_dados["nome"],
        autor=livro_dados["autor"],
        estoque=livro_dados["estoque"],
        status=livro_dados["status"]
    )
    livros_list.append(novo_livro)


def editar_livro(indice, livro_atualizado):
    """
    [TDD green] Edita as informações de um livro existente
    
    Args:
        indice (int): Índice do livro na lista
        livro_atualizado (dict): Dicionário com os novos dados do livro
    
    Returns:
        bool: True se o livro foi editado com sucesso
    
    Raises:
        ValueError: Se o livro não for encontrado ou dados forem inválidos
        TypeError: Se o tipo do campo estoque não for inteiro
        IndexError: Se o índice for inválido
    """
    # Verificar se o índice é válido
    if indice < 0 or indice >= len(livros_list):
        raise IndexError("Índice de livro inválido")
    
    livro_encontrado = livros_list[indice]
    
    # Validar os novos dados
    if livro_atualizado.get("estoque") is not None:
        if not isinstance(livro_atualizado["estoque"], int):
            raise TypeError("Estoque deve ser um número inteiro")
        
        if livro_atualizado["estoque"] < 0:
            raise ValueError("Estoque não pode ser negativo")
    
    if livro_atualizado.get("status") is not None:
        status_validos = ["disponível", "emprestado"]
        if livro_atualizado["status"] not in status_validos:
            raise ValueError("Status deve ser 'disponível' ou 'emprestado'")
    
    # Atualizar os campos
    if livro_atualizado.get("nome"):
        livro_encontrado.set_nome(livro_atualizado["nome"])
    
    if livro_atualizado.get("autor"):
        livro_encontrado.set_autor(livro_atualizado["autor"])
    
    if livro_atualizado.get("estoque") is not None:
        livro_encontrado.set_estoque(livro_atualizado["estoque"])
    
    if livro_atualizado.get("status"):
        livro_encontrado.set_status(livro_atualizado["status"])
    
    return True


def remover_livro(indice):
    """
    [TDD green] Remove um livro do sistema
    
    Args:
        indice (int): Índice do livro na lista
    
    Returns:
        bool: True se o livro foi removido com sucesso
    
    Raises:
        ValueError: Se o livro estiver emprestado
        IndexError: Se o índice for inválido
    """
    # Verificar se o índice é válido
    if indice < 0 or indice >= len(livros_list):
        raise IndexError("Índice de livro inválido")
    
    livro_encontrado = livros_list[indice]
    
    # Verificar se o livro está emprestado
    if livro_encontrado.get_status() == "emprestado":
        raise ValueError("Não é possível remover livros emprestados")
    
    # Remover o livro da lista
    livros_list.pop(indice)
    return True


def listar_livros(autor=None, status=None):
    """
    [TDD green] Lista os livros cadastrados com possibilidade de filtros
    
    Args:
        autor (str, optional): Filtrar por autor
        status (str, optional): Filtrar por status ('disponível' ou 'emprestado')
    
    Returns:
        list: Lista de livros que atendem aos critérios de filtro
    """
    # Se não houver filtros, retornar todos os livros
    if autor is None and status is None:
        return livros_list.copy()
    
    # Aplicar filtros
    livros_filtrados = []
    
    for livro in livros_list:
        # Verificar se o livro atende aos critérios
        atende_autor = (autor is None) or (livro.get_autor() == autor)
        atende_status = (status is None) or (livro.get_status() == status)
        
        if atende_autor and atende_status:
            livros_filtrados.append(livro)
    
    return livros_filtrados


def filtrar_livros_por_status(status):
    """
    [TDD green] Filtra livros por status
    
    Args:
        status (str): Status para filtrar ('disponível' ou 'emprestado')
    
    Returns:
        list: Lista de livros com o status especificado
    """
    return listar_livros(status=status)


def filtrar_livros_por_autor(autor):
    """
    [TDD green] Filtra livros por autor
    
    Args:
        autor (str): Nome do autor para filtrar
    
    Returns:
        list: Lista de livros do autor especificado
    """
    return listar_livros(autor=autor)


