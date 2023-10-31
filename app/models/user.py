from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True, nullable= False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable= False)
    mobile_number = db.Column(db.String(20), unique=True, nullable= False)
    balance = db.Column(db.Float, default=0.0)
    expenses = db.relationship("ExpenseModel", back_populates="payer")
    