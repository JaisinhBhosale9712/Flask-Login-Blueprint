from flask import make_response,jsonify, request,Blueprint, current_app
from werkzeug.security import check_password_hash
import datetime
from datetime import datetime as dt
import jwt
from views.models import User

login = Blueprint("login",__name__)

@login.route("/login")
def login_check():
    auth=request.authorization
    if auth and auth.password and auth.username:
        user = User.query.filter_by(name=auth.username).first()
        if not user:
            return jsonify({"message":"user not found"})
        if check_password_hash(user.password,auth.password):
            token=jwt.encode({'username':user.name,"id":user.id,"password":user.password,'exp':dt.utcnow()+datetime.timedelta(minutes=10)},current_app.config["SECRET_KEY"])
            resp = make_response(jsonify({"token":token}))
            resp.set_cookie("x-access-token",token,expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
            return resp
    return make_response("Could not verify user","401",{'WWW-Authenticate':'Basic realm="Login required"'})
