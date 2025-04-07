from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models.users_model import User
from app.models.contas_model import Conta
from app.models.transacoes_model import Transacao
from datetime import datetime

contas_bp = Blueprint('contas', __name__)


@contas_bp.route('/criar/<int:user_id>', methods=['GET', 'POST'])
@login_required
def criar_conta(user_id):
    if request.method == 'POST':
        nome = request.form['nome'] 
        instituicao_bancaria = request.form.get('instituicao_bancaria') # Se o campo for nulo, o get retorna None
        descricao = request.form.get('descricao')
        tipo_conta = request.form.get('tipo_conta')
        
        nova_conta = Conta(nome=nome, instituicao_bancaria=instituicao_bancaria, descricao=descricao, tipo_conta=tipo_conta, user_id=user_id)
        db.session.add(nova_conta) 
        db.session.commit()

        return redirect(url_for('contas.ver_contas', user_id=user_id))

    return render_template('criar_conta.html', user_id=user_id)


@contas_bp.route('/update/<int:conta_id>', methods=['GET', 'POST'])
@login_required
def update(conta_id):
    conta = Conta.query.get(conta_id)

    if not conta:
        return "Conta não encontrada", 404

    if conta.user_id != current_user.id:
        return "Acesso não autorizado", 403

    if request.method == 'POST':
        nome = request.form.get('nome')
        instituicao = request.form.get('instituicao_bancaria')
        descricao = request.form.get('descricao')
        tipo_conta = request.form.get('tipo_conta')

        if nome and nome != conta.nome:
            conta.nome = nome
        if instituicao and instituicao != conta.instituicao_bancaria:
            conta.instituicao_bancaria = instituicao
        if descricao and descricao != conta.descricao:
            conta.descricao = descricao
        if tipo_conta and tipo_conta != conta.tipo_conta:
            conta.tipo_conta = tipo_conta

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Erro ao atualizar conta: {str(e)}", 500

        return redirect(url_for('contas.ver_contas', user_id=conta.user_id))
    
    return render_template('dashboard.html', conta=conta)


@contas_bp.route('/<int:user_id>/contas')
@login_required
def ver_contas(user_id):
    user = User.query.get(user_id)
    transacoes = Transacao.query.all()
    if user:
        contas = user.contas
        saldo_total = sum(conta.saldo for conta in contas)  
        return render_template('ver_contas.html', contas=contas, user=current_user, saldo_total=saldo_total, transacoes=transacoes)
    return "User not found", 404


@contas_bp.route('/<int:user_id>/conta/<int:conta_id>')
@login_required
def detalhe_conta(user_id, conta_id):
    user = User.query.get(user_id)
    conta = Conta.query.get(conta_id)
    if conta:
        return render_template('detalhe_conta.html', conta=conta, user_id=user_id, conta_id=conta_id, user=user)


@contas_bp.route('/<int:conta_id>/depositar', methods=['POST'])
@login_required
def depositar(conta_id):
    conta = Conta.query.get(conta_id)
    if conta.user_id != current_user.id:
        return "Acesso não autorizado", 403
    
    data = datetime.strptime(request.form.get('data'), '%Y-%m-%d') # Convertendo para datetime
    descricao = request.form.get('descricao')
    if conta:
        valor = float(request.form['valor'])
        try:
            conta.depositar(valor, data, descricao)
            return redirect(url_for('contas.ver_contas', user_id=conta.user_id)) # trocar a rota
        except ValueError as e:
            return str(e), 400 # Criar template dinamica para erros
    return 'Conta não encontrada', 404


@contas_bp.route('/<int:conta_id>/sacar', methods=['POST'])
@login_required
def sacar(conta_id):
    conta = Conta.query.get(conta_id)
    if conta.user_id != current_user.id:
        return "Acesso não autorizado", 403

    if conta:
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form.get('data'), '%Y-%m-%d') # Convertendo para datetime
        descricao = request.form.get('descricao')
        try:
            conta.sacar(valor, data, descricao)
            return redirect(url_for('contas.ver_contas', user_id=conta.user_id)) # trocar a rota
        except ValueError as e:
            return str(e), 400
    return "Conta não encontrada", 404


@contas_bp.route('<int:user_id>/conta/<int:conta_id>/extrato', methods=["GET"])
@login_required
def ver_extrato(user_id, conta_id):
    user = User.query.get(user_id)
    conta = Conta.query.get(conta_id)

    if conta and conta.user_id == user.id:
        transacoes = Transacao.query.filter_by(conta_id=conta.id).all()
        return render_template('extrato_conta.html', transacoes=transacoes, conta=conta, user=user)
    
    return redirect(url_for('contas.ver_contas', user_id=user.id))


@contas_bp.route('<int:user_id>/conta/<int:conta_id>/delete', methods=['POST'])
@login_required
def delete(user_id, conta_id):
    user = User.query.get(user_id)
    conta = Conta.query.get(conta_id)

    if not user or not conta or conta.user_id != current_user.id:
        return "Acesso não autorizado ou conta inexistente", 403

    try:
        # Deletar transações da conta
        transacoes = Transacao.query.filter_by(conta_id=conta.id).all()
        for transacao in transacoes:
            db.session.delete(transacao)

        # Deletar conta
        db.session.delete(conta)
        db.session.commit()

        return redirect(url_for('contas.ver_contas', user_id=user.id))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao deletar conta: {str(e)}", 500
    

@contas_bp.route('<int:conta_id>/transacao/delete/<int:transacao_id>', methods=['POST'])
@login_required
def delete_transacao(transacao_id, conta_id):
    transacao = Transacao.query.get(transacao_id)

    if not transacao or transacao.conta_id != conta_id:
        return "Transação não encontrada ou conta incorreta", 404

    conta = transacao.conta

    # Verifica se a conta pertence ao usuário logado
    if conta.user_id != current_user.id:
        return "Acesso não autorizado", 403

    try:
        # Reverte o saldo
        if transacao.natureza == 'saque':
            conta._saldo += transacao.valor
        elif transacao.natureza == 'deposito':
            conta._saldo -= transacao.valor

        db.session.delete(transacao)
        db.session.commit()

        return redirect(url_for('contas.ver_extrato', conta_id=conta_id, user_id=current_user.id))

    except Exception as e:
        db.session.rollback()
        return f"Erro ao deletar transação: {str(e)}", 500


