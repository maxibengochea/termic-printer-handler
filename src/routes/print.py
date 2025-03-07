from flask import Blueprint
from flask import request, jsonify
from src.dto.print_text import PrintextDto
from src.services.printer import Printer

print_router = Blueprint('print', __name__, url_prefix='/print')

@print_router.route('/text', methods=['POST'])
def print_text():
  #capturar el body
  data: PrintextDto = request.get_json(silent=True)
  
  try:
    #imprimir el texto
    Printer.print_text(data['text'], printer_name=data['printerName'], styles=data['styles'])

    return jsonify({
      'ok': True,
      'message': 'Text printed successfully', 
    })
    
  except Exception as e:
    return jsonify({
      'ok': False,
      'message': str(e)
    })
  
@print_router.route('/image', methods=['POST'])
def print_image():
  #capturar el body
  data = request.get_json(silent=True)
  
  try:
    #imprimir la imagen
    Printer.print_image(data['image'], printer_name=data['printerName'])

    return jsonify({
      'ok': True,
      'message': 'Img printed successfully' 
    })

  except Exception as e:
    return jsonify({
      'ok': False,
      'message': str(e)
    })
