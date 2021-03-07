from views import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(40))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.name}', '{self.password}')"
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return f"Todo({self.text},{self.user_id})"