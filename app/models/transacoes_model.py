from app import db
from datetime import datetime

class Transacao(db.Model):
    __tablename__ = 'transacoes'
    id = db.Column(db.Integer, primary_key=True)
    natureza = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)  # Data da transação
    descricao = db.Column(db.String(200))

    conta_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    conta = db.relationship('Conta', backref=db.backref('transacoes', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transacoes'), lazy=True)

    def __init__(self, natureza, valor, conta, descricao=None):
        self.natureza = natureza
        self.valor = valor
        self.conta = conta
        self.user = conta.user
        self.descricao = descricao

    def __repr__(self):
        return f"<Transacao {self.natureza} de R${self.valor} na conta {self.conta.nome}>"
