class Usuario():


    def __init__(self, email, password):
        """
        Cria um Usuario

        Arguments:
            email: email do Usuario.
            password: Senha atual do Usuario
        """
        self.email = email
        self.password = password

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Usuario.
        """
        return{
            # "id": self.id,
            "email": self.email,
            "password": self.password            
        }

    def __repr__(self):
        """
        Retorna uma representação do Usuario em forma de texto.
        """
        return f"Product(email='{self.email}', password={self.password}')"
