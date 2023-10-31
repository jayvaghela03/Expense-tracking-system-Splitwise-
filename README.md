# Teachmint
### Description
The Expense Sharing System is a web-based application that allows users to add and manage expenses. Users can split expenses equally, specify exact shares, or use percentages to distribute costs. The system keeps track of users' balances and provides a simple way to settle debts among friends and housemates.

##Folder Structure
.
├── app.py
├── db.py
├── instance
│   └── data.db
├── mail_utility.py
├── models
│   ├── expense.py
│   ├── __init__.py
│   └── user.py
├── requirements.txt
├── resources
│   ├── expense.py
│   ├── user.py
│   └── utils.py
└── schema.py

Entry point is app.py. All the models are being stored in models. All the routes are structured in resources.

##Schema

###User Schema
The User Schema defines the structure of user data when interacting with the Splitwise API. It specifies the format of data that should be provided when creating or retrieving user information.

###User Schema Fields:
user_id: An integer that represents the unique identifier for a user. It is marked as "dump_only," which means it is read-only and should not be included when creating or updating a user.

name: A string that represents the name of the user. It is marked as "required" and must be provided when creating a new user.
password: A string that represents the user's password. It is marked as "required" and should be provided when registering a new user. However, it is marked as "load_only," which means it should not be included in response data. This is typically the case for sensitive information like passwords.
email: A string that represents the user's email address. It is marked as "required" and must be provided when creating a new user.
mobile_number: A string that represents the user's mobile phone number. It is marked as "required" and should be provided when registering a new user.
balance: A floating-point number that represents the user's balance. It is marked as "dump_only," meaning it is read-only and should not be included when creating or updating a user.
expenses: This field represents the relationship between the User and Expense models. It is marked as "dump_only," indicating that it should not be included in the response. This field typically represents a list of expenses associated with the user.

###User Schema Usage:
When creating a new user, you need to provide the "name," "password," "email," and "mobile_number" fields. The other fields are generated or updated by the system.
When retrieving user details, the response will include the user's "user_id," "name," "email," "mobile_number," and "balance." The "password" field is excluded, as it should not be exposed.

###Expense Schema
The Expense Schema defines the structure of expense data when interacting with the Splitwise API. It specifies the format of data that should be provided when creating or retrieving expense information.
Expense Schema Fields:
expense_id: An integer that represents the unique identifier for an expense. It is marked as "dump_only," indicating that it is read-only and should not be included when creating or updating an expense.
expense_type: A string that represents the type of the expense. It is marked as "required" and should be one of the values "EQUAL," "EXACT," or "PERCENT." This field describes how the expense is split among participants.
total_amount: A floating-point number that represents the total amount of the expense. It is marked as "required" and must be provided when creating a new expense.
expense_name: A string that represents the name or description of the expense. It is optional and not required when creating an expense.
payer_id: An integer that represents the user ID of the person who paid for the expense. It is marked as "required" and must be provided when creating an expense.
participants: A field that represents the participants in the expense. It is marked as "required" and should contain data in a specific format. The exact format might vary based on the "expense_type." For example, in an "EQUAL" expense, it might be a list of participant names, while in an "EXACT" expense, it might be a dictionary of participants and their shares.
split_by: A field that seems to represent how the expense is split.


##System Design

###API Server (Flask): The API server is responsible for handling incoming requests from clients and managing the core business logic. It serves as the intermediary between the client and the database.
Database (SQLAlchemy): The database stores user information, expense data, and the relationships between users and expenses. It allows for data persistence and retrieval.

###API Contracts
User Management API
The User Management API provides endpoints for creating and retrieving user information. Users can register with their name, email, and mobile number. The API allows the following operations:

Create a User: Users can register by providing their personal information.
Get User by ID: Retrieve user details by specifying a user ID.
Get All Users: Fetch a list of all registered users.
Expense Management API
The Expense Management API offers endpoints for creating and managing expenses. Users can create expenses, specify the type of expense (EQUAL, EXACT, PERCENT), and define participants. The API includes these operations:
Create an Expense: Users can create a new expense, indicating the payer, total amount, expense type, and participants.
Get Expense by ID: Retrieve expense details by specifying an expense ID.
Get All Expenses: Fetch a list of all recorded expenses.

###Class Structure
The system's core data structure includes two primary classes:
User Class: Represents a user in the system and includes fields for user ID, name, email, mobile number, and balance. The balance field stores the financial balance of the user.
Expense Class: Represents an expense in the system and includes fields for expense ID, the user who paid, the total amount, the expense type, and participants. The participants field is a dictionary that stores the user IDs and their respective shares in the expense.

###Running the Application
To run the Expense Sharing System:

Install the required dependencies using pip install -r requirements.txt.
Start the Flask application using python app.py.
Access the API at http://localhost:5000.


Apache Airflow for scheduling the weekly mail. 
Why Apache Airflow:
Apache Airflow is an open-source platform for programmatically authoring, scheduling, and monitoring workflows. It is used to automate and orchestrate complex tasks and workflows, making it an ideal choice for managing and scheduling data pipelines, ETL (Extract, Transform, Load) processes, and more.

How to Start Apache Airflow:
airflow webserver -p 8080

Start the scheduler for task scheduling:
airflow scheduler

It contains a dag file(send_mail_dag.py) which is the logic to hit the send-report endpoint on scheduled time.
Now you can access the Airflow web UI at http://localhost:8080.
