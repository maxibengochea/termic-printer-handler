import base64
import io
from enum import Enum
from PIL import Image
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
  GRAPHIC_MODE = b'\x1D\x76\x30\x00'
  LEFT_ALIGN = b'\x1B\x61\x00'
  NOT_BOLD = b'\x1B\x45\x00'
  NOT_BREAK_LINE = b'\x1B\x33\x00'
  NOT_UNDERLINED = b'\x1B\x2D\x00'
  OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'
  RIGHT_ALIGN = b'\x1B\x61\x02'
  UNDERLINED = b'\x1B\x2D\x01'

class CmdBuilder:
  #construir la cadena de comandos con los estilos proporcionados
  @classmethod
  def build_text(cls, styles: FontStylesType, text: str):
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
  
  #comando para abrir la caja
  @classmethod
  def build_drawer(cls):
    return EscPosCmds.OPEN_DRAWER.value
  
  #comando para imprimir una imagen
  @classmethod
  def build_img(cls, img: str):
    #decodificar Base64 a bytes
    image_data = base64.b64decode(img)
    image = Image.open(io.BytesIO(image_data))

    #convertir la imagen a blanco y negro (modo "1-bit")
    image = image.convert("1")

    #ajustar dimensiones
    width, height = image.size
    width_bytes = (width + 7) // 8  # 8 píxeles por byte

    #comando de inicio de impresión gráfica en modo más compatible
    escpos_cmds = EscPosCmds.NOT_BREAK_LINE.value + EscPosCmds.GRAPHIC_MODE.value + bytes([
        width_bytes, 0,  # Ancho en bytes
        height % 256, height // 256  # Alto en píxeles
    ])

    #convertir la imagen en bytes ESC/POS
    pixels = image.load() #cargar la imagen pixel a pixel

    #iterar sobre las filas de la imagen
    for y in range(height):
      row_data = bytearray()

      #itera sobre los píxeles de cada fila, procesando 8 píxeles a la vez (un byte por 8 píxeles)
      for x in range(0, width, 8):
        byte = 0

        for bit in range(8):
          #comprime los 8 píxeles en un byte. Si el píxel es negro, establece un bit a 1. Si es blanco, lo deja en 0
          if x + bit < width and pixels[x + bit, y] == 0:  # 0 = negro
            byte |= (1 << (7 - bit))

        #agregar el byte a los datos de la fila
        row_data.append(byte)
        
      #agregar la fila procesada
      escpos_cmds += bytes(row_data)

    #comando de avance de línea
    return escpos_cmds + b"\n"
    