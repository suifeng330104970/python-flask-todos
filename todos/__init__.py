import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import pkg_resources

app = Flask(__name__)
db_path = pkg_resources.resource_filename('todos', 'todos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path 
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __init__(self, text):
        self.text = text
        self.completed = False


@app.route('/')
def index():
    return redirect(url_for('todos'))


@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        return render_template("todos.html", todos=Todo.query.all())
    elif request.method == 'POST':
        new_todo = Todo(request.form['text'])
        db.session.add(new_todo)
        db.session.commit()
        return render_template("todos.html", todos=Todo.query.all())
    flask.abort(405) # method not allowed


@app.route('/todos/<id>/complete')
def complete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos'))

    
@app.route('/todos/<id>/uncomplete')
def uncomplete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = False
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todos'))


@app.route('/remove_completed')
def remove_completed():
    todos = Todo.query.filter_by(completed=True).all()
    for todo in todos:
        db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos'))

def main():
    db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    main()
