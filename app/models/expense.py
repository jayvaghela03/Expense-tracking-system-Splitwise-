from db import db

class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    expense_id = db.Column(db.Integer, primary_key= True)
    expense_type = db.Column(db.String(10), nullable= False)
    total_amount = db.Column(db.Float(precision=2), nullable=False)
    expense_name = db.Column(db.String(50))
    payer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable= False)
    participants = db.Column(db.String(255), nullable=False)
    split_by = db.Column(db.String(255))
    payer = db.relationship("UserModel", back_populates="expenses")