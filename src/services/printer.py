import win32print
from src.services.cmds import CmdBuilder
from src.types.print_text import FontStylesType
from typing import TypedDict

#tipar la respuesta del printer
class ResponsePrinterType(TypedDict):
  ok: bool
  message: str

class Printer:
  @classmethod
  def print_text(cls, text: str, printer_name: str, styles: FontStylesType) -> ResponsePrinterType:
    #comandos a enviar a la impresora
    cmds = CmdBuilder.build_text(styles, f'{text}\n')

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

      return { 'ok': True }
      
    except Exception as e:
      return {
        'ok': False,
        'message': f'Error printing text: {e}'
      }
    
  @classmethod
  def print_image(cls, img: str, printer_name: str, alignment: str) -> ResponsePrinterType:
    try:
      #obtener los comandos para imprimir la imagen
      cmds = CmdBuilder.build_img(img, alignment)

    except Exception as e:
      return {
        'ok': False,
        'message': f'Error processing image: {e}'
      }

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

      return { 'ok': True }

    except Exception as e:
      return {
        'ok': False,
        'message': f'Error printing image: {e}'
      }
  
  @classmethod
  def open_drawer(cls, printer_name: str) -> ResponsePrinterType:
    #obtener el comando para abrir la caja
    cmds = CmdBuilder.build_open_drawer()

    try:
      printer = win32print.OpenPrinter(printer_name) #configurar la impresora
      win32print.StartDocPrinter(printer, 1, ("Open Drawer", None, "RAW"))  #iniciar un trabajo de impresión en modo RAW (envío directo)
      win32print.WritePrinter(printer, cmds) #enviar el comando de abrir la caja
      
      #cerrar la conexion
      win32print.EndDocPrinter(printer)
      win32print.ClosePrinter(printer)

      return { 'ok': True }
      
    except Exception as e:
      return {
        'ok': False,
        'message': f'Error opening drawer: {e}'
      }
    