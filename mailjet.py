from mailjet_rest import Client
import os

def send_email(to_email):
    api_key = '2adddfa1a7eb9bc43b664bce069dadea'
    api_secret = '247ec3c807c8cc20d2139e81909093ae'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "notificacioncontactanos@gmail.com",
            "Name": "Selene"
        },
        "To": [
            {
            "Email": f"{to_email}",
            "Name": "Selene"
            }
        ],
        "Subject": "Gracias por contactarnos.",
        "TextPart": "Gracias por contactar a Selene",
        "HTMLPart": "<h1>Hola, gracias por comunicarte con Selene</h1> <h3>Nos comunicaremos contigo, lo más pronto posible</h3> <h4>Saludos</h4>",
        "CustomID": "Contactanos"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print (result.json())