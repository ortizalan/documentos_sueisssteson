from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash, session, g
    )
from werkzeug.security import generate_password_hash, check_password_hash
from . import models, db
from .models import Usuarios, Comites, Secretarias, Estatus_usuario
from .auth import login_required
import base64

bp = Blueprint('usuarios',__name__,url_prefix='/usuarios')

@login_required
@bp.route('/list')
def list():
    usuarios = Usuarios.query.all()
    return render_template('usuarios/index.html', usuarios = usuarios)