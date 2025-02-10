from flask import Blueprint, render_template, redirect, request, url_for, g
from documentos.auth import login_required
from .models import Secretarias, Usuarios
from . import db

bp = Blueprint('srias',__name__,url_prefix='/srias')

@bp.route('/index')
@login_required
def index():
    srias = Secretarias.query.all()
    return render_template('srias/index.html', srias = srias)

def srias():
    srias = Secretarias.query.filter(Secretarias.id != 14)
    return render_template('auth/register.html', srias = srias)