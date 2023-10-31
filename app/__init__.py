from flask import Flask # Importa a classe principal (Flask)
from flask_sqlalchemy import SQLAlchemy # Importa a ORM SQLAlchemy

app = Flask(__name__) # Cria uma instância do Flask na a variável app

# URL do banco: <Nome do Banco>://<Usuário>:<Senha>@<Endereço>/<Nome do banco>
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True # Ativa o rastreamento de modificações
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@127.0.0.1/pfi" # Define a URL do banco de dados
app.config["UPLOAD_FOLDER"] = "uploads" # Pasta onde as fotos ficaram armazenadas
app.secret_key = "q4t7w!z%C*F-JaNd" # Define uma chave de segurança para a aplicação

db = SQLAlchemy(app) # Cria uma instância da ORM

from app.controllers import routes, admin