from app import db  # Importa a instância que controla o banco de dados

class Questao(db.Model):  # Define a classe Escritora, representando escritoras
    __tablename__ = "questoes"  # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Coluna ID do tipo inteiro - declarada como chave primária
    pergunta = db.Column(db.String(500))  # Coluna questao do tipo String

    def __init__(self, pergunta):
        self.pergunta = pergunta

    def toJson(self):  # Método que retorna todas as informações da classe em formato de dicionário
        return {
            "id": self.id,
            "pergunta": self.pergunta
        }
