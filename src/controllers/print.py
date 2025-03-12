import time
from flask import Response, jsonify
from src.dto.print import PrintDto
from src.services.printer import Printer

#imprimir en cola
def print_data(data: PrintDto) -> tuple[Response, int]:
  #parseamos el nombre de la impresora
  printer_name = data['printerName']

  #impresion condicional
  for element in data['content']:
    if element['type'] == 'text':
      response = Printer.print_text(element['text'], printer_name, element['styles'])

      if not response['ok']:
        return jsonify({ 'message': response['message'] }), 400
      
    elif element['type'] == 'img':
      response = Printer.print_image(element['image'], printer_name, element['alignment'])

      if not response['ok']:
        return jsonify({ 'message': response['message'] }), 400
      
    elif element['type'] == 'stop':
      time.sleep(element['time'])
    
  #abrir la caja
  if data['openDrawer']:
    response = Printer.open_drawer(printer_name)
    
    if not response['ok']:
      return jsonify({ 'message': response['message'] }), 400
    
  return jsonify({ 'message': 'Successfully operation' }), 200
