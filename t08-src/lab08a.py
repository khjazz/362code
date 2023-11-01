# File: lab08a.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Write code below
from flask import Flask
app = Flask(__name__)

@app.get("/<int(signed=True):a>/plus/<int(signed=True):b>")
def add(a, b):
    return f"{a} + {b} = {a+b}"

@app.get("/<int(signed=True):a>/minus/<int(signed=True):b>")
def subtract(a, b):
    return f"{a} - {b} = {a-b}"

@app.get("/<int(signed=True):a>/times/<int(signed=True):b>")
def multiply(a, b):
    return f"{a} * {b} = {a*b}"

@app.get("/<int(signed=True):a>/over/<int(signed=True):b>")
def divide(a, b):
    return f"{a} / {b} = {a/b}"

if __name__ == "__main__":
    app.run()
