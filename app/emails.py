from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
"""
def confirmacion_compra(mail, usuario, libro):
    try:
        message = Message('Confirmación de compra de libro',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=['20213tn063@utez.edu.mx'])
        message.html = render_template(
            'emails/confirmacion_compra.html', usuario=usuario, libro=libro)
        mail.send(message)
    except Exception as ex:
        raise Exception(ex)
"""

def confirmacion_compra(app, mail, usuario, libro):
    try:

        message = Message('Confirmación de compra de libro',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=['20213tn113@utez.edu.mx'])
        message.html = render_template(
            'emails/confirmacion_compra.html', usuario=usuario, libro=libro)
        thread = Thread(target=envio_email_async, args=[app, mail, message])
        
        thread.start()
    except Exception as ex:
        raise Exception(ex)
    

def confirmacion_compraU(app, mail, usuario, libro, correo):
    try:

        message = Message('Confirmación de compra de libro',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[correo])
        message.html = render_template(
            'emails/confirmacion_compra.html', usuario=usuario, libro=libro)
        thread = Thread(target=envio_email_async, args=[app, mail, message])
        thread.start()
    except Exception as ex:
        raise Exception(ex)
    

def confirmacion_registro(app, mail, usuario, libro, correo):
    try:
        message = Message('Confirmación de su registro exitoso',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[correo])
        usuario1 = usuario
        print("EL usuario: ", usuario1)
        message.html = render_template(
            'emails/confirmacion_compra.html', usuario1=usuario1, libro=libro)
        
        thread = Thread(target=envio_email_async, args=[app, mail, message])
        thread.start()
    except Exception as ex:
        raise Exception(ex)



def envio_email_async(app, mail, message):
    with app.app_context():
        mail.send(message)