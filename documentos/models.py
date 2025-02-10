from documentos import db
from sqlalchemy import text, select

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombres = db.Column(db.String(40), nullable = False)
    ap_paterno = db.Column(db.String(20),nullable = False)
    ap_materno = db.Column(db.String(20))
    secretaria = db.Column(db.Integer, db.ForeignKey('secretarias.id'))
    usuario = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    comite = db.Column(db.Integer, db.ForeignKey('comites.id'))
    estatus = db.Column(db.Integer, db.ForeignKey('estatus_usuario.id'))

    def __init__(self,nombres,ap_paterno,ap_materno,secretaria,
                 usuario,password,comite,estatus):
        #self.id = id
        self.nombres = nombres
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.secretaria = secretaria
        self.usuario = usuario
        self.password = password
        self.comite = comite
        self.estatus = estatus

    def __repr__(self):
        return f'< Usuario: {self.usuario} >'
    
class Documentos(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True, unique=True)
    folio = db.Column(db.Integer,nullable=True)
    nombre = db.Column(db.String(40),nullable=False)
    documento = db.Column(db.LargeBinary, nullable= False)
    exte = db.Column(db.String(5),nullable=False)
    asunto = db.Column(db.Integer, db.ForeignKey('asuntos.id'))
    asunto_styc = db.Column(db.Integer,db.ForeignKey('asuntos_styc.id'))
    secretaria = db.Column(db.Integer,db.ForeignKey('secretarias.id'))
    fecha = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __init__(self,folio,nombre,documento,exte,asunto,asunto_styc,secretaria,fecha,usuario):
        self.folio = folio
        self.nombre = nombre
        self.documento = documento
        self.exte = exte
        self.asunto = asunto
        self.asunto_styc = asunto_styc
        self.secretaria = secretaria
        self.fecha = fecha
        self.usuario = usuario

    def __repr__(self):
        return f'< Documento: {self.nombre} >'
    
    @staticmethod
    def get_by_id(id):
        return Documentos.query.get(id)

class Asuntos(db.Model):
    __tablename__ = 'asuntos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asunto = db.Column(db.String(40),nullable=False)
    empleado = db.Column(db.Integer, nullable = False)
    fecha = db.Column(db.Date, nullable = False)
    secretaria = db.Column(db.Integer, db.ForeignKey('secretarias.id'))
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estatus = db.Column(db.Integer, db.ForeignKey('estatus_asuntos.id'))

    def __init__(self,asunto,empleado,fecha,secretaria,usuario,estatus):
        self.asunto = asunto
        self.empleado = empleado
        self.fecha = fecha
        self.secretaria = secretaria
        self.usuario = usuario
        self.estatus = estatus

    def __repr__(self):
        return f'< Asunto: {self.asunto} >'
    
    @staticmethod
    def get_by_id(id):
        return Asuntos.query.get(id)
    
    @staticmethod
    def get_asunto_by_id(id):
        stmt = text("SELECT asunto FROM Asuntos WHERE id = " + str(id))
        asunto = db.session.execute(stmt).one()
        return asunto

class Secretarias(db.Model):
    __tablename__ = 'secretarias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secretaria = db.Column(db.String(40),nullable=False)
    codigo = db.Column(db.String(10),nullable=False)

    def __init__(self,secretaria,codigo):
        self.secretaria = secretaria
        self.codigo = codigo

    def __repr__(self):
        return f'< Secretaria: {self.secretaria} >'
    
    @staticmethod
    def get_sria_by_id(id):
        stmt = text('SELECT secretaria FROM secretarias WHERE id = ' + str(id))
        sria = db.session.execute(stmt).one()
        return sria[0]

class Comites(db.Model):
    __tablename__ = 'comites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comite = db.Column(db.String(40), nullable=False)

    def __init__(self,comite):
        self.comite = comite

    def __repr__(self):
        return f'< Comite: {self.comite}>'
    
class Estatus_usuario(db.Model):
    __tablename__ = 'estatus_usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estatus = db.Column(db.String(40), nullable=False)

    def __init__(self, estatus):
        self.estatus = estatus

    def __repr__(self):
        return f'< Estatus: {self.estatus}>'
    
class Estatus_asuntos(db.Model):
    __tablename__ = 'estatus_asuntos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estatus = db.Column(db.String(40), nullable=False)

    def __init__(self, estatus):
        self.estatus = estatus

    def __repr__(self):
        return f'< Estatus: {self.estatus}>'
    
