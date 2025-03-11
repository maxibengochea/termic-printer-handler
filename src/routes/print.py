from flask import Blueprint
from flask import request
from src.dto.print import PrintDto
from src.services.printer import print_data

print_router = Blueprint('print', __name__, url_prefix='/print')

@print_router.route(methods=['POST'])
def print():
  data: PrintDto = request.get_json(silent=True)  #capturar el body 
  return print_data(data) #imprimir el texto
