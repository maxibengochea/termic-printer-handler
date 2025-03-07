import win32print
import win32ui
import win32con
from enum import Enum

PRINTER_NAME = "IMP1"

def imprimir_texto_estilizado(texto, fuente="Arial", tamano=24, negrita=True, alineacion="izquierda"):
    # Abrir la impresora
    printer = win32print.OpenPrinter(PRINTER_NAME)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(PRINTER_NAME)
    
    # Iniciar documento
    pdc.StartDoc("Documento con Estilos")
    pdc.StartPage()

    # Definir grosor de negrita (700 = negrita, 400 = normal)
    peso_negrita = 700 if negrita else 400

    # Crear fuente personalizada
    font = win32ui.CreateFont({
        "name": fuente,
        "height": tamano,
        "weight": peso_negrita,
    })
    
    pdc.SelectObject(font)  # Aplicar fuente

    # Configurar alineación
    if alineacion == "derecha":
        pdc.SetTextAlign(win32con.TA_RIGHT)
        x = 400  # Ajusta según tamaño del papel
    elif alineacion == "centro":
        pdc.SetTextAlign(win32con.TA_CENTER)
        x = 200
    else:  # Izquierda (por defecto)
        pdc.SetTextAlign(win32con.TA_LEFT)
        x = 100

    # Imprimir texto
    pdc.TextOut(x, 100, texto)

    # Finalizar impresión
    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()
    win32print.ClosePrinter(printer)

# Prueba de impresión con estilo
#imprimir_texto_estilizado("Texto en Arial, 24px, Negrita", "Arial", 24, True, "centro")

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

print(FontStyles.BOLD.value)