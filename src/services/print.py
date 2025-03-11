import base64
import win32print
import win32ui
from io import BytesIO
from PIL import Image, ImageWin
from flask import jsonify, Response
from src.dto.print import PrintDto
from src.services.cmds import CmdBuilder
from src.types.print_text import FontStylesType

class Printer:
  @classmethod
  def print_text(cls, text: str, printer_name: str, styles: FontStylesType):
    #comandos a enviar a la impresora
    cmds = CmdBuilder.build_text(text, styles)

    try:
      #configurar la impresora
      printer = win32print.OpenPrinter(printer_name)
      
      #iniciar un trabajo de impresión en modo RAW (envío directo)
      win32print.StartDocPrinter(printer, 1, ("Doc Text", None, "RAW"))
      win32print.StartPagePrinter(printer)

      #enviar comandos a la impresora
      win32print.WritePrinter(printer, cmds)

      #finalizar la conexion con la impresora
      win32print.EndPagePrinter(printer)
      win32print.EndDocPrinter(printer)
      win32print.ClosePrinter(printer)

      return jsonify({
        'ok': True,
        'message': 'Printed successfully', 
      }), 200
      
    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error printing text: {e}'
      }), 400
    
  @classmethod
  def print_image(cls, img: str, printer_name: str):
    try:
      #obtener los comandos para imprimir la imagen
      cmds = CmdBuilder.build_img(img)

    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error processing image: {e}'
      }), 400

    try:
      #configurar la impresora
      printer = win32print.OpenPrinter(printer_name)
      
      #iniciar un trabajo de impresión en modo RAW (envío directo)
      win32print.StartDocPrinter(printer, 1, ("Doc Image", None, "RAW"))
      win32print.StartPagePrinter(printer)

      #enviar comandos a la impresora
      win32print.WritePrinter(printer, cmds)

      #finalizar la conexion con la impresora
      win32print.EndPagePrinter(printer)
      win32print.EndDocPrinter(printer)
      win32print.ClosePrinter(printer)

      return jsonify({
        'ok': True,
        'message': 'Printed successfully', 
      }), 200

    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error printing image: {e}'
      }), 400
  
  @classmethod
  def open_drawer(cls, printer_name: str):
    #obtener el comando para abrir la caja
    cmds = CmdBuilder.build_drawer()

    try:
      printer = win32print.OpenPrinter(printer_name) #configurar la impresora
      win32print.StartDocPrinter(printer, 1, ("Open Drawer", None, "RAW"))  #iniciar un trabajo de impresión en modo RAW (envío directo)
      win32print.WritePrinter(printer, cmds) #enviar el comando de abrir la caja
      
      #cerrar la conexion
      win32print.EndDocPrinter(printer)
      win32print.ClosePrinter(printer)
      
    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error opening drawer: {e}'
      }), 500
    
#imprimir en cola
def print_data(data: PrintDto) -> tuple[Response, int]:
  #parseamos el nombre de la impresora
  printer_name = data['printerName']

  #impresion condicional
  for element in data['content']:
    if element['type'] == 'text':
      response, status_code = Printer.print_text(element['text'], printer_name, element['styles'])

      if status_code != 200:
        return response, status_code
      
    elif element['type'] == 'img':
      response, status_code = Printer.print_image(element['image'], printer_name)

      if status_code != 200:
        return response, status_code
    
    #abrir la caja
    if data['openDrawer']:
      Printer.open_drawer(printer_name)
    
    return response, status_code