class Conflictos(db.Model):
    __tablename__ = 'conflictos'
    folio = db.Column(db.Integer, primary_key=True, autoincrement=False)
    secretaria = db.Column(db.Integer,db.ForeignKey('secretarias.id'))
    asunto = db.Column(db.Integer,db.ForeignKey('asuntos_styc.id'))
    empleado = db.Column(db.Integer,db.ForeignKey('trabajadores.numero'))
    pensionado = db.Column(db.Integer,db.ForeignKey('pensionados.pensionado'))
    ispen = db.Column(db.Boolean,nullable=False)
    clausula_convenio = db.Column(db.Text, nullable=True)
    info_extra = db.Column(db.Text, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.Date,nullable=False)
    estatus = db.Column(db.Integer,nullable=False)

    def __init__(self,folio,secretaria,asunto,empleado,pensionado,ispen,
                 clausula_convenio,info_extra,observaciones,fecha,estatus):
        self.folio = folio
        self.secretaria = secretaria
        self.asunto = asunto
        self.empleado = empleado
        self.pensionado = pensionado
        self.ispen = ispen
        self.clausula_convenio = clausula_convenio
        self.info_extra = info_extra
        self.observaciones = observaciones
        self.fecha = fecha
        self.estatus = estatus

    def __repr__(self):
        return f'< Folio: {self.folio}>'
    
    @staticmethod
    def get_sriaid_by_folio(folio):
        stmt = text('SELECT secretaria FROM conflictos WHERE folio = ' + str(folio))
        sria = db.session.execute(stmt).one()
        return sria[0]
    
    @staticmethod
    def get_ispen_by_folio(folio):
        stmt = text("SELECT ispen FROM conflictos WHERE folio = " + str(folio))
        ispen = db.session.execute(stmt).one()
        return ispen[0]
    
    @staticmethod
    def get_numemp_by_folio(folio):
        stmt = text("SELECT empleado FROM conflictos WHERE folio = " + str(folio))
        num = db.session.execute(stmt).one()
        return num[0]
    
    @staticmethod
    def get_numpens_by_folio(folio):
        stmt = text("SELECT pensionado FROM conflictos WHERE folio = " + str(folio))
        num = db.session.execute(stmt).one()
        return num[0]
    
    @staticmethod
    def get_asuntoid_by_folio(folio):
        stmt = text("SELECT asunto FROM conflictos WHERE folio = " + str(folio))
        asunto = db.session.execute(stmt).one()
        return asunto[0]
    
    @staticmethod
    def get_estatusid_by_folio(folio):
        stmt = text("SELECT estatus FROM conflictos WHERE folio = " + str(folio))
        estatus = db.session.execute(stmt).one()
        return estatus[0]

class Sindicatos(db.Model):
    __tablename__ = 'sindicatos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    sindicato = db.Column(db.Text,nullable=False)
    nombre = db.Column(db.Text,nullable=False)

    def __init__(self,id,sindicato,nombre):
        self.id = id
        self.sindicato = sindicato
        self.nombre = nombre

    def __repr__(self):
        return f'< Sindicato : {self.sindicato}>'
    
class Asuntos_styc(db.Model):
    __tablename__ = 'asuntos_styc'
    id = db.Column(db.Integer,primary_key=True,autoincrement=False)
    secretaria = db.Column(db.Integer, db.ForeignKey('secretarias.id'))
    asunto = db.Column(db.Text,nullable=False)
    conflicto = db.relationship('Conflictos', backref='conflictos')

    def __init__(self,id,secretaria,asunto):
        self.id = id
        self.secretaria = secretaria
        self.asunto = asunto

    def __repr__(self):
        return f'< Secretaria : {self.secretaria}>'
    
    @staticmethod
    def get_by_id(id):
        return Asuntos_styc.query.get(id)
    
    @staticmethod
    def get_asunto_by_id(id):
        stmt = text('SELECT asunto FROM Asuntos_styc WHERE id = ' + str(id))
        asunto = db.session.execute(stmt).one()
        return asunto[0]
    
class Generos(db.Model):
    __tablename__ = 'generos'
    id =db.Column(db.Integer,primary_key=True,autoincrement=False)
    genero = db.Column(db.Text,nullable=False)
    codigo = db.Column(db.Text,nullable=False)

    def __init__(self,id,genero,codigo):
        self.id = id
        self.genero = genero
        self.codigo = codigo

    def __repr__(self):
        return f'<Genero : {self.genero}>'

