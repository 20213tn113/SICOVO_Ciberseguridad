from flask_script import Manager, Server
from app import inicializar_app
from config import config

configuracion=config['development']
app= inicializar_app(configuracion)

manager= Manager(app)
manager.add_command('runserver',Server(host='192.168.x.x',port=5000))

if __name__ == '__main__':
    manager.run()