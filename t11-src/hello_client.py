# File: hello_client.py
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for i in range(10):
    request = f"#{i} hello"
    socket.send_string(request)
    print("Client sent:", request)
    reply = socket.recv_string()
    print("Client received:", reply)
