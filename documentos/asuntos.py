from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash, session, g
)
from documentos.auth import login_required
from .models import Asuntos, Usuarios, Secretarias, Estatus_asuntos
from . import db
from datetime import date

bp = Blueprint('asuntos',__name__,url_prefix='/asuntos')


@bp.route('/index')
@login_required
def index():
    asuntos = Asuntos.query.all()
    return render_template('asuntos/index.html', asuntos = asuntos)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        asunto = request.form['asunto']
        empleado = request.form['empleado']
        fecha = request.form['fecha']
        secretaria = request.form['secretaria']
        usuario = g.user.id
        estatus = request.form['estatus']
        
        asunto = Asuntos(asunto,empleado,fecha,secretaria,usuario,estatus)
        
        db.session.add(asunto)
        db.session.commit()
        return redirect(url_for('asuntos.index'))
    return render_template('asuntos/create.html', c_date = date.today())


def get_asunto(id):
    asunto = Asuntos.query.get_or_404(id)
    return asunto

@bp.route('/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    asunto = get_asunto(id)
    secre = Secretarias.query.filter_by(id = asunto.secretaria).first()
    estatus = Estatus_asuntos.query.all()
    estat = Estatus_asuntos.query.filter_by(id = asunto.estatus).first()
    
    if request.method == 'POST':
        asunto.asunto = request.form['asunto']
        asunto.empleado = request.form['empleado']
        asunto.estatus = request.form['new_estatus']

        db.session.commit()
        return redirect(url_for('asuntos.index'))
    return render_template('asuntos/update.html', asunto = asunto, secre = secre, estatus = estatus, estat = estat)