from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.routes.print import print_router
import os

#usar las variables de entorno
load_dotenv()

#inicializar la app
def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
  app.register_blueprint(print_router)
  CORS(app)
  return app
