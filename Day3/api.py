from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api,reqparse,marshal_with,abort,fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(80),unique= True,nullable=False)
    email = db.Column(db.String(80),unique= True,nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name',type=str,required = True,help="Name Should not be empty")
user_args.add_argument('email',type=str,required = True,help="Email Should not be empty")

userFields = {
    'id': fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

class UsersApi(Resource):
    @marshal_with(userFields)
    def get(self):
        user = User.query.all()
        return user
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = User(name=args["name"],email = args["email"])
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        return users, 201
    
class UserApi(Resource):
    @marshal_with(userFields)
    def get(self,id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404,message = "User not Found")
        return user
    
    @marshal_with(userFields)
    def patch(self,id):
        args = user_args.parse_args()
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404,message = "User not Found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self,id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404,message = "User not Found")
        db.session.delete(user)
        db.session.commit()
        users = User.query.all()
        return users, 204
    
api.add_resource(UsersApi,'/api/users')
api.add_resource(UserApi,'/api/users/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)