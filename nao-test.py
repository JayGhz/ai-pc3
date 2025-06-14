# -*- coding: utf-8 -*-
from naoqi import ALProxy
import requests
import base64
import time
import cv2
import numpy as np

NAO_IP = "127.0.0.1"
PORT = 65226
SERVER_IP = "http://172.20.10.2:5000/emocion"

tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
video = ALProxy("ALVideoDevice", NAO_IP, PORT)

# Suscribirse a la cámara del NAO
resolution = 2    # VGA (640x480)
colorSpace = 11   # RGB
fps = 5
nameId = "nao_camera"
captureDevice = video.subscribeCamera(nameId, 0, resolution, colorSpace, fps)

def capturar_imagen():
    # Obtener frame desde NAO
    naoImage = video.getImageRemote(nameId)
    if naoImage is None:
        print("Error: no se pudo capturar imagen")
        return None

    width = naoImage[0]
    height = naoImage[1]
    array = naoImage[6]
    img = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

    # Codificar como JPEG y luego base64
    _, buffer = cv2.imencode('.jpg', img)
    img_b64 = base64.b64encode(buffer.tobytes()).decode("utf-8")
    return img_b64

def procesar_emocion(img_b64):
    response = requests.post(SERVER_IP, json={"imagen": img_b64})
    emocion = response.json().get("emocion", "neutral")
    return emocion

def reaccionar(emocion):
    if emocion == "happy":
        tts.say("¡Qué bueno que estás feliz!")
    elif emocion == "sad":
        tts.say("Veo que estás triste. ¿Puedo ayudarte?")
    elif emocion == "angry":
        tts.say("No te enojes. Respira profundo conmigo.")
    else:
        tts.say("Detecto que estás {}.".format(emocion))

for _ in range(3):
    print("Capturando imagen desde la cámara del NAO...")
    img_b64 = capturar_imagen()
    if img_b64:
        emocion = procesar_emocion(img_b64)
        print("Emoción detectada:", emocion)
        reaccionar(emocion)
    time.sleep(5)

# Liberar cámara
video.unsubscribe(nameId)
