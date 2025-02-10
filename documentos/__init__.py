from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Crear extensión
db = SQLAlchemy()
# Para la actualización de la BD
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'devdocs',
        SESSION_PERMANENT=False,
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://sue24-27:Sueisssteson2024@localhost/documentos_db"
        # SQLALCHEMY_ECHO = True
    )

    # Inicializar la conexión a la base de datos
    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de Blueprints
    from . import docs
    app.register_blueprint(docs.bp)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import secretarias
    app.register_blueprint(secretarias.bp)
    from . import asuntos
    app.register_blueprint(asuntos.bp)
    from . import visor
    app.register_blueprint(visor.bp)
    from . import usuarios
    app.register_blueprint(usuarios.bp)
    from . import conflictos
    app.register_blueprint(conflictos.bp)
    from . import trabajadores
    app.register_blueprint(trabajadores.bp)
    
    @app.route('/')
    def index():
        # if g.user:
        #     return render_template('docs/index.html')
        # else:
        return render_template('index.html')
    
    
    # Crear los modelos que no existan en la base de datos
    with app.app_context():
        db.create_all()

    return app

