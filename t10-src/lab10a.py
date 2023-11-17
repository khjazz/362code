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
        original_desc = "to be updated" # desc
        create_resp = ws_client(f"http://{SERVER}/api/todos",
                "POST", {"desc": original_desc})
        id = create_resp["id"]  # id
        # 2 get a list of all todos (refer delete TC)
        list_resp = ws_client(f"http://{SERVER}/api/todos")
        original_list_size = len(list_resp) # length
        # 3 send update request
        #   require 3 things:
        #   url:
        #   http method: PUT
        #   JSON request data: (refer create TC)
        update_resp = ws_client(f"http://{SERVER}/api/todos/{id}",
                "PUT", {"desc": "updated"})
        # 4 check/assert update result
        self.assertEqual("updated", update_resp["desc"])
        # 4a more check
        self.assertNotEqual(original_desc, update_resp["desc"])
        # 5 get and keep a list of all todos (refere delete TC)
        resp_list2 = ws_client(f"http://{SERVER}/api/todos") 
        self.assertEqual(original_list_size, len(resp_list2))
        # 6 check/assert updated item in second list
        updated_item = {}
        for item in resp_list2:
            if item["id"] == id:
                updated_item = item
        self.assertEqual("updated", updated_item["desc"])
        # 7! do more proper checking/assertions
        self.assertNotEqual(original_desc, updated_item["desc"])

    def test_update_todo_invalid_desc(self):
        """
        verifies a failed update operation due to invalid
        desc data in input data (e.g. a blank string)
        """
        original_desc = "created item"
        create_resp = ws_client(f"http://{SERVER}/api/todos",
                "POST", {"desc": original_desc})
        id = create_resp["id"]
        # error code should be 400
        desc_list = [" ", "", None, []]
        for desc in desc_list:
            with self.assertRaises(HTTPError) as cm:
                ws_client(f"http://{SERVER}/api/todos/{id}",
                        "PUT", {"desc": desc})
            self.assertEqual(400, cm.exception.code)
        # should not be updated
        resp_list = ws_client(f"http://{SERVER}/api/todos")
        updated_item = {}
        for item in resp_list:
            if item["id"] == id:
                updated_item = item
        self.assertEqual(original_desc, updated_item["desc"])

    def test_update_todo_invalid_id(self):
        """
        verifies a failed update operation due to an invalid
        ID (e.g. 999, assumed to be a non-existing ID)
        """
        # error code should be 404
        id_list = [999, 30000, 1e8]
        for id in id_list:
            with self.assertRaises(HTTPError) as cm:
                ws_client(f"http://{SERVER}/api/todos/{id}",
                        "PUT", {"desc": "trying to update"})
            self.assertEqual(404, cm.exception.code)


if __name__ == "__main__":
    unittest.main()
