from flask import render_template, request, redirect, url_for, session
import base64

from app import app, db

from app.model.Escritora import Escritora
from app.model.Questao import Questao
from app.model.Alternativa import Alternativa

# Rotas do usuário administrador
@app.route("/adm", methods=['GET'])
def administrar():
    if 'id' in session and session['adm'] == True:
        return render_template("administrar.html")
    return redirect(url_for('index'))

@app.route("/adm/escritora", methods=['GET', 'POST']) # Rota para inserir escritora
def criarEscritora():
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        if request.method == 'POST':

            # Coleta os dados da requisição
            nome = request.form['nome']
            nacionalidade = request.form['nacionalidade']
            biografia = request.form['biografia']
            data_nascimento = request.form['data_nascimento']
            data_falecimento = '9999-12-01'
            foto = None
            link = None

            if 'link' in request.form:
                link = request.form['link']

            if 'data_falecimento' in request.form:
                data_falecimento = request.form['data_falecimento']

            if 'foto' in request.files: # Verifica se existe uma foto na requisição
                foto = request.files['foto'] # Coleta a foto da requisição

            # Instancia uma nova escritora com base nos dados coletados na requisição
            nova_escritora = Escritora(
                nome=nome,
                nacionalidade=nacionalidade,
                biografia=biografia,
                data_nascimento=data_nascimento,
                data_falecimento=data_falecimento,
                foto=foto.read(),
                link=link
            )

            db.session.add(nova_escritora) # Grava a escritora no banco de dados
            db.session.commit() # Confirma as alterações no banco de dados

            return redirect(url_for('index')) # Retorna para a tela principal
        else:
            return render_template('adicionar-escritora.html') # Carrega a página

@app.route("/adm/escritora/deletar", methods=['GET']) # Rota para deletar escritoras
def deletarEscritora():
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        consulta_escritoras = Escritora.query.all() # Retorna todas as escritoras do banco de dados
        lista_escritoras = [escritora.toJson() for escritora in consulta_escritoras] # Transforma as informações em uma lista com dicionários

        for escritora in lista_escritoras: # percorre a lista de escritoras
            if escritora['foto'] is not None: # Verifica se existe uma foto no banco de dados
                escritora['foto'] = base64.b64encode(escritora['foto']).decode('utf-8') # Transforma a codificação da imagem de Base64 para Utf-8

        return render_template('deletar-escritoras.html', lista_escritoras=lista_escritoras)

@app.route("/deletar/escritora/<int:id>", methods=['GET'])
def apagarEscritora(id):
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        db.session.delete(Escritora.query.get(id))
        db.session.commit()
        return redirect(url_for('deletarEscritora'))
    return redirect(url_for('index'))

@app.route("/adm/quiz", methods=['GET', 'POST']) # Rota para o quiz
def criarPergunta():
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        if request.method == 'POST':

            print(request.form.keys())
            (['pergunta', 'texto-a', 'correta-a', 'texto-b', 'texto-c', 'texto-d'])

            # Coleta os dados das perguntas
            pergunta = request.form['pergunta']
            questao = Questao(pergunta=pergunta)

            db.session.add(questao)
            db.session.commit()

            pergunta_a = request.form['texto-a'] # Coleta a pergunta
            correta_a = 'a' in request.form # Guarda se é correta ou não
            alternativa_a = Alternativa(texto=pergunta_a, correta=correta_a, pergunta_id=questao.id) # Instancia o objeto
            db.session.add(alternativa_a) # Salva no banco de dados

            pergunta_b = request.form['texto-b']
            correta_b = 'b' in request.form
            alternativa_b = Alternativa(texto=pergunta_b, correta=correta_b, pergunta_id=questao.id)
            db.session.add(alternativa_b)

            pergunta_c = request.form['texto-c']
            correta_c = 'c' in request.form
            alternativa_c = Alternativa(texto=pergunta_c, correta=correta_c, pergunta_id=questao.id)
            db.session.add(alternativa_c)

            pergunta_d = request.form['texto-d']
            correta_d = 'd' in request.form
            alternativa_d = Alternativa(texto=pergunta_d, correta=correta_d, pergunta_id=questao.id)
            db.session.add(alternativa_d)

            db.session.commit() # Confirma as alterações no banco de dados

            session['perguntas'] = [questao.toJson() for questao in Questao.query.all()]
            return redirect(url_for('administrar')) # Retorna para a tela de administração
        else:
            return render_template('adicionar-pergunta.html') # Carrega a página

@app.route("/adm/quiz/deletar", methods=['GET']) # Rota para deletar questoes
def deletarQuestao():
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        consulta_questoes = Questao.query.all() # Retorna todas as questoes do banco de dados
        lista_questoes = [questao.toJson() for questao in consulta_questoes] # Transforma as informações em uma lista com dicionários

        return render_template('deletar-questoes.html', lista_questoes=lista_questoes) # Carrega a página de questões para deletar

@app.route("/deletar/questao/<int:id>", methods=['GET']) # Rota para deletar a questao do banco
def apagarQuestao(id):
    if 'id' in session and session['adm'] == True: # Verifica se existe um usuário do tipo ADM logado
        questao = Questao.query.get(id)  # Seleciona a questão com base no ID
        alternativas = Alternativa.query.filter_by(pergunta_id=id).all() # Seleciona todas as alternativas com base no ID da questão
        for alternativa in alternativas: # Percorre a lista de alternativas
            db.session.delete(alternativa)  # Deleta cada alternativa
        db.session.delete(questao)  # Deleta a questão
        db.session.commit() # Salva a alteração
        return redirect(url_for('deletarQuestao')) # Redireciona para a página com as questões
    return redirect(url_for('index')) # Redireciona para a página inicial, caso não seja ADM
