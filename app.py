from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, session, jsonify
from urllib.parse import unquote
from dotenv import load_dotenv
import pyrebase
from envs import env

from models import Usuario
from logger import logger
from schemas import *

from middleware import auth_middleware

load_dotenv()

info = Info(title="API Autenticação FireBase", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configuração do FireBase
config = {
    'apiKey': env('API_KEY'),
    'authDomain': env('AUTH_DOMAIN'),
    'projectId': env('PROJECT_ID'),
    'storageBucket': env('STORAGE_BUCKET'),
    'messagingSenderId': env('MESSAGING_SENDER_ID'),
    'appId': env('APP_ID'),
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = env('SECRET_KEY')

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuários no FireBase")

# Middleware para autenticar com a chave recebida no header
@app.before_request
def before_request():
    auth_middleware.authenticate_with_key()

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Criar um novo usuário no FireBase
@app.post('/usuario', tags=[usuario_tag], 
          responses={"200": UsuarioViewSchema, 
                     "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(query: UsuarioSchema):
    data = request.json
    email = data.get('email')
    password = data.get('password')
    """Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuarios.
    """
    # email = request.args.get('email')
    # password = request.args.get('password')
    
    logger.info(f"Adicionando usuário: '{email}'")

    try:
        if not email or not password:
            error_msg = "Email e Senha Obrigatórios"
            return {"message": error_msg}, 400
                        
        # adicionando usuário
        user = auth.create_user_with_email_and_password(email, password)
        logger.info("Adicionado usuário: %s" % email)
        user_data = {
            "user_id": user['localId'],  # ou outra chave que você queira retornar
            "email": email,
            "message": "Usuário adicionado com sucesso"
        }
        return user_data, 200
    except ValueError as e:
        error_msg = str(e)
        logger.warning(error_msg)
        return {"message": error_msg}, 404
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o usuário :/"
        logger.warning(f"Erro ao adicionar email '{email}', {error_msg}")
        return {"message": error_msg}, 400

# Fazer Login no sistema
@app.post('/login', tags=[usuario_tag])
def login(query: UsuarioSchema):
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if 'user' in session:
        print("Eu entrei no if do user")
        email = session['user']
        print("eu entrei no if para testar o user session", email)
        token = session.get('token_firebase')
        print("eu entrei no if para testar o user session", token)
        
        if token:
            email = session['user']
            # user = auth.get_user_by_email(email)
            print("entrei no if do token", email)
            try:
                print("entrei no try")
                email = session['user']
                print("user que está tentando ser autenticado", email)
                token = session.get('token_firebase')
                # auth.get_account_info(token)
                # token = auth.create_custom_token(email)
                print("Token de USuário Logado", token)
                
                session['token_firebase'] = token
                
                return {"message": "Olá usuário, {}, você já está logado!".format(email), "token": token}, 200
            except Exception as e:
                error_msg = 'Erro ao verificar autenticação do usuário, {}'.format(email)
                return {"message": error_msg, "token": None}, 401
        else:
            error_msg = 'Token de usuário não encontrado na sessão'
            return {"message": error_msg, "token": None}, 401
    else:
        print("Eu entrei no else para tentar logar user: ", email)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            
            if user:
                token = user['idToken']
                
                session['user'] = email
                session['token_firebase'] = token
                
                return {"message": "Login bem-sucedido", "token": token}, 200
            else:
                error_msg = 'Falha ao tentar logar, {}'.format(email)
                return {"message": error_msg, "token": None}, 401
        
        except Exception as e:
            error_msg = 'Falha ao tentar logar, {}'.format(email)
            return {"message": error_msg, "token": None}, 401

@app.get('/logout', tags=[home_tag])
def logout():
    """Realiza o logout do usuário e retorna um código de sucesso 200.
    """
    if 'user' in session:
        session.pop('user')
    
    # Retorna um código de sucesso 200 e uma mensagem indicando o logout bem-sucedido
    return jsonify({"message": "Logout bem-sucedido"}), 200