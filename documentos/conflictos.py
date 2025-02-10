from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash, session, g
)
from documentos.auth import login_required
from .models import Conflictos, Secretarias, Estatus_asuntos, Asuntos_styc, Trabajadores, Pensionados
from . import db
from datetime import date

bp = Blueprint('conflictos',__name__,url_prefix='/conflictos')

@bp.route('/index')
@login_required
def index():
    #conflictos = Conflictos.query.all()
    contenedor = db.session.query(Conflictos, Asuntos_styc).join(Asuntos_styc)
    return render_template('conflictos/index.html', contenedor = contenedor)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    asuntos = Asuntos_styc.query.all()
    estatus = Estatus_asuntos.query.all()
    pensionados = Pensionados.get_pensionados()
    trabajadores = Trabajadores.get_trabajadores()
    if request.method == 'POST':
        folio = request.form['folio']
        secretaria = request.form['secretaria']
        asunto = request.form['asunto']
        empleado = request.form['trabajador']
        pensionado = request.form['pensionado']
        if (request.form.get('es_pen') != None):
            ispen = 1
        else:
            ispen = 0
        clausula_convenio = request.form['clausula']
        info_extra = request.form['info_extra']
        observaciones = request.form['observaciones']
        fecha = request.form['fecha']
        estatus = request.form['estatus']

        conflictos = Conflictos(folio,secretaria,asunto,empleado,pensionado,ispen,
                                clausula_convenio,info_extra,observaciones,fecha,estatus)

        db.session.add(conflictos)
        db.session.commit()
        return redirect(url_for('conflictos.index'))
    return render_template('conflictos/create.html', c_date = date.today(), asuntos = asuntos,
                           estatus = estatus, pens = pensionados, trabs = trabajadores)

@bp.route('/update/<int:folio>', methods=('GET','POST'))
@login_required
def update(folio):
    conf = Conflictos.query.get_or_404(folio)
    asuntos = Asuntos_styc.query.all()
    estatus = Estatus_asuntos.query.all()
    id_asunto = Conflictos.get_asuntoid_by_folio(folio)
    id_estatus = Conflictos.get_estatusid_by_folio(folio)
    id_sria = Conflictos.get_sriaid_by_folio(folio)
    sria = Secretarias.get_sria_by_id(id_sria)
    conflictos = Conflictos.query.get(folio)
    is_pen = Conflictos.get_ispen_by_folio(folio)
    if(is_pen == 0):
        num = Conflictos.get_numemp_by_folio(folio)
        nom = Trabajadores.get_trabajador_by_num(num) 
    else:
        pen = Conflictos.get_numpens_by_folio(folio)
        nom = Pensionados.get_pensionado_by_pension(pen)
    
    if request.method == 'POST':
        conf.clausula_convenio = request.form['clausula']
        conf.asunto = request.form['asunto']
        conf.info_extra = request.form['info']
        conf.observaciones = request.form['observaciones']
        conf.estatus = request.form['estatus']

        db.session.commit()
        return redirect(url_for('conflictos.index'))

    return render_template('conflictos/update.html',asuntos = asuntos,estatus = estatus,asuntoid = id_asunto,
                           estatusid = id_estatus, conflicto = conflictos,sria = sria,n = nom)

@bp.route('/details/<int:folio>', methods=('GET','POST'))
@login_required
def details(folio):
    conflicto = Conflictos.query.get(folio)
    id_sria = Conflictos.get_sriaid_by_folio(folio)
    sria = Secretarias.get_sria_by_id(id_sria)
    is_pen = Conflictos.get_ispen_by_folio(folio)
    idasunto = Conflictos.get_asuntoid_by_folio(folio)
    if(is_pen == 0):
        num = Conflictos.get_numemp_by_folio(folio)
        nombre = Trabajadores.get_trabajador_by_num(num)
    else:
        num = Conflictos.get_numpens_by_folio(folio)
        nombre = Pensionados.get_pensionado_by_pension(num)
    asunto = Asuntos_styc.get_asunto_by_id(idasunto)

    return render_template('conflictos/details.html',conflicto = conflicto, asunto = asunto, sria = sria, nombre = nombre)

#### OBTENER ASUNTO DE CONFLICTOS ####
def get_asunto_styc(id):
    asunto = Asuntos_styc.get_asunto_by_id(id)
    return asunto