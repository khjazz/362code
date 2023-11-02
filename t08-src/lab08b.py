# File: lab08b.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Write code below
from flask import (Flask, redirect, render_template_string,
                   request)
app = Flask(__name__)

template_str = """
<h2>Account</h2>
Balance: {{balance}}<br />
Last transaction: {{last_txn}}<br />
<br />
<form action="/deposit" method="POST">
<input type="text" name="amount" />
<input type="submit" value="Deposit" />
</form>
<form action="/withdraw" method="POST">
<input type="text" name="amount" />
<input type="submit" value="Withdraw" />
</form>
"""

balance = 0
last_txn = ""

@app.route("/")
def account_display():
    # todos = [(id, desc, url_for("todo_delete", id=id))
    #         for id, desc in enumerate(todo)]
    return render_template_string(template_str, balance=balance, last_txn=last_txn)

@app.route("/deposit", methods=["POST"])
def deposit():
    amount = int(request.form["amount"].strip())
    global balance, last_txn
    balance = balance + amount
    last_txn = f"deposit {amount}"
    return redirect("/")

@app.route("/withdraw", methods=["POST"])
def withdraw():
    global balance, last_txn
    amount = int(request.form["amount"].strip())
    if balance >= amount:
        balance = balance - amount
        last_txn = f"withdraw {amount}"
    else:
        last_txn = f"withdraw {amount} (failed)"
    return redirect("/")

if __name__ == "__main__":
    app.run()
