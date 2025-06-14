from flask import Flask, request, jsonify
from deepface import DeepFace
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)

ultima_emocion = None

@app.route("/emocion", methods=["POST"])
def detectar_emocion():
    global ultima_emocion

    data = request.json
    img_b64 = data["imagen"]
    img = Image.open(io.BytesIO(base64.b64decode(img_b64)))
    img = np.array(img)

    try:
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        emocion = result[0]["dominant_emotion"]
        ultima_emocion = emocion  # Se actualiza aquí
        return jsonify({"emocion": emocion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/emocion", methods=["GET"])
def obtener_emocion():
    return jsonify({"emocion": ultima_emocion})

app.run(host="0.0.0.0", port=5000)
