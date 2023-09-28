from flask import request
import hashlib
import base64
from dotenv import load_dotenv
from envs import  env
# from app import app

load_dotenv()


# Chave secreta compartilhada no backend
SECRET_KEY_BACKEND = env('SECRET_WORD')
password = SECRET_KEY_BACKEND
# Gerar o hash com base na palavra secreta para comparar com o hash recebido
def generate_key_from_password(password):
    hashed_password = hashlib.sha256(password.encode()).digest()
    key = base64.b64encode(hashed_password).decode()
    return key

# Middleware para autenticar com a chave recebida no header
def authenticate_with_key():
    key_received = request.headers.get("X-Secret-Key")
    print("Chave Servidor Chegou = ", key_received)
    # Gere a chave a partir da mesma palavra-chave no backend
    expected_key = generate_key_from_password(SECRET_KEY_BACKEND)
    print("Chave Servidor = ", key_received)
    print("Chave Esperada = ", expected_key)
    # Compare a chave recebida com a chave esperada
    if key_received != expected_key:
        # Chave inválida, retorne uma resposta de erro (por exemplo, 401 Unauthorized)
        return {"message": "Chave de autenticação inválida"}, 401