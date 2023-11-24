# File: urlopen_eg.py
from urllib.request import Request, urlopen
SERVER = "jsonplaceholder.typicode.com"

# Code segment #1
req = Request(url = f"https://{SERVER}/todos/1")
with urlopen(req) as resp:
    print(resp.getcode(), resp.read().decode())

# Code segment #2
req = Request(url = f"https://{SERVER}/todos", data = b"hello")
with urlopen(req) as resp:
    print(resp.getcode(), resp.read().decode())
