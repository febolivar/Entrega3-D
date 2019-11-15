""" Send email for processed images module
"""

# Email server and email mimes
import os
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

# Global variables

PORT = 465
SERVICE = os.getenv('AWS_EMAIL_SERVICE')
PROJECT_EMAIL = os.getenv('AWS_EMAIL_EMAIL')
SUBJECT = "Diseño [%s] disponible"


def send_email(password, send_to, name, design_name, enterprise_url = '', image_proc_url = ''):
    """ Function to send a processed design notification """
    # print("{} \t Inicia envío de correo electrónico".format(datetime.now()))
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        SERVICE,
        port = PORT,
        context = context) as server:
        
        #server.starttls()
        server.login(PROJECT_EMAIL,password)

        message = MIMEMultipart("alternative")
        message['Subject'] = (SUBJECT % design_name)
        message['From'] = send_to
        message['To'] = send_to

        html_message = ((
                            '<html>'
                            '<body>'
                            '    <h2 style="color:#367fa9; font-family: Calibri">Notificación de Proyecto1</h2>'
                            '    <h3 style="color:#367fa9; font-family: Calibri">Procesamiento de diseños</h3>'
                            '    <br />'
                            '    <p style="font-family: Calibri">'
                            'Hola, %s'
                            '    </p>'
                            '    <p style="font-family: Calibri">'
                            'Tu diseño <b>%s</b> ha sido procesado con éxito y se encuentra disponible para ser visualizado en nuestra plataforma.'
                            '    </p>'
                            '    <p style="font-family: Calibri">'
                            'En el siguiente enlace podrás visualizar tu diseño:'
                            '    </p>'
                            '    <br / >'
                            '   <a href="%s" target="_blank" style="font-family: Calibri">'
                            '       %s'
                            '   </a>'
                            '    <br / >'
                            '    <br / >'
                            '    <p style="font-family: Calibri">'
                            'En el siguiente enlace podrás descargar tu imagen procesada:'
                            '    </p>'
                            '    <br / >'
                            '   <a href="%s" target="_blank" style="font-family: Calibri">'
                            '       %s'
                            '   </a>'
                            '    <br / >'
                            '    <br / >'
                            '    <p style="color:#367fa9; font-family: Calibri">Nota: </p> <p style="font-family: Calibri"> Este es un correo automático, por favor no respondas a este mensaje.</p>'
                            '</body>'
                            '</html>'
                        ) % (name, design_name, enterprise_url, enterprise_url, image_proc_url, image_proc_url))

        email_part = MIMEText(html_message, "html")

        message.attach(email_part)

        server.sendmail(send_to, send_to, message.as_string())

        # print("{} \t Notificación vía correo electrónico enviada".format(datetime.now()))
