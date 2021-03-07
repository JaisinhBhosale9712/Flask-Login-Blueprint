from flask import jsonify, request,Blueprint
from functools import wraps
import jwt
from views.models import Todo, User
from views import db
from functions_required.token_check import token_required

todo = Blueprint("todo",__name__)

@todo.route("/todo",methods=["GET","POST"])
@token_required
def todo_check(user):
    if request.method == "GET":
        todos = Todo.query.filter_by(user_id=user.id).all()
        output=[]
        for todo in todos:
            item={"text":todo.text,"user_name":user.name,"complete":todo.complete}
            output.append(item)
        return jsonify({"todos":output})
    elif request.method == "POST":
        data = request.get_json()
        todo = Todo(text=data["text"],complete=False,user_id=user.id)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"message":"item added successfully"})
