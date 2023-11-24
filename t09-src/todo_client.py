# File: todo_client.py
import json
from urllib.request import Request, urlopen

SERVER = "localhost:5000"
JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

def get_all_todos():
    with urlopen(f"http://{SERVER}/api/todos") as resp:
        result = json.loads(resp.read().decode())
    return result

def delete_todo(id):
    req = Request(url = f"http://{SERVER}/api/todos/{id}",
                  method = "DELETE")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

def create_todo(desc):
    data = { "desc" : desc }
    req = Request(url = f"http://{SERVER}/api/todos",
            data = json.dumps(data).encode(),
            headers = {"Content-type": JSON_CONTENT_TYPE},
            method = "POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

if __name__ == "__main__":
    print(get_all_todos())
    food = create_todo("Buy food")
    print(get_all_todos())
    delete_todo(food["id"])
    print(get_all_todos())
    try:
        print(create_todo(""))
    except Exception as e:
        print(e)
    try:
        print(delete_todo(999))
    except Exception as e:
        print(e)
