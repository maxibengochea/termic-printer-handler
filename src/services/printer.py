import base64
import win32print
import win32ui
from enum import Enum
from io import BytesIO
from PIL import Image, ImageWin
from flask import jsonify, Response
from src.dto.print import PrintDto
from src.types.print_text import FontStylesType

#comandos ESC/POS para estilar el texto
class EscPosCmds(Enum):
  BOLD = b'\x1B\x45\x01'
  CENTER_ALIGN = b'\x1B\x61\x01'
  DOUBLE_HEIGHT = b'\x1D\x21\x01'
  DOUBLE_WIDTH = b'\x1D\x21\x10'
  DOUBLE_WIDTH_HEIGHT = b'\x1D\x21\x11'
  FONT_A = b'\x1B\x4D\x00'
  FONT_B = b'\x1B\x4D\x01'
  FONT_C = b'\x1B\x4D\x02'
  LEFT_ALIGN = b'\x1B\x61\x00'
  NOT_BOLD = b'\x1B\x45\x00'
  NOT_UNDERLINED = b'\x1B\x2D\x00'
  OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'
  RIGHT_ALIGN = b'\x1B\x61\x02'
  UNDERLINED = b'\x1B\x2D\x01'

class Printer:
  @classmethod
  def print_text(cls, text: str, printer_name: str, styles: FontStylesType):
    #comandos a enviar a la impresora
    cmds = cls._build_escpos_cmds(styles, text)

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
      
    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error printing text: {e}'
      }), 500
    
  @classmethod
  def print_image(cls, img: str, printer_name: str):
    try:
      #decodificar la imagen
      image_data = base64.b64decode(img)
      image = Image.open(BytesIO(image_data))

      #procesar la imagen
      image = image.convert("L").convert("1") #convertir la imagen a escala de grises y monocromática (1-bit)
      width, height = image.size #obtener el tamaño de la imagen
    
    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error processing image: {e}'
      }), 400

    try:
      #configurar la impresora
      printer = win32print.OpenPrinter(printer_name)
      printer_handle = win32print.StartDocPrinter(printer, 1, ("Print Img", None, "RAW"))
      printer_dc = win32ui.CreateDC()
      printer_dc.CreatePrinterDC(printer_name)
      printer_dc.StartDoc("Image")
      printer_dc.StartPage()

      #dibujar la imagen en la impresora
      dib = ImageWin.Dib(image)
      dib.draw(printer_dc.GetHandleOutput(), (0, 0, width, height))

      #finalizar la conexion con la impresora
      printer_dc.EndPage()
      printer_dc.EndDoc()
      printer_dc.DeleteDC()
      win32print.EndDocPrinter(printer_handle)
      win32print.ClosePrinter(printer)

    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error printing image: {e}'
      }), 500
  
  @classmethod
  def open_drawer(cls, printer_name: str):
    try:
      printer = win32print.OpenPrinter(printer_name) #configurar la impresora
      win32print.StartDocPrinter(printer, 1, ("Open Drawer", None, "RAW"))  #iniciar un trabajo de impresión en modo RAW (envío directo)
      win32print.WritePrinter(printer, EscPosCmds.OPEN_DRAWER.value) #enviar el comando de abrir la caja
      
      #cerrar la conexion
      win32print.EndDocPrinter(printer)
      win32print.ClosePrinter(printer)
      
    except Exception as e:
      return jsonify({
        'ok': False,
        'message': f'Error opening drawer: {e}'
      }), 500
    
  #construir la cadena de comandos con los estilos proporcionados
  def _build_escpos_cmds(styles: FontStylesType, text: str):
    #comenzar código ESC/POS
    escpos_cmds = b''  

    #configurar la alineacion
    if 'alignment' in styles.keys():
      if styles['alignment'] == "right":
        escpos_cmds += EscPosCmds.RIGHT_ALIGN.value

      elif styles['alignment'] == "left":
        escpos_cmds += EscPosCmds.LEFT_ALIGN.value

      elif styles['alignment'] == "center":
        escpos_cmds += EscPosCmds.CENTER_ALIGN.value

    #estilar la fuente
    if 'fontType' in styles.keys():
      if styles['fontType'] == 'fontA':
        escpos_cmds += EscPosCmds.FONT_A.value

      elif styles['fontType'] == 'fontB':
        escpos_cmds += EscPosCmds.FONT_B.value

      elif styles['fontType'] == 'fontC':
        escpos_cmds += EscPosCmds.FONT_C.value

    #estilar el tamaño
    if 'fontSize' in styles.keys():
      if styles['fontSize'] == 'doubleWidthHeight':
        escpos_cmds += EscPosCmds.DOUBLE_WIDTH_HEIGHT.value

      elif styles['fontSize'] == 'doubleWidth':
        escpos_cmds += EscPosCmds.DOUBLE_HEIGHT.value

      elif styles['fontSize'] == 'doubleHeight':
        escpos_cmds += EscPosCmds.DOUBLE_WIDTH.value

    escpos_cmds += EscPosCmds.BOLD.value if 'bold' in styles.keys() else EscPosCmds.NOT_BOLD.value #estilar la negrita
    escpos_cmds += EscPosCmds.UNDERLINED.value if 'underlined' in styles.keys() else EscPosCmds.NOT_UNDERLINED.value #estilar el subrayado
    escpos_cmds += text.encode('utf-8') #codificar el texto
    return escpos_cmds

#imprimir en cola
def print_data(data: PrintDto) -> tuple[Response, int]:
  #parseamos el nombre de la impresora
  printer_name = data['printerName']

  #impresion condicional
  try:
    for element in data['content']:
      if element['type'] == 'text':
        Printer.print_text(element['text'], printer_name, element['styles'])

      elif element['type'] == 'img':
        Printer.print_image(element['image'], printer_name)
    
    #abrir la caja
    if data['openDrawer']:
      Printer.open_drawer(printer_name)
    
    return jsonify({
        'ok': True,
        'message': 'Printed successfully', 
      }), 200
  
  except Exception as e:
    return e
