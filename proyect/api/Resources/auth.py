from api.Utils.database import db
from api.Resources.usuarios import Usuario
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
import datetime


class SignupApi(Resource):
    def post(self):
        new_user = Usuario(
            email=request.json['email'],
            password=request.json['password']
        )
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        id = new_user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):
    def post(self):
        mail = request.json['email']
        password = request.json['password']
        user = Usuario.query.filter_by(email=mail).first_or_404()
        authorized = user.check_password(password)
        if not authorized:
            return {'error': 'Email or password invalid'}, 401
        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
