# File: lab11b.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

# Write code below
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


class Account():
    _DEPOSIT = 'deposit'
    _WITHDRAW = 'withdraw'

    def __init__(self):
        self._balance = 0

    def get_balance(self):
        return self._balance

    def _deposit(self, amount):
        self._balance += amount

    def _withdraw(self, amount):
        self._balance -= amount

    def handle_request(self, obj, socket):
        op = obj["operation"]
        amount = obj["amount"]
        if op == self._DEPOSIT:
            self._deposit(amount)
            socket.send_json({"status": "success", "balance": self.get_balance()})
        elif op == self._WITHDRAW:
            if self.get_balance() >= amount:
                self._withdraw(amount)
                socket.send_json({"status": "success", "balance": self.get_balance()})
            else:
                socket.send_json({"status": "failure (insufficient funds)", "balance": self.get_balance()})

account = Account()
while True:
    obj = socket.recv_json()
    account.handle_request(obj, socket)

"""
Write a ZeroMQ request-reply server to perform deposit and withdrawal operations on an account
using JSON messages. The account balance, deposit amounts and withdrawal amounts are integers.
A withdrawal is only carried out when the existing balance is sufficient, i.e. when balance >= amount.
In other words, the balance must be positive or zero at any time. The operations are described as
follows.
The request data for a deposit operation has the JSON format: {"operation": "deposit",
"amount": x }, where x is a positive integer or zero. Upon receiving such a request, the server
updates the balance and returns the JSON message { "status": "success", "balance": x },
where x is the current balance.
The request data for a withdrawal operation has the JSON format: {"operation": "withdraw",
"amount": x }, where x is a positive integer or zero. Upon receiving such a request, the server does
the following:
• If the balance is sufficient for the withdrawal amount, the server updates the balance and
returns the JSON message { "status": "success", "balance": x }, where x is the current balance.
• If the balance is insufficient for the withdrawal amount, the server returns the JSON message
{ "status": "failure (insufficient funds)", "balance": x }, where x is the current balance.
Use the TCP port 5555. No validation of the request data is required.
Write the program in the lab11b.py file for submission. Remember to enforce good programming
style in your code.
"""