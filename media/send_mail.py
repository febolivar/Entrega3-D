""" Send email for processed images module
    2019-11: Updating to SendGrid
"""

# Email server and email mimes

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from datetime import datetime

# Global variables

PROJECT_EMAIL = "grupo06proyectos@gmail.com"
SUBJECT = "Diseño [%s] disponible"


def send_email(password, send_to, name, design_name, enterprise_url='', image_proc_url=''):
    """ Function to send a processed design notification """
    print("{} \t Inicia envío de correo electrónico".format(datetime.now()))

    email_subject = (SUBJECT % design_name)

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

    message = Mail(
        from_email=PROJECT_EMAIL,
        to_emails=send_to,
        subject=email_subject,
        html_content=html_message
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print("{} \t Notificación vía correo electrónico enviada".format(datetime.now()))
    except Exception as e:
        print("{} \t Error durante envío de correo".format(datetime.now()))
        print(e.message)