class Trabajadores(db.Model):
    __tablename__ = 'trabajadores'
    numero = db.Column(db.Numeric,primary_key=True,autoincrement=False)
    nombre = db.Column(db.Text,nullable=False)
    ap_paterno = db.Column(db.Text,nullable=False)
    ap_materno = db.Column(db.Text,nullable=True)
    ingreso = db.Column(db.Date)
    rfc = db.Column(db.Text)
    curp = db.Column(db.Text,nullable=True)
    afiliacion = db.Column(db.Integer,nullable=False)
    pension = db.Column(db.Integer,nullable=False)
    categoria = db.Column(db.Integer,nullable=False)
    nivel = db.Column(db.Integer,db.ForeignKey('niveles.nivel'))
    opcion = db.Column(db.Text,db.ForeignKey('opciones.opcion'))
    genero = db.Column(db.Integer, db.ForeignKey('generos.id'))
    sindicato = db.Column(db.Integer, db.ForeignKey('sindicatos.id'))
    localidad = db.Column(db.Integer, db.ForeignKey('municipios.codigo'))

    def __init__(self,numero,nombre,ap_paterno,ap_materno,ingreso,rfc,curp,
                 afiliacion,pension,categoria,nivel,opcion,genero,sindicato,localidad):
        self.numero = numero
        self.nombre = nombre
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.ingreso = ingreso
        self.rfc = rfc
        self.curp = curp
        self.afiliacion = afiliacion
        self.pension = pension
        self.categoria = categoria
        self.nivel = nivel
        self.opcion = opcion
        self.genero = genero
        self.sindicato = sindicato
        self.localidad = localidad

    def __repr__(self):
        return f'<Nombre : {self.nombre ,' ', self.ap_paterno ,' ', self.ap_materno}>'
    
    @staticmethod
    def get_trabajador_by_num(num):
        stmt = text("select concat(nombre,' ',ap_paterno,' ',coalesce(ap_materno,' ')) as nombre from trabajadores where numero = " + str(num))
        nombre = db.session.execute(stmt).one()
        return nombre[0]

    @staticmethod
    def get_trabajadores():
        stmt = text("select t.numero as num, concat(t.nombre,' ',t.ap_paterno,' ',coalesce(t.ap_materno,'')) as nombre from trabajadores t")
        trabajadores = db.session.execute(stmt).all()
        return trabajadores
    
class Tipo_pensiones(db.Model):
    __tablename__ = 'tipo_pensiones'
    id = db.Column(db.Integer,primary_key=True,autoincrement=False)
    tipo = db.Column(db.Text,nullable=False)

    def __init__(self,id,tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return f'<Tipo : {self.tipo}>'
    
class Municipios(db.Model):
    __tablename__ = 'municipios'
    codigo = db.Column(db.Integer,primary_key=True,autoincrement=False)
    municipio = db.Column(db.Integer,nullable=False)

    def __init__(self,codigo,municipio):
        self.codigo = codigo
        self.municipio = municipio

    def __repr__(self):
        return f'<Municipio : {self.municipio}>'
    
class Pensionados(db.Model):
    __tablename__ = 'pensionados'
    pensionado = db.Column(db.Numeric,primary_key=True,autoincrement=False)
    nombres = db.Column(db.Text,nullable=False)
    ap_paterno = db.Column(db.Text,nullable=False)
    ap_materno = db.Column(db.Text,nullable=True)
    fec_nacimiento = db.Column(db.Date,nullable=False)
    genero = db.Column(db.Integer,db.ForeignKey('generos.id'))
    telefono = db.Column(db.Text,nullable=True)
    municipio = db.Column(db.Integer,db.ForeignKey('municipios.codigo'))
    tipo_pension = db.Column(db.Integer,db.ForeignKey('tipo_pensiones.id'))
    sindicato = db.Column(db.Integer,db.ForeignKey('sindicatos.id'))

    def __init__(self,pensionado,nombres,ap_paterno,ap_materno,fec_nacimiento,
                 genero,telefono,municipio,tipo_pension,sindicato):
        self.pensionado = pensionado
        self.nombres = nombres
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.fec_nacimiento = fec_nacimiento
        self.genero = genero
        self.telefono = telefono
        self.municipio = municipio
        self.tipo_pension = tipo_pension
        self.sindicato = sindicato

    def __repr__(self):
        return f'< Nombre : {self.nombres}>'
    
    @staticmethod
    def get_pensionado_by_pension(pen):
        stmt = text("select concat(nombres,' ',ap_paterno,' ',coalesce(ap_materno,' ')) as nombre from pensionados where pensionado = " + str(pen))
        nombre = db.session.execute(stmt).one()
        return nombre[0]
    
    @staticmethod
    def get_pensionados():
        stmt = text("select pensionado as num, concat(nombres,' ',ap_paterno,' ',coalesce(ap_materno,'')) as nombre from pensionados")
        pensionados = db.session.execute(stmt).all()
        return pensionados

class Categorias (db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer,primary_key=True,autoincrement=False)
    categoria = db.Column(db.Text,nullable=False)

    def __init__(self,id,categoria):
        self.id = id
        self.categoria = categoria

    def __repr__(self):
        return f'< Categoria : {self.categoria}>'

class Niveles(db.Model):
    __tablename__= 'niveles'
    nivel = db.Column(db.Integer,primary_key=True,autoincrement=False)
    descripcion = db.Column(db.Text,nullable=False)

    def __init__(self, nivel, descripcion):
        self.nivel = nivel
        self.descripcion = descripcion

    def __repr__(self):
        return f'< Descripcion : {self.descripcion}>'
    
class Opciones(db.Model):
    __tablename__ = 'opciones'
    opcion = db.Column(db.Text,primary_key=True)
    descripcion = db.Column(db.Text, nullable=True)

    def __init__(self,opcion,descripcion):
        self.opcion = opcion
        self.descripcion = descripcion

    def __repr__(self):
        return f'< Descripcion : {self.descripcion}>'