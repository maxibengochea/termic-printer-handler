import win32print
import win32ui

PRINTER_NAME = "IMP1"

def abrir_caja():
    try:
        # Abrir conexión con la impresora
        printer = win32print.OpenPrinter(PRINTER_NAME)
        hprinter = win32print.GetPrinter(printer, 2)

        # Crear un contexto de impresión
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(PRINTER_NAME)

        # Iniciar impresión
        pdc.StartDoc("Abrir caja registradora")
        pdc.StartPage()

        # Comando ESC/POS para abrir la caja registradora (impulso eléctrico)
        pdc.TextOut(0, 0, "\x1B\x70\x00\x19\xFA")  # ESC p 0 25 250 (prueba con este)

        # Finalizar impresión
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()

        win32print.ClosePrinter(printer)
        print("✅ ¡Caja registradora abierta!")

    except Exception as e:
        print(f"❌ Error al abrir la caja: {e}")

# Ejecutar la función
abrir_caja()
