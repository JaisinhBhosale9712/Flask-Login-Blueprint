from flask import request, jsonify, current_app
import jwt
from views.models import db, User
from functools import wraps
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if "x-access-token" in request.cookies:
            token = request.cookies["x-access-token"]
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message":"Token is missing"})
        try:
            data = jwt.decode(token,current_app.config["SECRET_KEY"],"HS256")
            user = User.query.filter_by(name=data["username"]).first()
        except:
            return jsonify({"message":"token is invalid"})
        return f(user,*args,**kwargs)
    return decorated
