# File: todo.py
from flask import (Flask, redirect, render_template_string,
                   request, url_for)
app = Flask(__name__)

template_str = """
<h2>Todo list</h2>
<table>
{% for id, item, url in todos %}
<tr>
  <td>({{id+1}})</td>
  <td>{{item}}</td>
  <td><a href="{{url}}">Delete</a></td>
</tr>
{% endfor %}
</table>
<hr />
<form action="/add" method="POST">
  <input type="text" name="desc" />
  <input type="submit" value="Add" />
</form>
"""

todo = []

@app.route("/")
def todo_display():
    todos = [(id, desc, url_for("todo_delete", id=id))
            for id, desc in enumerate(todo)]
    return render_template_string(template_str, todos=todos)

@app.route("/delete/<int:id>")
def todo_delete(id):
    todo.pop(id)
    return redirect("/")

@app.route("/add", methods=["POST"])
def todo_add():
    desc = request.form["desc"].strip()
    if desc:
        todo.append(desc)
    return redirect("/")

if __name__ == "__main__":
    app.run()
