from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash, session, g
    )

from werkzeug.security import generate_password_hash, check_password_hash
from . import models, db
from .models import Usuarios, Comites, Secretarias, Estatus_usuario
import base64


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        ap_pat = request.form['ap_paterno']
        ap_mat = request.form['ap_materno']
        secretaria = request.form['secretaria']
        usuario = request.form['usuario']
        password = base64.b64encode(request.form['password'].encode('utf-8'))
        comite = request.form['comite']
        estatus = request.form['estatus']

        user = Usuarios(nombres,ap_pat,ap_mat,secretaria,usuario,password,comite,estatus)
        error = None
        user_name = Usuarios.query.filter_by(usuario = usuario).first()
        
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El Usuario {usuario} ya existe en la Base de Datos.'
        
        flash(error)

    comites = Comites.query.all()
    secres = Secretarias.query.all()
    est_usr = Estatus_usuario.query.all()

    return render_template('auth/register.html', comites = comites, secres = secres, est_usr = est_usr)

@bp.route('/login', methods = ('GET','POST'))
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        password = base64.b64encode(request.form['password'].encode('ascii'))

        error = None
        usrId = 0

        # Validar los datos
        User = Usuarios.query.filter_by(usuario = usuario).first()
        
        # if User != None:
        #     bd_pass = base64.b64decode(User.password).decode('ascii')
        #     frm_pass = base64.b64decode(password).decode('ascii')
        
        if User == None:
            error = 'Nombre de Usuario Incorrecto.'
        #elif not check_password_hash( str(bd_pass), str(frm_pass)):
        elif base64.b64decode(User.password).decode('ascii') != base64.b64decode(password).decode('ascii'):
            #valor = User.password == password.decode('ascii')
            error = 'Contraseña Incorrecta.'
        else:
            usrId = User.id
        
        # Iniciar Sesión
        if error == None:
            session.clear()
            session['user_id'] = usrId
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id == None:
        g.user = None
    else:
        g.user = Usuarios.query.get_or_404(user_id)
        #g.user.usuario = g.user.usuario
        #enc =  g.user.usuario.rstrip('=')
        #g.user.usuario = base64.b64decode(enc + '=' * (-len(enc) % 4))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




@bp.route('/index')
def index():
    usuarios = Usuarios.query.all()
    return render_template('auth/index.html', usuarios = usuarios)



import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view