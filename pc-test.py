# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import requests
import os

NAO_IP = "127.0.0.1"
PORT = 54013
SERVER_URL = "http://192.168.18.6:5000/emocion"
SENAL_PATH = "nueva_emocion.txt"

tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
audioplayer = ALProxy("ALAudioPlayer", NAO_IP, PORT)
motion = ALProxy("ALMotion", NAO_IP, PORT)
posture = ALProxy("ALRobotPosture", NAO_IP, PORT)

ultima_emocion = None


def bailar():
    posture.goToPosture("StandInit", 0.5)
    motion.setStiffnesses("Body", 1.0)

    # Inicio suave - levantar brazos lentamente
    motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [-0.2, -0.2], 0.1)
    time.sleep(2)

    # Balanceo elegante de brazos y torso
    for _ in range(2):
        motion.setAngles(
            ["LShoulderRoll", "RShoulderRoll", "LHipRoll", "RHipRoll"],
            [0.4, -0.4, 0.2, -0.2],
            0.15,
        )
        time.sleep(1)
        motion.setAngles(
            ["LShoulderRoll", "RShoulderRoll", "LHipRoll", "RHipRoll"],
            [-0.4, 0.4, -0.2, 0.2],
            0.15,
        )
        time.sleep(1)

    # Movimiento de caderas tipo vallenato (izq-der)
    for _ in range(3):
        motion.setAngles(["LHipRoll", "RHipRoll"], [0.3, -0.3], 0.2)
        time.sleep(0.6)
        motion.setAngles(["LHipRoll", "RHipRoll"], [-0.3, 0.3], 0.2)
        time.sleep(0.6)

    # Gesto romántico: brazos cruzados frente al pecho
    motion.setAngles(["LElbowRoll", "RElbowRoll"], [-1.0, 1.0], 0.2)
    time.sleep(1.5)

    # Movimiento de torso (giro leve de hombros y cabeza)
    for _ in range(2):
        motion.setAngles(
            ["HeadYaw", "LShoulderRoll", "RShoulderRoll"], [0.5, 0.2, -0.2], 0.2
        )
        time.sleep(0.8)
        motion.setAngles(
            ["HeadYaw", "LShoulderRoll", "RShoulderRoll"], [-0.5, -0.2, 0.2], 0.2
        )
        time.sleep(0.8)

    # Manos al aire en celebración
    motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [-1.3, -1.3], 0.2)
    motion.setAngles(["LElbowRoll", "RElbowRoll"], [-0.4, 0.4], 0.2)
    time.sleep(2)

    # Repetir la parte central (balanceo y caderas)
    for _ in range(2):
        motion.setAngles(
            ["LShoulderRoll", "RShoulderRoll", "LHipRoll", "RHipRoll"],
            [0.4, -0.4, 0.2, -0.2],
            0.15,
        )
        time.sleep(1)
        motion.setAngles(
            ["LShoulderRoll", "RShoulderRoll", "LHipRoll", "RHipRoll"],
            [-0.4, 0.4, -0.2, 0.2],
            0.15,
        )
        time.sleep(1)

        motion.setAngles(["LHipRoll", "RHipRoll"], [0.3, -0.3], 0.2)
        time.sleep(0.6)
        motion.setAngles(["LHipRoll", "RHipRoll"], [-0.3, 0.3], 0.2)
        time.sleep(0.6)

    motion.setAngles(
        ["LShoulderRoll", "RShoulderRoll", "HeadPitch"], [0.3, -0.3, -0.2], 0.15
    )
    time.sleep(1.2)

    posture.goToPosture("StandInit", 0.5)


def abrazar():
    # Activar postura inicial y rigidez
    posture.goToPosture("StandInit", 0.5)
    motion.setStiffnesses("Body", 1.0)

    # Paso corto hacia adelante para acercarse
    motion.moveInit()
    motion.moveTo(0.1, 0.0, 0.0)  # 10 cm hacia adelante
    time.sleep(1)

    # Abrir los brazos lentamente
    motion.setAngles(
        ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll"],
        [0.5, 0.5, -1.0, 1.0],
        0.1,
    )
    time.sleep(1.5)

    # Gesto de abrazo (cerrar ligeramente)
    motion.setAngles(
        ["LElbowYaw", "RElbowYaw", "LShoulderRoll", "RShoulderRoll"],
        [-1.2, 1.2, 0.4, -0.4],
        0.15,
    )
    time.sleep(2)

    # Cabeza hacia abajo ligeramente para dar empatía
    motion.setAngles("HeadPitch", 0.3, 0.1)
    tts.say("Todo estará bien, estoy contigo.")
    time.sleep(2)

    # Mantener el gesto un momento
    time.sleep(1.5)

    # Regresar los brazos primero para evitar movimientos raros
    motion.setAngles(
        ["LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll"],
        [0.0, 0.0, -0.5, 0.5],
        0.1,
    )
    time.sleep(1.2)

    # Volver postura estándar suavemente
    posture.goToPosture("StandInit", 0.8)

    # Retroceder a la posición original
    motion.moveTo(-0.1, 0.0, 0.0)  # volver 10 cm atrás
    time.sleep(1)

    

def reproducir_musica(music_path):
    audioplayer.playFile(music_path)


def reaccionar(emocion):
    if emocion == "happy":
        time.sleep(1)
        tts.say("Que bueno que estas feliz!, pongamos algo de musica")
        time.sleep(2)
        bailar()
    elif emocion == "sad":
        time.sleep(1)
        tts.say("Veo que estás triste. ¿Te puedo dar un abrazo?")
        time.sleep(1)
        abrazar()
    elif emocion == "angry":
        tts.say("No te enojes. Respira profundo conmigo.")
    else:
        tts.say("Detecto que estas {}.".format(emocion))


while True:
    try:
        if os.path.exists(SENAL_PATH):
            response = requests.get(SERVER_URL)
            emocion = response.json().get("emocion", "neutral")

            if emocion != ultima_emocion and emocion != "neutral":
                print("Nueva emocion detectada:", emocion)
                reaccionar(emocion)
                ultima_emocion = emocion
            else:
                print("Misma emocion detectada o neutral.")

            os.remove(SENAL_PATH)  # Borrar señal después de actuar
        else:
            print("Esperando nueva imagen...")

    except Exception as e:
        print("Error al obtener emocion:", e)

    time.sleep(2)
