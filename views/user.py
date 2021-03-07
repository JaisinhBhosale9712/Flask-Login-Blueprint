from flask import Blueprint,request, jsonify, session
import jwt
import pdb
import uuid
from werkzeug.security import generate_password_hash
from views.models import User
from views import db
from functions_required.token_check import token_required

user = Blueprint("user",__name__)

@user.route("/user",methods=["GET","POST","PUT"])
def check_method():
    if request.method == "POST":  #Jay,string
        data = request.get_json()
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(public_id=str(uuid.uuid4()),name=data["name"],password=hashed_password,admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"new user created"})
    else:
        users = User.query.all()
        session["user"]="hello"
        output = []
        for user in users:
            user_data={"id":user.id,"public_id":user.public_id,"name":user.name,"password":user.password,"admin":user.admin}
            output.append(user_data)
        return jsonify({"user_data":output})


@user.route("/user/<user_id>", methods=["GET","DELETE","PUT"])
@token_required
def check_method_1(user,user_id):
    if request.method == "GET":
        user = User.query.filter_by(id=user_id).first()
        user_data = {"id": user.id, "public_id": user.public_id, "name": user.name, "password": user.password,
                     "admin": user.admin}
        return jsonify({"user": user_data})
    elif request.method == "PUT":
        user = User.query.filter_by(id=user_id).first()
        pdb.set_trace()
        print(user.name)
        user.admin = True
        print(user.admin)
        db.session.commit()
        return jsonify({"message":"user is promoted"})
    else:
        #delete
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return({"message":"User deleted"})

