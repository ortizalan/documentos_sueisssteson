from flask import Blueprint, render_template, redirect, request, url_for, g
from documentos.auth import login_required
from documentos.models import Documentos
import io, base64,os
import sqlalchemy as data

bp = Blueprint('visor',__name__,url_prefix='/visor')

@bp.route('/mostrar/<int:id>/<string:ext>/<int:sria>')
@login_required
def mostrar(id,ext,sria):
    docs = Documentos.get_by_id(id)

    if(docs is not None):
        if ext == ".pdf":
            d = docs.documento
            if (sria == 5 or sria == 13):
                asunto = docs.asunto_styc
            else:
                asunto = docs.asunto
            ext = docs.exte[1:]
            sria = docs.secretaria

            script_dir = os.path.dirname(os.path.abspath(__file__))
            f_path = os.path.join(script_dir,'static/docs/documento.pdf')
            with open(f_path, 'wb') as dw:
                dw.write(d)
            
            # docu = 'documento.pdf'
            return render_template('/visor/view.html', docu = f_path, asunto = asunto, ext = ext, sria = sria)
        else:
            docu = base64.b64encode(docs.documento).decode('utf-8') 
            if (sria == 5 or sria == 13):
                asunto = docs.asunto_styc
            else:
                asunto = docs.asunto
            ext = docs.exte[1:]
            sria = docs.secretaria
            return render_template('/visor/view.html', docu = docu, asunto = asunto, ext = ext,sria = sria)
    else:
        return 'None'

# @bp.route('/mostrar')
# @login_required
# def mostrar():
#     #archivo = io.BytesIO(file)
#     return render_template('/visor/view.html')


# @bp.route('/mostrar/<int:id>/<string:ext>')
# @login_required
# def mostrar(id, ext):
#     # from sqlalchemy import select
#     # from sqlalchemy.orm import defer, Session

#     # engine = data.create_engine("mysql+pymysql://sue24-27:Sueisssteson2024@localhost/documentos_db")
#     # meta_data = data.MetaData()
#     # meta_data.reflect(bind = engine)

#     # DOCS = meta_data.tables['Documentos']

#     # query = data.select(DOCS.c.documento).where(DOCS.c.id = id)

#     # with Session(engine) as session:
#     #     #stmt = select(Documentos).where(Documentos.id == id).options(defer(Documentos.documento,Documentos.asunto,Documentos.exte))  # type: ignore
#     #     whereStmt = "Documentos.id == " + str(id)
#     #     stmt = select(Documentos).where(eval(whereStmt))
#     #     docs = session.execute(stmt)
#     res = Documentos.get_by_id(id)

#     if ext == '.pdf':
#         for doc in docs:
#             #if(doc.id == id):
#             d = doc.documento
#             #docu = doc.documento
#             asunto = doc.asunto
#             ext = doc.exte[1:]
#         #bytes = base64.b64decode(d)
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         f_path = os.path.join(script_dir,'static/docs/documento.pdf')
#         with open(f_path, 'wb') as dw:
#             dw.write(d)
           
        
#         docu = 'documento.pdf'
#         return render_template('/visor/view.html', docu = f_path, asunto = asunto, ext = ext)
#     else:
#         for doc in docs:
#             docu = base64.b64encode(doc.documento).decode('utf-8') 
#             asunto = doc.asunto
#             ext = doc.exte[1:]
#         return render_template('/visor/view.html', docu = docu, asunto = asunto, ext = ext)
#     # return '-- EN CONSTRUCCIÓN. --'