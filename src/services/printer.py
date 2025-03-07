import win32print
import win32ui
import base64
from enum import Enum
from io import BytesIO
from PIL import Image, ImageWin

#comandos ESC/POS para estilar el texto
class FontStyles(Enum):
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
  RIGHT_ALIGN = b'\x1B\x61\x02'
  UNDERLINED = b'\x1B\x2D\x01'

def _build_escpos_cmds(styles: dict, text: str):
  #comenzar código ESC/POS
  escpos_cmds = b'\x1B\x40'  

  #configurar la alineacion
  if styles.get('alignment', None) == "right":
    escpos_cmds += FontStyles.RIGHT_ALIGN.value
  
  elif styles.get('alignment', None) == "left":
    escpos_cmds += FontStyles.LEFT_ALIGN.value
  
  elif styles.get('alignment', None) == "center":
    escpos_cmds += FontStyles.CENTER_ALIGN.value

  #estilar la negrita
  if styles.get('bold', False) == True:
    escpos_cmds += FontStyles.BOLD.value
    
  else:
    escpos_cmds += FontStyles.NOT_BOLD.value
      
  #estilar el subrayado
  if styles.get('underlined', False) == True:
    escpos_cmds += FontStyles.UNDERLINED.value

  else:
    escpos_cmds += FontStyles.NOT_UNDERLINED.value

  #estilar la fuente
  if styles.get('fonSize', None) == 'fontA':
    escpos_cmds += FontStyles.FONT_A.value
      
  elif styles.get('fonSize', None) == 'fontB':
    escpos_cmds += FontStyles.FONT_B.value
    
  elif styles.get('fonSize', None) == 'fontC':
    escpos_cmds += FontStyles.FONT_C.value

  #estilar el tamaño
  if styles.get('doubleWidthHeight', False) == True:
    escpos_cmds += FontStyles.DOUBLE_WIDTH_HEIGHT.value

  elif styles.get('doubleWidth', False) == True:
    escpos_cmds += FontStyles.DOUBLE_HEIGHT.value

  elif styles.get('doubleHeight', False) == True:
    escpos_cmds += FontStyles.DOUBLE_WIDTH.value

  #codificar el texto
  return escpos_cmds + text.encode('utf-8') + b'\n' 

class Printer:
  @classmethod
  def print_text(cls, text: str, printer_name='IMP1', styles: dict = {}):
    comand = _build_escpos_cmds(styles, text)

    try:
      #configurar la impresora
      printer = win32print.OpenPrinter(printer_name)
      printer_dc = win32ui.CreateDC()
      printer_dc.CreatePrinterDC(printer_name)
      printer_dc.StartDoc("Doc Text")
      printer_dc.StartPage()

      #enviar comandos a la impresora
      printer_dc.Write(comand) 

      #finalizar la conexion con la impresora
      printer_dc.EndPage()
      printer_dc.EndDoc()
      
    except Exception as e:
      print(f"Operation failed: {e}")

    finally:
      win32print.ClosePrinter(printer)
    
  @classmethod
  def print_image(cls, img: str, printer_name='IMP1'):
    #decodificar la imagen
    image_data = base64.b64decode(img)
    image = Image.open(BytesIO(image_data))

    #procesar la imagen
    image = image.convert("L").convert("1") #convertir la imagen a escala de grises y monocromática (1-bit)
    width, height = image.size #obtener el tamaño de la imagen
    
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

    except Exception as e:
      print(f"Operation failed: {e}")

    finally:
      win32print.ClosePrinter(printer)
