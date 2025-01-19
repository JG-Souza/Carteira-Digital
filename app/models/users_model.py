from app import db

class User(db.Model):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # O email não pode ser nulo
    password = db.Column(db.String(20), nullable=False)  # A senha não pode ser nula
    name = db.Column(db.String(20), nullable=False)

    # Propriedade que sempre retorna True, usado pelo Flask-Login para indicar que o usuário está autenticado
    @property
    def is_authenticated(self):
        return True
    
    # Propriedade que sempre retorna True, indicando que o usuário está ativo
    @property
    def is_active(self):
        return True
    
    # Propriedade que sempre retorna False, indicando que o usuário não é anônimo
    @property
    def is_anonymous(self):
        return False
    
    # Método que retorna o ID do usuário como uma string, necessário para o Flask-Login
    def get_id(self):
        return str(self.id)

    # Construtor da classe. Inicializa um novo usuário com as informações fornecidas.
    def __init__(self, password, name, email):
        self.password = password
        self.name = name
        self.email = email


    def __repr__(self):
        return f'<User {self.name}>'