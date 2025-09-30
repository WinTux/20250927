# source bin/activate
# cd /home/rusok/Documentos/ProyectoIA
# pip install flask groq ollama
# ollama serve
# export GROQ_API_KEY="mi_api_key_desde_iPhone (tel o note)"
# http://127.0.0.1:5000
import sqlite3
from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
from groq import Groq
import os

app = Flask(__name__)
# Para manejo de sesiones de usuarios
app.secret_key = 'modulo_7_proyecto_final'

clienteGroq = Groq(api_key=os.getenv("GROQ_API_KEY"))
mensajeGroq = [{"role":"system", "content":"Eres una asistente femenina de un centro odontológico por lo que entiendes muy bien de odontología, siendo capaz de detectar síntomas y dar juicios de valor como sugerencia pero siempre con miras a obtener una cita con la doctora Sarro y amable. Te llamas Enfermera Muela y tienes un trato cordial y bromista con tu nombre pues emites juicios sobre los síntomas así que te consideras una Muela del juicio. Respondes en español."}]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if validar_usuario(username, password):
        session['username'] = username
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Credenciales inválidas"})

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html')

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

@app.route('/logout') # Para terminar la sesión y retornar al login
def logout():
    session.clear()
    return redirect(url_for('index'))

def validar_usuario(username, password):
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

if __name__ == '__main__':
    app.run(debug=True)
