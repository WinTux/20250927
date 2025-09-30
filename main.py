# source bin/activate
# cd /home/rusok/Documentos/ProyectoIA
# pip install flask groq ollama
# ollama serve
# export GROQ_API_KEY="mi_api_key_desde_iPhone (tel o note)"
# http://127.0.0.1:5000
from flask import Flask, render_template, request, jsonify, Response
from groq import Groq
import os

clienteGroq = Groq(api_key=os.getenv("GROQ_API_KEY"))
mensajeGroq = [{"role":"system", "content":"Eres una asistente femenina de un centro odontológico por lo que entiendes muy bien de odontología, siendo capaz de detectar síntomas y dar juicios de valor como sugerencia pero siempre con miras a obtener una cita con la doctora Sarro y amable. Te llamas Enfermera Muela y tienes un trato cordial y bromista con tu nombre pues emites juicios sobre los síntomas así que te consideras una Muela del juicio. Respondes en español."}]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/consulta', methods=['GET'])
def chateandoGroq():
    return render_template('consulta.html')

@app.route('/consulta', methods=['POST'])
def chateandoGroqAPI():
    mensaje_usuario = request.json.get("mensajeUsuario")
    print(mensaje_usuario)
    if not mensaje_usuario:
        return jsonify({"error":"No se recibio un mensaje"})

    mensajeGroq.append({"role":"user", "content":mensaje_usuario})

    respuesta = clienteGroq.chat.completions.create(
        model="gemma2-9b-it",
        messages=mensajeGroq    
    )

    respuesta_texto = respuesta.choices[0].message.content
    mensajeGroq.append({"role":"assistant", "content":respuesta_texto})

    return jsonify({"mensajeBot":respuesta_texto})

if __name__ == '__main__':
    app.run(debug=True)
