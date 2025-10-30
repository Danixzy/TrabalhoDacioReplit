"""
[TDD green] Classe Livro para o sistema de controle da biblioteca
Equipe 2 - Biblioteca TecLearn TABAJARA
"""


class Livro:
    """
    Classe que representa um livro no sistema da biblioteca
    
    Attributes:
        nome (str): Nome do livro
        autor (str): Autor do livro
        estoque (int): Quantidade em estoque
        status (str): Status do livro ('disponível' ou 'emprestado')
    """
    
    def __init__(self, nome, autor, estoque, status):
        """
        Inicializa um objeto Livro com validações
        
        Args:
            nome (str): Nome do livro
            autor (str): Autor do livro
            estoque (int): Quantidade em estoque
            status (str): Status do livro ('disponível' ou 'emprestado')
            
        Raises:
            ValueError: Se campos obrigatórios estiverem vazios ou inválidos
            TypeError: Se o tipo do estoque não for inteiro
        """
        # Validação de nome
        if not nome or nome is None or nome.strip() == "":
            raise ValueError("Nome do livro é obrigatório")
        
        # Validação de autor
        if not autor or autor is None or autor.strip() == "":
            raise ValueError("Autor do livro é obrigatório")
        
        # Validação de tipo do estoque
        if not isinstance(estoque, int):
            raise TypeError("Estoque deve ser um número inteiro")
        
        # Validação de estoque negativo
        if estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        # Validação de status
        status_validos = ["disponível", "emprestado"]
        if status not in status_validos:
            raise ValueError("Status deve ser 'disponível' ou 'emprestado'")
        
        self.__nome = nome
        self.__autor = autor
        self.__estoque = estoque
        self.__status = status
    
    # Getters
    def get_nome(self):
        """Retorna o nome do livro"""
        return self.__nome
    
    def get_autor(self):
        """Retorna o autor do livro"""
        return self.__autor
    
    def get_estoque(self):
        """Retorna a quantidade em estoque"""
        return self.__estoque
    
    def get_status(self):
        """Retorna o status do livro"""
        return self.__status
    
    # Setters
    def set_nome(self, nome):
        """Define o nome do livro"""
        if not nome or nome.strip() == "":
            raise ValueError("Nome do livro é obrigatório")
        self.__nome = nome
    
    def set_autor(self, autor):
        """Define o autor do livro"""
        if not autor or autor.strip() == "":
            raise ValueError("Autor do livro é obrigatório")
        self.__autor = autor
    
    def set_estoque(self, estoque):
        """Define a quantidade em estoque"""
        if not isinstance(estoque, int):
            raise TypeError("Estoque deve ser um número inteiro")
        if estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
        self.__estoque = estoque
    
    def set_status(self, status):
        """Define o status do livro"""
        status_validos = ["disponível", "emprestado"]
        if status not in status_validos:
            raise ValueError("Status deve ser 'disponível' ou 'emprestado'")
        self.__status = status
    
    # Métodos de serialização
    def to_dict(self):
        """
        Serializa o objeto Livro para um dicionário
        
        Returns:
            dict: Dicionário com os dados do livro
        """
        return {
            "nome": self.__nome,
            "autor": self.__autor,
            "estoque": self.__estoque,
            "status": self.__status
        }
    
    @classmethod
    def from_dict(cls, dados):
        """
        Cria um objeto Livro a partir de um dicionário
        
        Args:
            dados (dict): Dicionário com os dados do livro
            
        Returns:
            Livro: Objeto Livro criado
        """
        return cls(
            dados["nome"],
            dados["autor"],
            dados["estoque"],
            dados["status"]
        )
    
    def __str__(self):
        """Representação em string do livro"""
        return f"Livro: {self.__nome} - Autor: {self.__autor} - Estoque: {self.__estoque} - Status: {self.__status}"
    
    def __repr__(self):
        """Representação técnica do livro"""
        return f"Livro('{self.__nome}', '{self.__autor}', {self.__estoque}, '{self.__status}')"
