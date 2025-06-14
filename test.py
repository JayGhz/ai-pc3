# -*- coding: utf-8 -*-
from naoqi import ALProxy
import requests
import base64
import time
import os

NAO_IP = "127.0.0.1"
PORT = 54013
SERVER_IP = "http://192.168.18.6:5000/emocion"

tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
audioplayer = ALProxy("ALAudioPlayer", NAO_IP, PORT)

img_folder = "public/emotions"
img_files = ["happy.jpg", "sad.jpg", "angry.jpg", "neutral.jpg"]

def procesar_emocion(path_img):
    with open(path_img, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    response = requests.post(SERVER_IP, json={"imagen": img_b64})
    emocion = response.json().get("emocion", "neutral")
    return emocion

def reaccionar(emocion):
    if emocion == "happy":
        tts.say("¡Qué bueno que estás feliz! Vamos a escuchar algo de música.")
        # music_path = "/home/nao/music/Danny-Ocean-Volare.wav"
        audioplayer.playFile(music_path)
    elif emocion == "sad":
        tts.say("Veo que estás triste. ¿Puedo ayudarte?")
    elif emocion == "angry":
        tts.say("No te enojes. Respira profundo conmigo.")
    else:
        tts.say("Detecto que estás {}.".format(emocion))

for img_name in img_files:
    path = os.path.join(img_folder, img_name)
    print("Procesando:", path)
    emocion = procesar_emocion(path)
    print("Emoción detectada:", emocion)
    reaccionar(emocion)
    time.sleep(5)
