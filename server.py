#!flask/bin/python
from flask import Flask, jsonify, abort, url_for


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def index():
    #abort(404)
    #return jsonify(tasks)
    return url_for('get_task', task_id=3, _external=True)

@app.route('/get/<task_id>')
def get_task(task_id):
  return task_id

if __name__ == '__main__':
    app.run(debug=True)
