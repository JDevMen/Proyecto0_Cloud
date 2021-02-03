from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from Resources import evento, usuarios, auth
from Utils.database import db

app = Flask(__name__)

app.config.from_envvar('ENV_FILE_LOCATION')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.db'

ma = Marshmallow(app)

api = Api(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(evento.RecursoListarEventos, '/events')
api.add_resource(evento.RecursoUnEvento, '/events/<int:id_evento>')
api.add_resource(usuarios.RecursoListarUsuarios, '/')
api.add_resource(usuarios.RecursoUnUsuario, '/')
api.add_resource(auth.SignupApi, '/auth/signup')
api.add_resource(auth.LoginApi, '/auth/login')

if __name__ == '__main__':
    app.run(debug=True)
