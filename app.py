from flask import Flask, render_template, request, jsonify, make_response, abort, redirect, url_for

from models import todos
from forms import LibraryForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "feather"

@app.route("/library/", methods=["GET"])
def library_list():
    form = LibraryForm()
    if "id_" in todos.all():
        fin_todos = [todos.all()]
    else:
        fin_todos = todos.all()
    return render_template("todos.html", form=form, todos=fin_todos)

@app.route("/library/", methods=["POST"])
def library_list_post():
    form=LibraryForm()
    todo=form.data
    if 'id_' in todos.all():
        todo["id_"] = todos.all()['id_'] + 1
    elif todos.all():
        todo["id_"] = todos.all()[-1]['id_'] + 1
    else:
        todo["id_"] = 1
    todos.create(todo)
    return redirect(url_for("library_list"))

@app.route("/library/<int:todo_id>/", methods=["GET"])
def todo_details(todo_id):
    todo = todos.get(todo_id)
    form = LibraryForm(data=todo)
    if not todo:
        abort(404)
    return render_template("todo.html", form=form, todo_id=todo_id)

@app.route("/library/<int:todo_id>/", methods=["POST"])
def todo_details_post(todo_id):
    todo = todos.get(todo_id)
    form = LibraryForm(data=todo)
    if form.validate_on_submit():
            todos.update(todo_id, form.data)
    return redirect(url_for("library_list"))

@app.route("/library/del/<int:todo_id>/", methods=['POST'])
def delete_todo(todo_id):
    todos.delete(todo_id)
    return redirect(url_for("library_list"))

@app.route("/library/delall/", methods = ["POST"])
def delete_all():
    todos.del_all()
    return redirect(url_for("library_list"))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)