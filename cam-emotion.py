import cv2
import base64
import requests
import os

SERVER_URL = "http://192.168.18.6:5000/emocion"
SENAL_PATH = "nueva_emocion.txt"  # Señal para test.py

def capturar():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("No se pudo abrir la cámara.")
        return

    print("Presiona ESPACIO para capturar imagen, o ESC para salir.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al capturar imagen.")
            break

        cv2.imshow("Preview - Presiona ESPACIO para capturar", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            print("Cancelado por el usuario.")
            break
        elif key == 32:
            print("Imagen capturada, enviando al servidor...")
            enviar_al_servidor(frame)
            break

    cam.release()
    cv2.destroyAllWindows()

def enviar_al_servidor(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    img_b64 = base64.b64encode(buffer).decode("utf-8")

    try:
        response = requests.post(SERVER_URL, json={"imagen": img_b64})
        if response.status_code == 200:
            emocion = response.json().get("emocion")
            print("Emoción detectada:", emocion)
            # Creamos el archivo de señal
            if emocion:
                with open(SENAL_PATH, "w") as f:
                    f.write("1")
        else:
            print("Error del servidor:", response.text)
    except Exception as e:
        print("Error al conectar con el servidor:", e)

if __name__ == "__main__":
    capturar()
