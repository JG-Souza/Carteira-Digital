# Sintetiza as configurações do ORM e app
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv('DEBUG')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')