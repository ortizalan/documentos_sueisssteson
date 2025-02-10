from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash, session, g
)
from documentos.auth import login_required
from .models import Trabajadores, Categorias, Niveles, Opciones,Generos, Sindicatos, Municipios
import datetime
from . import db

bp = Blueprint('trabajadores',__name__,url_prefix='/trabajadores')

@bp.route('/index')
@login_required
def index():
    return 'index'

@bp.route('/create')
@login_required
def create():
    categorias = Categorias.query.all()
    niveles = Niveles.query.all()
    opciones = Opciones.query.all()
    generos = Generos.query.all()
    sindicatos = Sindicatos.query.all()
    municipios = Municipios.query.all()
    if request.method == 'POST':
        numemp = request.form['numero']
        nom = request.form['nombre']
        pat = request.form['paterno']
        mat = request.form['materno']
        ingreso = request.form['ingreso']
        ingreso = ingreso.strip("%Y-%m-%d")
        rfc = request.form['rfc']
        curp = request.form['curp']
        afilia = request.form['afiliacion']
        pens = request.form['pension']
        catego = request.form['categoria']
        nivel = request.form['nivel']
        opcion = request.form['opcion']
        genero = request.form['genero']
        sindicato = request.form['sindicatos']
        localidad = request.form['localidad']

        trabajadores = Trabajadores(numemp,nom,pat,mat,ingreso,rfc,curp,afilia,pens,catego,nivel,opcion,
                                    genero,sindicato,localidad)
        db.session.add(trabajadores)
        db.session.commit()

        return render_template('trabajadores/index.html')
    return render_template('trabajadores/create.html',cates = categorias, niveles = niveles, opciones = opciones,
                           generos = generos, sindicatos = sindicatos, localidades = municipios)