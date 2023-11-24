# File: lab09a.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Write code below
from flask import Flask, jsonify, request
app = Flask(__name__)

balance = 0

@app.post("/deposit")
def deposit():
    data = request.get_json()
    amount = data.get("amount") 
    if amount is None or not isinstance(amount, int) or amount < 0: #modify, check if it is a positive integer
        return jsonify({"error": "incorrect amount"}), 400 #change this
    global balance
    balance = balance + amount
    return jsonify({ "status": "success", "balance": balance })

@app.post("/withdraw")
def withdraw():
    data = request.get_json()
    amount = data.get("amount") 
    if amount is None or not isinstance(amount, int) or amount < 0: #modify, check if it is a positive integer
        return jsonify({"error": "incorrect amount"}), 400 #change this
    # check balance >= amouont
    global balance
    if balance >= amount:
        balance = balance - amount
        return jsonify({ "status": "success", "balance": balance })
    return jsonify({ "status": "failure (insufficient funds)", "balance": balance })

if __name__ == "__main__":
    app.run()
