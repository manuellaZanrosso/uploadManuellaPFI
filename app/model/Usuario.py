from app import db # Importa do arquivo principal a instância que controla o banco de dados

class Usuario(db.Model): # Cria a classe usuário, herdando um modelo da instância db
    __tablename__ = "usuarios" # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True) # Coluna ID do tipo inteiro - declarada como chave primária
    nome = db.Column(db.String(50)) # Coluna nome do tipo String
    email = db.Column(db.String(50), unique=True) # Coluna email do tipo String - declarada como única
    senha = db.Column(db.String(50)) # Coluna senha declarada como String
    adm = db.Column(db.Boolean) # Coluna adm declarada como boolean
    pontos = db.Column(db.Integer) # Coluna pontos declarada como inteiro

    def __init__(self, nome, email, senha, adm = False, pontos = 0): # Método construtor da classe
        self.nome = nome
        self.email = email
        self.senha = senha
        self.adm = adm
        self.pontos = pontos

    def toJson(self): # Método que retorna todas as informações existentes da classe em formato de dicionário
        return {
            "id":self.id,
            "nome":self.nome,
            "email":self.email,
            "senha":self.senha,
            "pontos":self.pontos,
            "adm": self.adm
        }