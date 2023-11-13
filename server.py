from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message  # Importa las extensiones necesarias
import sqlite3
from mailjet import send_email

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos SQLite
DATABASE = 'dbcontacto.db'

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Puerto para el servidor de correo
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'notificacioncontactanos@gmail.com'
app.config['MAIL_PASSWORD'] = 'kzac oszw ytxv poub'
app.config['MAIL_DEFAULT_SENDER'] = 'notificacioncontactanos@gmail.com' 

mail = Mail(app)

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            telefono TEXT,
            mensaje TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/enviarMensaje', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    mensaje = data.get('mensaje')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO contactos (nombre, correo, telefono, mensaje)
            VALUES (?, ?, ?, ?)
        ''', (nombre, correo, telefono, mensaje))
        conn.commit()

        enviar_correo_confirmacion(correo)
        send_email(correo)

        result = {'message': 'Mensaje enviado correctamente'}
    except Exception as e:
        print(e)
        result = {'message': 'Error al enviar el mensaje'}

    conn.close()

    return jsonify(result)

def enviar_correo_confirmacion(destinatario):
    cuerpo_html = render_template('confirmacion.html')
    mensaje = Message('Confirmación de Contacto', recipients=[destinatario])
    mensaje.body = '¡Gracias por Contactarnos! Tu mensaje ha sido recibido correctamente. Nos comunicaremos contigo lo más pronto posible'
    mensaje.html = cuerpo_html

    try:
        mail.send(mensaje)
        print(f'Correo de confirmación enviado a {destinatario}')
    except Exception as e:
        print(f'Error al enviar el correo de confirmación a {destinatario}: {e}')

if __name__ == '__main__':
    app.run(debug=True)