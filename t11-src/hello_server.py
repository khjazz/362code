# File: hello_server.py
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv_string()
    time.sleep(0.1)
    socket.send_string(message + " world")
