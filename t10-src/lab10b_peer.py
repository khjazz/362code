# File: lab10b.py

# Replace the following by your full name and 8-digit student number
student_name = "Chan Tai Man"
student_id = "01234567"

import json
from urllib.request import urlopen
from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/api/plus/<int:a>/<int:b>")
def add_ws(a, b):  # web service
    return jsonify({"result": a+b})

# Modify code below

def call_ws(a, b):
    with urlopen(f"http://localhost:5000/api/plus/{a}/{b}") as resp:
        resp_json = resp.read().decode()
    resp_data = json.loads(resp_json)
    result = resp_data["result"]
    return result

@app.get("/plus/<int:a>/<int:b>")
def add2(a, b): # web application
    result = call_ws(a, b)
    return f"{a} + {b} = {result}"

@app.get("/plus/<int:a>/<int:b>/<int:c>")
def add3(a,b,c):
    result = call_ws(call_ws(a,b),c)
    return f"{a} + {b} + {c} = {result}"

if __name__ == "__main__":
    app.run()
