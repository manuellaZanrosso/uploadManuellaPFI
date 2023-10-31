from flask import render_template, redirect, url_for, request, session, flash
from sqlalchemy import update
import base64

from app import app, db

from app.model.Usuario import Usuario
from app.model.Escritora import Escritora
from app.model.Questao import Questao
from app.model.Alternativa import Alternativa

@app.context_processor # Cria um contexto global, de forma que todas as páginas tenham acesso a sessão do usuário
def injetar_sessao():
    return dict(session=session)

# Rotas para gerenciar as páginas das escritoras
@app.route("/", methods=['GET']) # Rota da página de escritoras
def index():
    if 'acertou' in session: # Verifia se exite cachê do quiz
        session['acertou'] = -1 # Se exitir, reseta

    consulta_escritoras = Escritora.query.all() # Retorna todas as escritoras do banco de dados
    lista_escritoras = [escritora.toJson() for escritora in consulta_escritoras] # Transforma as informações em uma lista com dicionários

    for escritora in lista_escritoras: # percorre a lista de escritoras
        if escritora['foto'] is not None: # Verifica se existe uma foto no banco de dados
            escritora['foto'] = base64.b64encode(escritora['foto']).decode('utf-8') # Transforma a codificação da imagem de Base64 para Utf-8

    return render_template("escritoras.html", lista_escritoras=lista_escritoras) # Carrega o arquivo HTML

@app.route("/escritora/<int:id>", methods=['GET']) # Rota para uma escritora específica
def detalhesEscritora(id):
    escritora = Escritora.query.get(id).toJson() # Retorna uma escritora do banco consultando o ID
    imagem = base64.b64encode(escritora['foto']).decode('utf-8') # Transforma a codificação da imagem de Base64 para Utf-8
    escritora['data_falecimento'] = str(escritora['data_falecimento'])
    print( type(escritora['data_falecimento']))
    return render_template("escritora.html", escritora=escritora, imagem=imagem) # Carrega o arquivo HTML

# Rotas para gerenciar os usuários
@app.route("/cadastrar", methods=['GET', 'POST']) # Rotina de cadastro
def cadastrarUsuario():
    if 'id' not in session: # Verifica se já não há um usuário logado
        if request.method == 'POST':

            # Coleta os dados para login
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            senha_confirmar = request.form['confirmar']

            # Validações para que todos os dados cheguem corretamente
            if (not nome) or (not email) or (not senha) or (not senha_confirmar):
                return redirect(url_for('cadastrarUsuario'))

            # Confirma que as duas senhas inseridas são identicas
            if senha == senha_confirmar:

                # Instancia um novo usuário com base nos dados coletados
                usuario = Usuario(
                    nome=nome,
                    email=email,
                    senha=senha
                )

                try:
                    # Adiciona o usuário no banco de dados
                    db.session.add(usuario)
                    db.session.commit()

                    # Redireciona para a página principal
                    return redirect('/')
                except:
                    return redirect(url_for('cadastrarUsuario'))
            else:
                return redirect(url_for('cadastrarUsuario'))

        return render_template('cadastrar.html')
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST']) # Rotina de login
def logarUsuario():
    if 'id' not in session: # Verifica se já não há um usuário logado
        if request.method == 'POST':

            # Coleta os dados da requisição
            email = request.form['email']
            senha = request.form['senha']

            # Validações para que todos os dados cheguem corretamente
            if (not email) or (not senha):
                return redirect(url_for('logarUsuario'))

            # Instancia um novo usuário com base nos dados coletados
            usuario = Usuario.query.filter_by(email=email).first().toJson()

            # Compara o formulário com as informações do banco de dados
            print(usuario['adm'])

            if (usuario['senha'] == senha):
                session['id'] = usuario['id']
                session['adm'] = usuario['adm']
                session['perguntas'] = [questao.toJson() for questao in Questao.query.all()]
                session['acertou'] = -1
                session['pontos'] = usuario['pontos']

                return redirect(url_for('index')) # Direciona o usuário para a página principal em caso de sucesso

            return redirect(url_for('logarUsuario')) # Direciona o usuário para o formulário caso os dados estejam incorretos

        return render_template('logar.html') # Carrega a página
    else:
        return redirect(url_for('index')) # Caso o usuário já esteja logado, direciona para a página principal

@app.route("/sair", methods=['GET'])
def sairUsuario():
    keys = list(session.keys()) # Coleta todos os dados do usuário armazenados em cachê
    for key in keys: # Percorre cada chave encontrada na sessão
        del session[key] # Deleta a chave

    return redirect(url_for('index')) # Retorna para a página home

@app.route("/quiz/<int:id>", methods=['GET']) # Rota para apresentar as questões do quiz
def quiz(id):
    if 'id' not in session:
        return redirect(url_for('index'))
    try:
        questao = session['perguntas'][id] # Verifica a questão do usuário em cachê
        alternativas = [alternativa.toJson() for alternativa in Alternativa.query.filter_by(pergunta_id=questao['id']).all()] # Carrega a questão do banco de dados

        for alternativa in alternativas: # Percorre as alternativas
            if alternativa['correta']:
                session['correta'] = alternativa['id'] # Guarda o id da alternativa correta em cachê

        if(session['acertou'] == 1): # Verifica se a questão anterior foi respondidada corretamente
            flash('Resposta correta!', 'correta') # Se sim, mostra na tela que foi correta
        if(session['acertou'] == 0):
            flash('Resposta incorreta!', 'incorreta') # Se não, mostra na tela que foi incorreta
        session['acertou'] = -1 # Retorna o cachê para o estado normal (Isso faz com que caso o usuário entre na página novamemnte, a mensagem não seja mostrada de novo)

        return render_template('quiz.html', questao = questao['pergunta'], alternativas = alternativas, id = id+1) # Carrega o template do quiz, passando as alternativas o id da próxima questão (para gerar o link)

    except Exception: # Caso não encontre a próxima questão, significa que o quiz aacabou
        query = ( # Altera o número de pontos do usuário
            update(Usuario)
            .where(Usuario.id == session['id'])
            .values(pontos = session['pontos'])
        )

        db.session.execute(query) # Executa a query de alteração
        db.session.commit() # Salva a alteração no banco de dados
        return redirect(url_for('index')) # Volta para home

@app.route('/quiz-check/<int:id>/<int:resposta>', methods=['POST']) # Rota para validar se o usuário acertou o errou a questão
def quizCheck(id, resposta):

    session['acertou'] = 0 # Coloca em cachê que o usuário não acertou a questão

    if (resposta == session['correta']):
        session['acertou'] = 1 # Altera o cachê caso ele tenha acertado
        session['pontos'] += 1 # Adiciona um ponto ao usuário

    del session['correta']
    return redirect('/quiz/' + str(id)) # Retornar para o página do quiz

@app.route('/pontuacao')
def pontuacao():
    if 'id' in session:
    # Busca todos os usuários no banco de dados
        usuarios_ordenados_consulta = db.session.query(Usuario).order_by(Usuario.pontos.desc()).all()
        usuarios_ordenados = [usuario.toJson() for usuario in usuarios_ordenados_consulta]

        # Encontra a posição do usuário logado na lista ordenada
        posicao = None
        for i, usuario in enumerate(usuarios_ordenados):
            if usuario['id'] == session['id']:
                usuario_logado = usuario
                posicao = i + 1
                break

        return render_template('pontuacao.html', usuarios=usuarios_ordenados, usuario = usuario_logado, posicao = posicao)
    return redirect(url_for('index'))