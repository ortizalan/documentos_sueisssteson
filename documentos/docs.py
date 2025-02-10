from flask import Blueprint, render_template, redirect, request, url_for, g
from documentos.auth import login_required
from .models import Documentos, Usuarios, Asuntos, Asuntos_styc
from . import db
from datetime import date
from io import BytesIO
import os, base64



bp = Blueprint('docs',__name__,url_prefix='/docs')


@bp.route('/list/<int:a>/<int:sria>')
@login_required
def index(a,sria):
    
    if sria == 5 or sria == 13:
        asnt = Asuntos_styc.get_asunto_by_id(a)
        docs = Documentos.query.filter_by(asunto_styc = a)
    else:
        asnt = Asuntos.get_asunto_by_id(a)
        docs = Documentos.query.filter_by(asunto = a)
    return render_template('docs/index.html', docs = docs, asunto = asnt)


@bp.route('/create/<int:folio>/<int:asunto_id>/<int:asunto_styc>/<int:sria>/<string:asunto>', methods=('GET','POST'))
@login_required
def create(folio,asunto_id,asunto_styc,sria,asunto):
    asuntos = Asuntos.query.filter_by(id = id).first()
    
    if request.method == 'POST':
        folio = request.form['folio']
        nombre = request.form['nombre']
        documento = request.files['documento']
        split = os.path.splitext(str(documento.filename))
        exte = split[-1]
        asunto = request.form['asunto_id']
        asunto_styc = request.form['asunto_styc']
        secretaria = sria
        fecha = request.form['fecha']
        usuario = g.user.id

        docs = Documentos(folio,nombre,documento.read(),exte,asunto_id,asunto_styc,secretaria,fecha,usuario)

        db.session.add(docs)
        db.session.commit()
        if sria == 5 or sria == 13:
            return redirect(url_for('conflictos.index'))
        else:
            return redirect(url_for('asuntos.index'))
    return render_template('docs/create.html', c_date = date.today(),folio = folio, asunto_id = asunto_styc, asunto = asunto, sria = sria)


# OBTENER UN DOCUMENTO X ID
def get_one_doc(id):
    doc = Documentos.query.get_or_404(id)
    return doc

from sqlalchemy import text
# # OBTENER ÚLTIMO REGISTRO
def get_last_doc(sria):
    with db.engine.connect() as  connect:
        result = connect.execute(text('SELECT id FROM documentos'))
    return "doc"

@bp.route('/update/<int:id>/<int:sria>', methods=('GET','POST'))
@login_required
def update(id,sria):

    docs = Documentos.query.filter_by(id = id, secretaria = sria).first_or_404()
    
    #docs = Documentos.query.get_or_404(id)
    
    if request.method == 'POST':
        docs.nombre = request.form['nombre']
        if request.files["documento"]:
            docs.documento = request.files['documento'].read()
        # docs.estatus = True if request.form.get('estatus') == 'on' else False

        db.session.commit()
        return redirect(url_for('docs.index', a = docs.asunto))
    return render_template('docs/update.html', docs = docs)

@bp.route('/delete/<int:id>/<int:a>/<int:sria>')
@login_required
def delete(id, a, sria):
    result = Documentos.query.filter_by(id = id, secretaria = sria)
    docs = result.first()
    db.session.delete(docs)
    db.session.commit()
    return redirect(url_for('docs.index', a = a, sria = sria))


def get_doc(id):

    return "-- EN CONSTRUCCIÓN --"