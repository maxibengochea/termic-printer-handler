import base64
from PIL import Image
from io import BytesIO

#convertir una imagen en base 64 a formato ESC/POS
def base64_to_escpos_image(img: str, max_width: int):
  #decodificar Base64 a bytes
  image_data = base64.b64decode(img.strip())
  image = Image.open(BytesIO(image_data))

  #convertir la imagen a blanco y negro (modo "1-bit")
  image = image.convert("1")

  #ajustar el ancho para que no exceda max_width y sea múltiplo de 8
  width, height = image.size

  if width > max_width:
      new_width = (max_width // 8) * 8  #asegurar múltiplo de 8
      new_height = int((new_width / width) * height)  #mantener proporción
      image = image.resize((new_width, new_height), Image.LANCZOS)

  else:
    new_width = (width // 8) * 8  #asegurar múltiplo de 8
    new_height = height

  width, height = image.size
  width_bytes = width // 8  # Convertir píxeles a bytes (8 píxeles por byte)

  #crear los datos 
  image_bytes = bytearray()
  image_bytes.append(width_bytes % 256)  # Ancho en bytes (LSB)
  image_bytes.append(width_bytes // 256)  # Ancho en bytes (MSB)
  image_bytes.append(height % 256)  # Alto en píxeles (LSB)
  image_bytes.append(height // 256)  # Alto en píxeles (MSB)

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
    image_bytes.extend(row_data)

  return image_bytes
