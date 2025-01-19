from app import db
from app.models.transacoes_model import Transacao

class Conta(db.Model):
    __tablename__ = 'contas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    instituicao_bancaria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    tipo_conta = db.Column(db.String(50), nullable=False)
    _saldo = db.Column('saldo', db.Float, default=0.0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('contas'))

    def __repr__(self):
        return f'<Conta {self.nome} - Usuário {self.user.email}>'
    

    # Getter para obter o saldo
    @property
    def saldo(self):
        return self._saldo
    
    # Setter para alterar o saldo
    @saldo.setter
    def saldo(self, valor):
        raise AttributeError("Não é possível alterar o saldo diretamente!")
    

    def depositar(self, valor, data, descricao):
        if valor <= 0:
            raise ValueError('O valor deve ser positivo')
        self._saldo += valor
        transacao = Transacao(natureza='deposito', valor=valor, conta=self, data=data, descricao=descricao)
        db.session.add(transacao)
        db.session.commit()

    def sacar(self, valor, data, descricao):
        if valor <= 0:
            raise ValueError("O saque deve ser de um valor positivo")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= valor
        transacao = Transacao(natureza='saque', valor=valor, conta=self, data=data, descricao=descricao)
        db.session.add(transacao)
        db.session.commit()