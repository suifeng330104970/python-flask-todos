"""
todos module
Tom Slankard <tom.slankard@here.com>

Simple Flask app for managing a todo list.
"""

# pylint: disable=no-member

import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import pkg_resources

app = Flask(__name__)
db_path = pkg_resources.resource_filename('todos', 'todos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)


class Todo(db.Model):

    """ORM for a todo item, which in this case,
    consists only of a string, a completed flag,
    and an integer primary key."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __init__(self, text):
        self.text = text
        self.completed = False


@app.route('/')
def index():
    """Merely redirects to /todos"""
    return redirect(url_for('todos'))


@app.route('/todos', methods=['GET', 'POST'])
def todos():
    """Display a list of todos, or create a new todo and display the list
    depending on whether the form was submitted."""
    if request.method == 'GET':
        return render_template("todos.html", todos=Todo.query.all())
    elif request.method == 'POST':
        new_todo = Todo(request.form['text'])
        db.session.add(new_todo)
        db.session.commit()
        return render_template("todos.html", todos=Todo.query.all())
    flask.abort(405)  # method not allowed


@app.route('/todos/<id>/complete')
def complete_todo(id):
    """Sets completed to true for the specified todo item."""
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos'))


@app.route('/todos/<id>/uncomplete')
def uncomplete_todo(id):
    """Sets completed to false for the specified todo item."""
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = False
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos'))


@app.route('/remove_completed')
def remove_completed():
    """Removes all completed todo items."""
    todos = Todo.query.filter_by(completed=True).all()
    for todo in todos:
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos'))


def main():
    """Initialize the database and run the Flask server."""
    db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    main()
