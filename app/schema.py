from marshmallow import Schema, fields


class ExpenseSchema(Schema):
    expense_id = fields.Integer(dump_only=True)
    expense_type = fields.String(required=True)
    total_amount = fields.Float(precision=2, required=True)
    expense_name = fields.String()
    payer_id = fields.Integer(required=True, dump_only=True)
    payer = fields.Nested('UserSchema', exclude=('expenses','balance','user_id',), dump_only=True)
    participants = fields.String(required=True)
    split_by = fields.String()


class UserSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    email = fields.Email(required=True)
    mobile_number = fields.String(required=True)
    balance = fields.Float(precision=2, dump_only=True)
    expenses = fields.List(fields.Nested(ExpenseSchema()), exclude=('payer','payer_id'), dump_only=True)
    
    
class LoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)