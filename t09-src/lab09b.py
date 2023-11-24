# File: lab09b.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Write code below
import json
from urllib.request import Request, urlopen

SERVER = "localhost:5000"
JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

def deposit(amount):
    data = { "amount" : amount }
    req = Request(url = f"http://{SERVER}/deposit",
            data = json.dumps(data).encode(),
            headers = {"Content-type": JSON_CONTENT_TYPE},
            method = "POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

def withdraw(amount):
    data = { "amount" : amount }
    req = Request(url = f"http://{SERVER}/withdraw",
            data = json.dumps(data).encode(),
            headers = {"Content-type": JSON_CONTENT_TYPE},
            method = "POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

if __name__ == "__main__":
    print(deposit(1000))
    print(withdraw(700))
    print(withdraw(700))
    try:
        print(deposit("1"))
    except Exception as e:
        print(e)
    try:
        print(deposit(-1))
    except Exception as e:
        print(e)
    try:
        print(deposit(None))
    except Exception as e:
        print(e)

    try:
        print(withdraw("1"))
    except Exception as e:
        print(e)
    try:
        print(withdraw(-1))
    except Exception as e:
        print(e)
    try:
        print(withdraw(None))
    except Exception as e:
        print(e)
    
    print(withdraw(300))
