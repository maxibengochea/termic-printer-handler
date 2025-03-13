from enum import Enum
from src.services.img_processor import base64_to_escpos_image
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
  OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'
  RESET = b'\x1B\x40'
  RIGHT_ALIGN = b'\x1B\x61\x02'
  UNDERLINED = b'\x1B\x2D\x01'

class CmdBuilder:
  #construir la cadena de comandos con los estilos proporcionados
  @classmethod
  def build_text(cls, styles: FontStylesType, text: str):
    #comenzar código ESC/POS
    escpos_cmds = EscPosCmds.RESET.value 

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
  
    escpos_cmds += EscPosCmds.BOLD.value if 'bold' in styles.keys() and styles['bold'] else b'' #estilar la negrita
    escpos_cmds += EscPosCmds.UNDERLINED.value if 'underlined' in styles.keys() and styles['underlined'] else b'' #estilar el subrayado
    escpos_cmds += text.encode('utf-8') #codificar el texto
    return escpos_cmds
  
  #comando para abrir la caja
  @classmethod
  def build_open_drawer(cls):
    return EscPosCmds.OPEN_DRAWER.value
  
  #comando para imprimir una imagen
  @classmethod
  def build_img(cls, img: str, alignment: str):
    #resetear la impresora
    escpos_cmds = EscPosCmds.RESET.value

    #configurar la alineacion de la imagen
    if alignment == "right":
      escpos_cmds += EscPosCmds.RIGHT_ALIGN.value

    elif alignment == "left":
      escpos_cmds += EscPosCmds.LEFT_ALIGN.value

    else:
      escpos_cmds += EscPosCmds.CENTER_ALIGN.value

    #agregar el modo grafico
    escpos_cmds += EscPosCmds.GRAPHIC_MODE.value 

    #decodificar base64 a bytes
    #el segundo parametro depende de la impresora, el otro valor seria 576
    img_data = base64_to_escpos_image(img, 384) 

    #comando de avance de línea
    return escpos_cmds + img_data + b'\n'
    