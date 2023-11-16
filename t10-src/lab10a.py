# File: lab10a.py

# Replace the following by your full name and 8-digit student number
student_name = "Tsang Ka Ho"
student_id = "12621133"

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
        """verifies a successful update operation"""
        # 1 create a new todo item, keep its id (refer delete TC)
        create_resp = ws_client(f"http://{SERVER}/api/todos",
                "POST", {"desc": "to be updated"})
        id = create_resp["id"]
        # 2 get a list of all todos (refer delete TC)
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        original_size = len(list_resp)
        # 3 send update request
        #   require 3 things:
        #   url:
        #   http method: PUT
        #   JSON request data: (refer create TC)
        resp_data = ws_client(f"http://{SERVER}/api/todos/{id}",
                "PUT", {"desc": "updated"})
        # 4 check/assert update result
        self.assertEqual("updated", resp_data["desc"])
        # 4a more check
        self.assertNotEqual("to be updated", resp_data["desc"])
        # 5 get and keep a list of all todos (refere delete TC)
        new_resp_list = ws_client(f"http://{SERVER}/api/todos") 
        final_size = len(new_resp_list)
        self.assertEqual(original_size, final_size)
        # 6 check/assert updated item in second list
        # 7! do more proper checking/assertions

    def test_update_todo_invalid_desc(self):
        pass

    def test_update_todo_invalid_id(self):
        pass
        


if __name__ == "__main__":
    unittest.main()
