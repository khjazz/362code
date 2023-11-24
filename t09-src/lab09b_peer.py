# File: lab09b.py

# Replace the following by your full name and 8-digit student number
student_name = "LIN Junming"
student_id = "13028624"

# Write code below
import json
from urllib.request import Request, urlopen

SERVER = "localhost:5000"
JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

def makeDepositRequest(amount):
    data = {"amount" : amount}
    req = Request(url = f"http://{SERVER}/deposit",
        data = json.dumps(data).encode(),
        headers = {"Content-type": JSON_CONTENT_TYPE},
        method="POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

def makeWithdrawRequest(amount):
    data = {"amount" : amount}
    req = Request(url = f"http://{SERVER}/withdraw",
        data = json.dumps(data).encode(),
        headers = {"Content-type": JSON_CONTENT_TYPE},
        method="POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

if __name__ == "__main__":
    testCases = [ [makeDepositRequest, 1000],
                  [makeWithdrawRequest, 700],
                  [makeWithdrawRequest, 700],
                  [makeDepositRequest, "1"],
                  [makeDepositRequest, -1],
                  [makeDepositRequest, ""],
                  [makeWithdrawRequest, "1"],
                  [makeWithdrawRequest, -1],
                  [makeWithdrawRequest, ""],
                  [makeWithdrawRequest, 300] ]
    for operation, amount in testCases:
        try:
            print(operation(amount))
        except Exception as e:
            print(e)    
