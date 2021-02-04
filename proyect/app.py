from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.Resources import auth
from api.Resources import usuarios, evento
from api.Utils.database import db

#En este archivo se inicializan los servicios de Flask para definir los recursos, la base de datos y los schemas
#que representan los servicios

#Se inicializa app como una aplicación flask
app = Flask(__name__)

#Se configuar la variable de ambiente donde se guarda la llave secreta para JWT
app.config.from_envvar('ENV_FILE_LOCATION')

#Se configura una base de datos sqlite usando el servicio de SQLalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.db'

#Se inicializa el servicio de Marshmallow para la definición de Schemas
ma = Marshmallow(app)

#Se inicializa el servicio de API dado por Flask-restful para construir la API
api = Api(app)

#Se inicializa el servicio de encriptación para poder guardar de forma segura las claves de los usuarios
bcrypt = Bcrypt(app)

#Se inicializa el servicio de JWTManager para el uso de Json Web Tokens
jwt = JWTManager(app)

#En caso de que la base de datos no haya sido creada por primera vez se crea al iniciar la aplicación.
#Esto solo se realiza una vez ya que se detecta si la base de datos ya está creada.
db.init_app(app)
with app.app_context():
    db.create_all()

#Se agregan los recursos de parte de los diferentes modelos de la aplicación.
#Cada recurso dentro de los modelos tiene una dirección dependiendo de lo que se necesite.
#Por convención todas las direcciones empiezan por '/api' para evitar conflictos con las rutas de servicios del front-end
api.add_resource(evento.RecursoListarEventos, '/api/events')
api.add_resource(evento.RecursoUnEvento, '/api/events/<int:id_evento>')
#api.add_resource(usuarios.RecursoListarUsuarios, '/api')
api.add_resource(usuarios.RecursoUnUsuario, '/api')
api.add_resource(auth.SignupApi, '/api/auth/signup')
api.add_resource(auth.LoginApi, '/api/auth/login')

#Se corre la aplicación en modo de debug
if __name__ == '__main__':
    app.run(debug=True)
