from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

# Flask Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Importações tardias para evitar circularidade de dependências

from app.controllers import users_controller
from app.controllers import contas_controller

from app.models import users_model
from app.models import contas_model

from app.controllers.contas_controller import contas_bp
app.register_blueprint(contas_bp, url_prefix='/contas')