# File: lab10b.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

import json
from urllib.request import urlopen
from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/api/plus/<int:a>/<int:b>")
def add_ws(a, b):  # web service
    return jsonify({"result": a+b})

# Modify code below

# step 1
def call_ws(a, b):
    """ Invokes the web service provided by add_ws() to calculate
    the sum of a and b, and returns the sum as an integer; it is
    not a view function and has no decorator.
    """
    # NOT call add_ws(a, b) directly
    # move most of the given add2(a, b) here and modify
    with urlopen(f"http://localhost:5000/api/plus/{a}/{b}") as resp:
        resp_json = resp.read().decode()
    resp_data = json.loads(resp_json)
    result = resp_data["result"]
    return result

# step 2
@app.get("/plus/<int:a>/<int:b>")
def add2(a, b):  # web application
    result = call_ws(a, b)
    return f"{a} + {b} = {result}"

# step 3: add3(a, b, c)
@app.get("/plus/<int:a>/<int:b>/<int:c>")
def add3(a, b, c):
    result1 = call_ws(a, b)
    result2 = call_ws(result1, c)
    return f"{a} + {b} + {c} = {result2}"

if __name__ == "__main__":
    app.run()
