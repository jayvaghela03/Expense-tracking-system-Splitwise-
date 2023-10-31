from flask.views import MethodView 
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required

from db import db

from schema import UserSchema, LoginSchema
from models import UserModel

blp = Blueprint("users", __name__, description= "Operations on users")
    

@blp.route("/register")
class UserRegister(MethodView):    
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.name == user_data["name"]).first():
            abort(409, message= "A user with that name already exists")
            
        user = UserModel(name=user_data["name"], 
                        email=user_data["email"],
                        mobile_number=user_data["mobile_number"], 
                        password=pbkdf2_sha256.hash(user_data["password"]))
        try:    
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message= "An error occured while creating user")

        return user
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):    
        user = UserModel.query.filter(
            UserModel.name == user_data['name']
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.user_id)
            return {"access_token": access_token}
        
        abort(401, message= "Invalid credentials")
        
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User deleted"}