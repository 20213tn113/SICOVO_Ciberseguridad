from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail

from .models.ModeloCompra import ModeloCompra
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario

from .models.entities.Compra import Compra
from .models.entities.Libro import Libro
from .models.entities.Usuario import Usuario

from .consts import *
from .emails import confirmacion_compra, confirmacion_compraU, confirmacion_registro

from flask import Flask, request, redirect, url_for, flash, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail()

def contains_unsafe_characters(value):
    unsafe_chars = ["'", '"', ";", "--", "#"]
    return any(char in value for char in unsafe_chars)


@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db,id)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/login', methods=['GET','POST'])
def login():
    data_request = request.get_json()

     
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        # usuario = request.args.get('usuario')
        # password = request.args.get('password')
        
        # if contains_unsafe_characters(usuario) or contains_unsafe_characters(password):
        #     flash("Error: La entrada contiene caracteres no permitidos.", 'danger')
        #     # flash(MENSAJE_SIGNOS, 'warning')
        #     return render_template('auth/login.html')
        
        usuario_obj = Usuario(None, usuario, password, None, None, None, None, None)
        usuario_logeado = ModeloUsuario.login(db, usuario_obj)
        if usuario_logeado != None:
            login_user(usuario_logeado)
            flash(MENSAJE_BIENVENIDA, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS, 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/login2')
def login2():
    usuario = request.args.get('usuario')
    password = request.args.get('password')
    print("Llego")
    print("usuario: ", usuario)
    print("contraseña: ",password)

    usuario_obj = Usuario(None, usuario, password, None, None, None, None, None)
    usuario_logeado = ModeloUsuario.login(db, usuario_obj)
    if usuario_logeado != None:
        login_user(usuario_logeado)
        flash(MENSAJE_BIENVENIDA, 'success')
        return redirect(url_for('index'))
    else:
        flash(LOGIN_CREDENCIALESINVALIDAS, 'warning')
        return render_template('auth/login.html')
    

@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

@app.route('/bienvenida')
def bienvenida():
    return render_template('auth/bienvenida.html')

@app.route('/registroExitoso')
def registroExitoso():
    flash(MENSAJE_REGISTRADO, 'success')
    return redirect(url_for('login'))

@app.route('/registroUsuario')
def registroUsuario():
    return render_template('auth/registro_usuario.html')

    
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    data_request = request.get_json()
    data = {}
    try:
        nombre =  data_request['nombre']
        apellido =  data_request['apellido']
        nombre_completo = nombre + ' ' + apellido
        usuario = Usuario(
            None,  data_request['usuario'],  data_request['password'], nombre_completo,  data_request['domicilio'],  data_request['correo'],  data_request['telefono'], 2)
        usuario_creado = ModeloUsuario.registrar_usuario(db, usuario)
        data['exito'] = usuario_creado
        libro = None
        confirmacion_registro(app,mail,usuario.usuario,libro,usuario.correo)
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                data = {
                    'titulo':'Libros Vendidos',
                    'libros_vendidos':libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html',mensaje=format(ex))
        else:
            try:
                compras=ModeloCompra.listar_compras_usuario(db, current_user)
                data = {
                    'titulo':'Mis compras',
                    'compras':compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html',mensaje=format(ex))
    else:
        return redirect(url_for('login'))


@app.route('/libros')
# @login_required
def listar_libros():
    try:
        libros = ModeloLibro.listar_libros(db)
        data={
            'titulo': 'Listado de libros',
            'libros': libros
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        return render_template('errores/error.html',mensaje=format(ex))

@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()

    data = {}
    try:
        #libro = Libro(data_request['isbn'], None, None, None, None)
        libro = ModeloLibro.leer_libro(db, data_request['isbn'])
        compra = Compra(None, libro, current_user)
        data['exito'] = ModeloCompra.registrar_compra(db, compra)
        correo = ModeloUsuario.obtener_gmail(db,current_user.id)

        # confirmacion_compra(mail, current_user, libro) #ENVIO NORMAL
        #confirmacion_compra(app, mail, current_user, libro) #ENVIO ASINCRONO
        confirmacion_compraU(app,mail,current_user,libro,correo)

    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)

def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def pagina_no_autorizada(error):
    return redirect(url_for('login'))

def inicializar_app(config):
    app.config.from_object(config)
    # csrf.init_app(app)
    mail.init_app(app)
    app.register_error_handler(401, pagina_no_autorizada)
    app.register_error_handler(404, pagina_no_encontrada)
    return app



@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Pasar la ruta de la imagen al template
        message = f"Imagen subida con éxito. Ruta: {filepath}"
        return render_template('auth/upload.html', message=message)

@app.route('/upload')
def upload():
    return render_template('auth/upload.html')