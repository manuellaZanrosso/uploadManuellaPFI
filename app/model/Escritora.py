from app import db  # Importa a instância que controla o banco de dados

class Escritora(db.Model):  # Define a classe Escritora, representando escritoras
    __tablename__ = "escritoras"  # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Coluna ID do tipo inteiro - declarada como chave primária
    nome = db.Column(db.String(50))  # Coluna nome do tipo String
    nacionalidade = db.Column(db.String(100))  # Coluna nacionalidade do tipo String
    biografia = db.Column(db.Text)  # Coluna biografia do tipo Text
    data_nascimento = db.Column(db.Date)  # Coluna data de nascimento do tipo Date
    data_falecimento = db.Column(db.Date)  # Coluna data de falecimento do tipo Date (pode ser NULL)
    foto = db.Column(db.LargeBinary)
    link = db.Column(db.String(255))

    def __init__(self, nome, biografia, nacionalidade,  data_nascimento, data_falecimento, foto, link):
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.biografia = biografia
        self.data_nascimento = data_nascimento
        self.data_falecimento = data_falecimento
        self.foto = foto
        self.link = link

    def toJson(self):  # Método que retorna todas as informações da classe em formato de dicionário
        return {
            "id": self.id,
            "nome": self.nome,
            "nacionalidade": self.nacionalidade,
            "biografia": self.biografia,
            "data_nascimento": self.data_nascimento,
            "data_falecimento": self.data_falecimento,
            "foto": self.foto,
            "link": self.link
        }
