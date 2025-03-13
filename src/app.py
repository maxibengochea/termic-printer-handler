from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.routes.print import print_router
import os

#usar las variables de entorno
load_dotenv()

#inicializar la app
def create_app():
  app = Flask(__name__) #crear la instancia de Flask
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #usar la secret key de la variable de entorno
  app.register_blueprint(print_router) #registrar las rutas
  CORS(app) #permitir peticiones de todas las rutas
  return app
