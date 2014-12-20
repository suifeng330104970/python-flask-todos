"""
test.py
Tom Slankard <tom.slankard@here.com>
tests for todo app
"""

import os
import unittest
import tempfile

from todos import app, db, Todo

#  rather than hitting the "real" database,
#  let's use a memory database for testing purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

class TodosTest(unittest.TestCase):
    """Run tests on the main features of the todos app"""

    def setUp(self):
        db.create_all()

        #  create a test client for the Flask server
        self.test_client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_post(self):
        """When we POST to /todos, a new Todo item should appear in the DB."""
        data = {'text':'some text'}
        self.test_client.post('/todos', data=data)
        todos_list = Todo.query.all()
        assert len(todos_list) == 1
        assert todos_list[0].text == 'some text'
        assert todos_list[0].completed == False

    def test_complete_uncomplete(self):
        """When we mark a Todo as [un]completed, the database should reflect the change."""
        data = {'text':'some text'}
        self.test_client.post('/todos', data=data)
        todos_list = Todo.query.all()
        assert len(todos_list) == 1
        assert todos_list[0].completed == False
        self.test_client.get('/todos/' + str(todos_list[0].id) + '/complete')
        todos_list = Todo.query.all()
        self.test_client.get('/todos/' + str(todos_list[0].id) + '/uncomplete')
        todos_list = Todo.query.all()
        assert todos_list[0].completed == False

    def test_remove_completed(self):
        """When we click the remove completed link the database should contain no
        completed Todo items."""
        foo = Todo('foo')
        foo.completed = True
        db.session.add(foo)
        bar = Todo('bar')
        db.session.add(bar)
        db.session.commit()
        self.test_client.get('/remove_completed')
        todos_list = Todo.query.all()
        assert len(todos_list) > 0
        for todo in todos_list:
            assert todo.completed == False

if __name__ == '__main__':
    unittest.main()
