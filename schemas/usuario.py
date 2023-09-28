from pydantic import BaseModel
from typing import Optional, List
from models.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    email: str = "email@email.com.br"
    password: str = "************"
    


class UsuarioViewSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    email: str = "email@email.com.br"
    password: str = "************"