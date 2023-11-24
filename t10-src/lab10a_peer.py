# File: lab10a.py

# Replace the following by your full name and 8-digit student number
student_name = "Chan Tai Man"
student_id = "01234567"

import json, time, unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

SERVER = "localhost:5000"

def ws_client(url, method=None, data=None):
    if not method:
        method = "POST" if data else "GET"
    if data:
        data = json.dumps(data).encode()
    headers = {"Content-type": "application/json; charset=UTF-8"} \
                if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    return result

class TestTodoServer(unittest.TestCase):
    def test_create_todo_item(self):
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        num_before_create = len(list_resp)
        create_resp = ws_client(f"http://{SERVER}/api/todos",
                "POST", {"desc": "create me"})
        self.assertEqual("create me", create_resp["desc"])
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        self.assertEqual(num_before_create + 1, len(list_resp))
        self.assertIn(create_resp, list_resp)

    def test_create_todo_error(self):
        with self.assertRaises(HTTPError) as cm:
            ws_client(f"http://{SERVER}/api/todos",
                    "POST", {"desc": " "})
        self.assertEqual(400, cm.exception.code)

    def test_delete_todo_item(self):
        create_resp = ws_client(f"http://{SERVER}/api/todos",
                "POST", {"desc": "delete me"})
        id = create_resp["id"]
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        num_before_delete = len(list_resp)
        self.assertIn(create_resp, list_resp)
        delete_resp = ws_client(f"http://{SERVER}/api/todos/{id}",
                "DELETE")
        self.assertEqual({}, delete_resp)
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        self.assertEqual(num_before_delete - 1, len(list_resp))
        self.assertNotIn(create_resp, list_resp)

    def test_delete_todo_error(self):
        with self.assertRaises(HTTPError) as cm:
            ws_client(f"http://{SERVER}/api/todos/999", "DELETE")
        self.assertEqual(404, cm.exception.code)

# Modify code below

class TestTodoServerUpdate(unittest.TestCase):
    def test_update_todo_item(self):
        createResp = ws_client(f"http://{SERVER}/api/todos", "POST", {"desc": "testing"})
        id = createResp["id"]
        listResp = ws_client(f"http://{SERVER}/api/todos")
        numBeforeCreate = len(listResp)
        updateResp = ws_client(f"http://{SERVER}/api/todos/{id}", "PUT", {"desc": "update testing"})
        self.assertEqual("update testing", updateResp["desc"])
        listResp = ws_client(f"http://{SERVER}/api/todos")
        self.assertNotIn(createResp, listResp)
        self.assertIn(updateResp, listResp)
        self.assertEqual(numBeforeCreate, len(listResp))
        
    def test_update_todo_invalid_desc(self):
        createResp = ws_client(f"http://{SERVER}/api/todos", "POST", {"desc": "testing"})
        id = createResp["id"]
        with self.assertRaises(HTTPError) as cm:
            ws_client(f"http://{SERVER}/api/todos/{id}", "PUT", {"desc": ""})
        self.assertEqual(400, cm.exception.code)
        
    def test_update_todo_invalid_id(self):
        with self.assertRaises(HTTPError) as cm:
            ws_client(f"http://{SERVER}/api/todos/999", "PUT", {"desc": "update invalid ID testing"})
        self.assertEqual(404, cm.exception.code) 

if __name__ == "__main__":
    unittest.main()
