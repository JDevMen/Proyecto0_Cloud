from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.Resources import auth
from api.Resources import usuarios, evento
from api.Utils.database import db

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

api.add_resource(evento.RecursoListarEventos, '/api/events')
api.add_resource(evento.RecursoUnEvento, '/api/events/<int:id_evento>')
api.add_resource(usuarios.RecursoListarUsuarios, '/api')
api.add_resource(usuarios.RecursoUnUsuario, '/api')
api.add_resource(auth.SignupApi, '/api/auth/signup')
api.add_resource(auth.LoginApi, '/api/auth/login')

if __name__ == '__main__':
    app.run(debug=True)
