from flask.views import MethodView 
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


from db import db

from schema import ExpenseSchema
from models import ExpenseModel, UserModel
from .utils import calculate_expense,get_my_expenses,proccess_mail,generate_report

blp = Blueprint("expenses", __name__, description= "Operations on expenses")

@blp.route("/expense/<int:expense_id>")
class Expense(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseModel)
    def get(self, expense_id):
        expense = ExpenseModel.query.get_or_404(expense_id)
        
        return expense
    
    @jwt_required()
    def delete(self, expense_id):
        expense = ExpenseModel.query.get_or_404(expense_id)
        
        db.session.delete(expense)
        db.session.commit()
        
        return {"message": "Expense deleted"},200
    

@blp.route("/expense")
class ExpenseList(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSchema(many=True))
    def get(self):
        return ExpenseModel.query.all()
    
    @jwt_required()
    @blp.arguments(ExpenseSchema)
    @blp.response(201, ExpenseSchema)
    def post(self, expense_data):
        try:
            # Ensure the expense type is valid
            valid_expense_types = ['EQUAL', 'EXACT', 'PERCENT']
            if expense_data["expense_type"] not in valid_expense_types:
                raise ValueError("Invalid expense type")

            # Calculate the expense and update user balances
            payer_id = get_jwt_identity()
            expense = calculate_expense(expense_data, payer_id)
            db.session.add(expense)
            db.session.commit()
            proccess_mail(expense)
        except (SQLAlchemyError, ValueError, ValidationError) as e:
            db.session.rollback()
            print(e)
            abort(500, message="An error occurred while creating the expense")

        return expense    
    
    
@blp.route("/my-expenses")
class AllExpenses(MethodView):
    @jwt_required()
    @blp.response(200, ExpenseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        name = UserModel.query.get_or_404(user_id).name

        all_expenses = ExpenseModel.query.filter(
           (ExpenseModel.payer_id.like(f"%{user_id}%")) | (ExpenseModel.participants.like(f"%{name}%"))
        ).all()
        
        return all_expenses
    
@blp.route("/my-expenses/simplified")
class AllExpenses(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self):
        user_id = get_jwt_identity()
        name = UserModel.query.get_or_404(user_id).name

        all_expenses = ExpenseModel.query.filter(
           (ExpenseModel.payer_id.like(f"%{user_id}%")) | (ExpenseModel.participants.like(f"%{name}%"))
        ).all()
        
        final_output = get_my_expenses(all_expenses, name)

        return final_output
    
@blp.route("/send-report")
class SendMail(MethodView):
    def get(self):

        generate_report()

        return {"message": "Report sent"},200