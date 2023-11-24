# File: lab09a.py

# Replace the following by your full name and 8-digit student number
student_name = "LIN Junming"
student_id = "13028624"

# Write code below
from flask import Flask, jsonify, request
app = Flask(__name__)

class BankAccount:
    def __init__(self):
        self.balance = 0

    def withdraw(self, amount):
        message = "success" if amount <= self.balance else "failure (insufficient funds)"
        if amount <= self.balance:
            self.balance -= amount
        return message            

    def deposit(self, amount):
        self.balance += amount
        return "success"

@app.post("/deposit")
def deposit():
    data =  request.get_json()
    amount = data.get("amount")
    try: 
        if type(amount) != int or amount < 0:
            raise Exception
    except Exception as e: 
        return jsonify({"error": "Incorrect data"}), 400
    message = account.deposit(amount)
    return jsonify({"status": message, "balance": account.balance})

@app.post("/withdraw")
def withdraw():
    data = request.get_json()
    amount = data.get("amount")
    try: 
        if type(amount) != int or amount < 0:
            raise Exception
    except Exception as e: 
        return jsonify({"error": "Incorrect data"}), 400
    message = account.withdraw(amount)
    return jsonify({"status": message, "balance": account.balance})
            
if __name__ == "__main__":
    account = BankAccount()
    app.run()