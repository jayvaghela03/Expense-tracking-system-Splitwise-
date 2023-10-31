from mail_utility import send_mail
from models import UserModel, ExpenseModel

def calculate_expense(expense_data, payer_id):
    # Extract relevant data from the input
    total_amount = expense_data["total_amount"]
    expense_type = expense_data["expense_type"]
    participants = [participant.strip() for participant in expense_data["participants"].split(",")]

    try:
        split_by = [float(splits.strip()) for splits in expense_data["split_by"].split(",")]
    except:
        if expense_type=="PERCENT" or expense_type=="EXACT":
            raise 
    
    # Fetch the payer
    payer = UserModel.query.get(payer_id)
    if payer is None:
        raise ValueError("Payer not found")

    if expense_type == 'EQUAL':
        # Calculate equal shares for all participants
        total_participants = len(participants)  # Including the payer
        share_per_person = total_amount / total_participants
        payer.balance -= total_amount

        for user in participants:
            participant = UserModel.query.filter_by(name=user).first()
            if participant:
                participant.balance += share_per_person
            else:
                raise ValueError(f"User not found: {user}")

    elif expense_type == 'EXACT':
        # Distribute expenses exactly as provided in the input
        if sum(split_by)==total_amount:
            for user, share in zip(participants,split_by):
                participant = UserModel.query.filter_by(name=user).first()
                if participant:
                    share = float(share)
                    participant.balance += share
                    payer.balance -= share
                else:
                    raise ValueError(f"User not found: {user}")
        else:
            raise ValueError("Split_by's sum should be equal to total_amount")

    elif expense_type == 'PERCENT':
        # Distribute expenses based on percentages
        total_percentage = sum(split_by)
        if total_percentage != 100:
            raise ValueError("Total percentage should be 100")

        for user, percentage in zip(participants, split_by):
            participant = UserModel.query.filter_by(name=user).first()
            if participant:
                share = (percentage / 100) * total_amount
                participant.balance += share
                payer.balance -= share
            else:
                raise ValueError(f"User not found: {user}")

    # Create the ExpenseModel
    try:
        expense = ExpenseModel(
            expense_type=expense_type,
            total_amount=total_amount,
            expense_name=expense_data.get("expense_name"),
            payer_id=payer_id,
            participants=','.join(participants),
            split_by=','.join([str(splits) for splits in split_by])
        )
    except:
        expense = ExpenseModel(
            expense_type=expense_type,
            total_amount=total_amount,
            expense_name=expense_data.get("expense_name"),
            payer_id=payer_id,
            participants=','.join(participants),
        )
    
    return expense

def get_owe(expense, total_amount, payer, participants, name):
    owe = ""
    if expense.expense_type=="EQUAL":
        share = round(total_amount/len(participants),2)
        if name !=payer:    
            owe = f"You owe {share} to {payer}"
        else:
            share = total_amount-share
            owe = f"You are owed {share}"
        
    elif expense.expense_type=="EXACT":
        split_by = [float(split.strip()) for split in expense.split_by.split(",")]
        for share in split_by:
            if payer in participants:
                if name!= payer:
                    owe = f"You owe {share} to {payer}"
                else:
                    owe = f"You are owed {total_amount-share}"
            else:
                owe = f"You are owed {total_amount}"
        
    elif expense.expense_type=="PERCENT":
        split_by = [float(split.strip()) for split in expense.split_by.split(",")]
        for percent in split_by:
            share = (percent/100)*total_amount
            if payer in participants:
                if name!= payer:
                    owe = f"You owe {share} to {payer}"
                else:   
                    owe = f"You are owed {total_amount-share}"
            else:
                owe = f"You are owed {total_amount}"
    return owe


def get_my_expenses(all_expenses, name):
    final_output= []
    for expense in all_expenses:
        item = {}
        total_amount = expense.total_amount
        expense_name = expense.expense_name
        payer = expense.payer.name
        participants = [participant.strip() for participant in expense.participants.split(",")]

        owe = get_owe(expense, total_amount, payer, participants, name)
        
        item["total_amount"]= total_amount
        item["payer"]= payer
        item["expense_name"]= expense_name
        item["owes"]= owe
        final_output.append(item)
    
    return final_output

def proccess_mail(expense):
    subject = "Expense added"
    participants = [participant.strip() for participant in expense.participants.split(",")]
    total_amount = expense.total_amount
    payer = expense.payer.name
    for user in participants:   
        user_instance = UserModel.query.filter_by(name=user).first()
        mail = user_instance.email
        
        owe = get_owe(expense, total_amount, payer, participants, user)        
        body = f"""Hi {user.capitalize()},
                You have been added to an expense by {payer.capitalize()}.
                Total amount = {total_amount}
                Owe's = {owe}""" 
    
        send_mail(subject, mail, body)
        
def generate_report():
    subject = "Weekly Splitwise report"
    try:    
        users = UserModel.query.all()
    except:
        raise ValueError("No users founf")

    if users:
        for user in users:
            user_expenses = ExpenseModel.query.filter(
            (ExpenseModel.participants.like(f"%{user.name}%"))
            ).all()
            
            mail = user.email
            balance = user.balance
            if user_expenses:    
                body = f"Hi {user.name.capitalize()}, \n Your Total balance is {balance}. \n"
                for expense in user_expenses:
                    participants = [participant.strip() for participant in expense.participants.split(",")]
                    total_amount = expense.total_amount
                    payer = expense.payer.name
                    
                    owe = get_owe(expense, total_amount, payer, participants, user.name)
                    body+= f"For {expense.expense_name} {owe}. \n"
                
                send_mail(subject, mail, body)
            else:
                body = f"Hi {user.name.capitalie()}, \n Your Total Balance is {balance}."
                send_mail(subject, mail, body)