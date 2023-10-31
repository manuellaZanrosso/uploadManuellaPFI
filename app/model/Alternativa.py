from app import db  # Importa a instância que controla o banco de dados

class Alternativa(db.Model):  # Define a classe Escritora, representando escritoras
    __tablename__ = "alternativas"  # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Coluna ID do tipo inteiro - declarada como chave primária
    texto = db.Column(db.String(500), unique=True) # Coluna texto do tipo String
    correta = db.Column(db.Boolean) # Coluna correta do tipo boolean
    pergunta_id = db.Column(db.Integer) # Coluna pergunta_id do tipo inteiro

    def __init__(self, texto,  pergunta_id, correta = False):
        self.texto = texto
        self.correta = correta
        self.pergunta_id = pergunta_id

    def toJson(self):  # Método que retorna todas as informações da classe em formato de dicionário
        return {
            "id": self.id,
            "texto": self.texto,
            "correta": self.correta,
            "pergunta_id": self.pergunta_id
        }
