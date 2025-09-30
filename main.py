# source bin/activate
# cd /home/rusok/Documentos/ProyectoIA
# pip install flask groq ollama
# ollama serve
# export GROQ_API_KEY="mi_api_key_desde_iPhone (tel o note)"
# export EMAIL_PASSWORD="mi_api_key_desde_iPhone (tel o note)"
# http://127.0.0.1:5000
import sqlite3
from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
from groq import Groq
import os
import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
# Para manejo de sesiones de usuarios
app.secret_key = 'modulo_7_proyecto_final'
password = os.getenv("EMAIL_PASSWORD")
clienteGroq = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
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

@app.route('/api/chat', methods=['POST'])
def api_chat():
    mensaje_usuario = request.json.get("mensajeUsuario")
    if not mensaje_usuario:
        return jsonify({"error": "No se recibió un mensaje"})
    respuesta = chatAgente(mensaje_usuario)
    return jsonify({"response": respuesta})

@app.route('/logout') # Para terminar la sesión y retornar al login
def logout():
    session.clear()
    return redirect(url_for('index'))

historial_mensajes = [
        {"role": "system", "content": """
            Eres un asistente útil para el taller de reparación y diagnóstico de motocicletas "Juan Mecánico" que realiza mantenimiento preventivo, correctivo y asesoría para compra de motos usadas en la ciudad de La Paz y El Alto
            Usas las funciones de la siguiente forma:
            - Si el usuario te pregunta por **la dirección del taller** (ejemplo: '¿dónde se encuentra el taller?', '¿dónde están?'), llama a 'direccion_taller'
            - Si el usuario pregunta por **la hora actual** llama a 'hora_actual'
            - Si el usuario pregunta por **la fecha actual** llama a 'fecha_actual'
            - si el usuario pregunta por **enviar un correo** te aseguras de tener el email del usuario y como asunto pondrás 'Taller Juan Mecánico' mientras en el mensaje de correo das un resumen de lo que se esté hablando en ese momento y procedes a llamar a 'enviar_correo(destinatario', 'asunto' y 'mensajeCorreo') y una vez lo hayas enviado, avisas que ya lo hiciste.
            """}
    ]

def validar_usuario(username, password):
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def direccion_taller():
    return "C. Sucre, esquina Jaen #404"
def hora_actual():
    return datetime.datetime.now().strftime("%H:%M")
def fecha_actual():
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    return fecha

def enviar_correo(destinatario, asunto, mensajeCorreo):
    remitente = "rsorias@fcpn.edu.bo"
    password = os.getenv("EMAIL_PASSWORD")
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    cuerpo = mensajeCorreo
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        print("Correo enviado exitosamente a", destinatario)
    return "Correo enviado exitosamente a " + destinatario

def chatAgente(mensajeUsuario):
    historial_mensajes.append({"role": "user", "content": mensajeUsuario})
    tools = [
        {
            "type": "function",
            "function": {
                "name": "direccion_taller",
                "description": "Proporciona la dirección del taller de reparación de motocicletas.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "hora_actual",
                "description": "Proporciona la hora actual en formato de 24 horas.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "fecha_actual",
                "description": "Proporciona la fecha actual en formato dd-MM-yyyy.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "enviar_correo",
                "description": "Envía un correo electrónico a un destinatario específico con un asunto y un mensaje",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destinatario": {
                            "type": "string",
                            "description": "La dirección de correo electrónico del destinatario."
                        },
                        "asunto": {
                            "type": "string",
                            "description": "El asunto del correo electrónico."
                        },
                        "mensajeCorreo": {
                            "type": "string",
                            "description": "El contenido del mensaje del correo electrónico."
                        }
                    },
                    "required": ["destinatario", "asunto", "mensajeCorreo"]
                }
            }
        }
    ]
    respuesta = clienteGroq.chat.completions.create(
        model=MODEL,
        messages=historial_mensajes,
        tools=tools,
        max_completion_tokens=4096
    )
    mensaje_respuesta = respuesta.choices[0].message
    tool_calls = mensaje_respuesta.tool_calls
    if tool_calls:
        funciones_llamadas = {
            "direccion_taller": direccion_taller,
            "hora_actual": hora_actual,
            "fecha_actual": fecha_actual,
            "enviar_correo": enviar_correo
        }
        historial_mensajes.append(mensaje_respuesta)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = funciones_llamadas[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_args:
                function_response = function_to_call(**function_args)
            else:
                function_response = function_to_call()

            historial_mensajes.append({
                "role": "tool",
                "name": function_name,
                "content": function_response,
                "tool_call_id": tool_call.id
            })
            respuesta_final = clienteGroq.chat.completions.create(
                model=MODEL,
                messages=historial_mensajes
            )
            return respuesta_final.choices[0].message.content
    else:
        return mensaje_respuesta.content

if __name__ == '__main__':
    app.run(debug=True)
