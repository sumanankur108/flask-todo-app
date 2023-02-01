import json

from flask import Flask, render_template, request as req, redirect, url_for

app = Flask(__name__)

todo_lists: dict[str, list[str, ...]] = {
    "default": ["Buy guide for Flask", "Read guide for Flask", "Learn Flask"]
}


@app.route("/")
def index():
    return render_template(
        "list.html",
        kind_of_list="default",
        todo_list=todo_lists["default"]
    )


@app.route("/<list_type>", methods=["GET"])
def get_list(list_type: str):
    # check if current list_type is in todo_list
    if list_type.lower() in todo_lists.keys():
        return render_template(
            "list.html",
            kind_of_list=list_type,
            todo_list=todo_lists[list_type]
        )
    else:
        todo_lists[list_type] = []
        return render_template(
            "list.html",
            kind_of_list=list_type,
            todo_list=todo_lists[list_type]
        )


@app.route("/", methods=["POST"])
def post_list():
    list_type: str = req.form["list_type"]

    # check if current list_type exists in todo_lists
    if list_type not in todo_lists.keys():
        return "<h1>Invalid List</h1>"

    new_todo: str = req.form["new_todo"]
    todo_lists[list_type].append(new_todo)
    return redirect(url_for("get_list", list_type=list_type)), 301


@app.route("/api/list")
def get_list_json():
    return json.dumps(todo_lists)
