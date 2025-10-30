from Model import model as md
from Model import User as user

class Controler():
  def __init__(self, loginTru):
   self.loginTrue = loginTru
 
  def Ctr_Adiciona_Despesa(self, despesa_new):
    md.adiocionar_despesa(despesa_new)
    print(md.desepesa[1].get_valor())
    
  def Get_Despesas(self):
    return md.despesas_list

  def Get_Total_Mensal(self, mes):
    return md.clac_total_mensal(mes)

  def Atutenticar(self, login, senha):
    Usuario_Autenticado = user.User(login, senha)
    return Usuario_Autenticado.autenticar()

  def get_Contas_Cadastradas(self):
    return md.bancos_list

  def get_Bancos_List(self):
    list = []  
    for bn in md.bancos:
        list.append (bn.get_bank())
    return list
    
  def Ctr_Adiciona_Categoria(self, categoria):
    md.adiocionar_categoria(categoria)

  def Get_Categorias_Cadastradas(self):
    return md.categorias_list

  def Ctr_Cadastra_Conta(self, bank, ag, cc, tipo):
     dados_inseridos = [bank, ag, cc, tipo]
     md.adiocionar_conta(dados_inseridos)

  # ============================================================================
  # MÉTODOS PARA GERENCIAMENTO DE LIVROS - Equipe 2
  # ============================================================================
  
  def Ctr_Adiciona_Livro(self, livro_dados):
    """Cadastra um novo livro no sistema"""
    try:
      md.adicionar_livro(livro_dados)
      return True, "Livro cadastrado com sucesso"
    except (ValueError, TypeError) as e:
      return False, str(e)
  
  def Ctr_Edita_Livro(self, indice, livro_atualizado):
    """Edita informações de um livro existente"""
    try:
      md.editar_livro(indice, livro_atualizado)
      return True, "Livro editado com sucesso"
    except (ValueError, TypeError, IndexError) as e:
      return False, str(e)
  
  def Ctr_Remove_Livro(self, indice):
    """Remove um livro do sistema"""
    try:
      md.remover_livro(indice)
      return True, "Livro removido com sucesso"
    except (ValueError, IndexError) as e:
      return False, str(e)
  
  def Ctr_Lista_Livros(self, autor=None, status=None):
    """Lista livros com possibilidade de filtros"""
    return md.listar_livros(autor, status)
  
  def Ctr_Filtrar_Livros_Por_Status(self, status):
    """Filtra livros por status"""
    return md.filtrar_livros_por_status(status)
  
  def Ctr_Filtrar_Livros_Por_Autor(self, autor):
    """Filtra livros por autor"""
    return md.filtrar_livros_por_autor(autor)


# @Alunos --> moc de implementação correta para versões futuras;
class Ctrl_User(user.User):
  def __init__(self, login, senha):
    super().__init__(login, senha)

  def autenticar(self):
      return super().autenticar()