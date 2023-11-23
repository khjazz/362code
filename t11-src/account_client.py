# File: account_client.py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for operation, amount in (("deposit", 50), ("withdraw", 60),
                          ("deposit", 50), ("withdraw", 60)):
    request = {"operation": operation, "amount": amount}
    socket.send_json(request)
    print("Request:", request)
    reply = socket.recv_json()
    print("Reply:", reply)
