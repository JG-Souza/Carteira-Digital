from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from app import app, db, login_manager
from app.models.users_model import User


def redirect_if_authenticated(route='dashboard'):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(route))  # Redireciona o usuário logado
            return f(*args, **kwargs)  # Permite o acesso à rota
        return wrapped
    return decorator


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@redirect_if_authenticated(route='dashboard')
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Esse email já está em uso."
        new_user = User(email=email, password=password, name=name)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        user = User.query.get(current_user.id)

        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if email and email != user.email:
            user.email = email
        if password and password != user.password:
            user.password = password
        if name and name != user.name:
            user.name = name

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

        return redirect(url_for('ver_perfil'))
    
    return render_template('dashboard.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
@redirect_if_authenticated(route='dashboard')
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Falha no login. Usuário ou senha incorretos.'
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def ver_perfil():
    return render_template('ver_perfil.html', user=current_user)


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    user = User.query.get(current_user.id)
    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('register'))

