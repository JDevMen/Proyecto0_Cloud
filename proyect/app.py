from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from Models import evento, usuarios
from Utils.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.db'

ma = Marshmallow(app)

api = Api(app)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(evento.RecursoListarEventos, '/events')
api.add_resource(evento.RecursoUnEvento, '/events/<int:id_evento>')
api.add_resource(usuarios.RecursoListarUsuarios, '/')
api.add_resource(usuarios.RecursoUnUsuario, '/<int:id_usuario>')

if __name__ == '__main__':
    app.run(debug=True)
