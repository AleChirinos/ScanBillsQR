from tkinter import *
import cv2
import pandas as pd
import numpy as np
from pyzbar import pyzbar
import csv
from playsound import playsound

def dataConc(data):
    data = data.split("|")
    print(data)
    nit = data[0]
    factura = data[1]
    autorizacion = data[2]
    fecha_emision = data[3]
    total = data[4]
    codigo_control = data[5]
    nit_cliente = data[6]
    valor_nulo1 = data[7]
    valor_nulo2 = data[8]
    valor_nulo3 = data[9]
    valor_nulo4 = data[10]

    row = [nit, factura, autorizacion, fecha_emision, total, codigo_control, nit_cliente, valor_nulo1, valor_nulo2, valor_nulo3, valor_nulo4]

    return row



def read_barcodes(frame, current_val):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info,
                    (x + 6, y - 6), font,
                    2.0, (255, 255, 255), 1
                    )
        # playsound('sonido.mp3')
        # 3
        if not (barcode_info == current_val):
            current_df = barcode_info
            current_val = barcode_info
            result = dataConc(barcode_info)
            df = np.array([result])
            with open("facturasQR1.csv", mode = 'a') as f:
                pd.DataFrame(df).to_csv(f, header=f.tell()==0)
    return frame


def main1():
    # 1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    current_df = ""
    # 2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame, current_df)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # 3
    camera.release()
    cv2.destroyAllWindows()


# 4
# if __name__ == '__main__':
#     main()

def eliminarDuplicados():
    df=pd.read_csv('facturasQR1.csv',
                 skiprows = 1,
                 names=['Num', 'Nit_empresa', 'Numero_factura', 'Numero_autorizacion', 'Fecha', 'Monto', 'Monto2', 'Codigo', 'Nit_usuario', 'Valor_nulo', 'Valor_nulo2', 'Valor_nulo3'])

    eliminarDuplicados = df.drop_duplicates()
    print(eliminarDuplicados)

    eliminarDuplicados.to_csv('fixDuplicates.csv')


raiz= Tk()
raiz.title("ProyectoFinal - Facturacion por QR")
# raiz.config(bg="black")

bienvenida = Label(raiz, text="Bienvenido", width=25)
bienvenida.grid(column=0, row=0, padx=0, pady=0)

paso1 = Label(raiz, text="Paso 1: Debes apretar el boton para poder escanear el codigo QR de todas las facturas que quieras", width=75)
paso1.grid(column=0, row=2, padx=0, pady=0)

paso2 = Label(raiz, text="Paso 2: Debes apretar el boton para que pueda generar un archivo csv sin facturas repetidas", width=75)
paso2.grid(column=0, row=3, padx=0, pady=0)

btn = Button(raiz, text= "Escanear el codigo", width=25, command=main1)
btn.grid(column=0, row=4, padx=0, pady=0)

btn2 = Button(raiz, text= "Eliminar duplicados", width=25, command=eliminarDuplicados)
btn2.grid(column=0, row=5, padx=0, pady=0)
# Necesita ser un bucle infinito para que este abierta la ventana
raiz.mainloop()