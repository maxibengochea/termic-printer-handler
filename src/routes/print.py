from flask import Blueprint
from flask import request
from src.controllers.print import print_data
from src.dto.print import PrintDto

print_router = Blueprint('print', __name__)

@print_router.route('/print', methods=['POST'])
def print():
  data: PrintDto = request.get_json(silent=True)  #capturar el body 
  return print_data(data) #imprimir el texto
