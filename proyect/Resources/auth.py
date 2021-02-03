from Utils.database import db
from flask import request
from Resources.usuarios import Usuario
from flask_restful import Resource


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
