from collections.abc import Sequence
from logging import getLogger
from pprint import pprint
from sqlite3 import DatabaseError
from uuid import uuid4

from flask import (
    abort,
    Blueprint,
    g,
    redirect,
    request,
    session,
    url_for
)
from flask.json import jsonify

from todo.db import get_db


log = getLogger(__name__)


bp = Blueprint('todo', __name__, url_prefix='/todo/1.0.0')


def _int(args, param, default=0):
    '''
    Given a 'args' dict of str,
    converts the value associated with 'param' into a python int object or returns the 'default' value.
    '''
    value = args.get(param, default)
    if value:
        try:
            value = int(value)
        except ValueError:
            value = default
    return value


@bp.route('/lists')
def lists():
    '''
        Returns all of the available lists
    '''
    searchString = request.args.get('searchString', None)
    skip = _int(request.args, 'skip')
    limit = _int(request.args, 'limit', default=-1)
    db = get_db()
    select = 'SELECT {columns} FROM todo_list'
    if searchString:
        select += f' WHERE name LIKE "{searchString}"'
    select += ' LIMIT :limit OFFSET :skip'
    #print(f'SQL: {select}')
    limit_skip = {
        'limit': limit,
        'skip': skip
    }
    todo_list_rows = db.execute(
        select.format(columns='id, name, description'),
        limit_skip
    )
    select_tasks = f'SELECT * FROM task WHERE list_id IN ({select.format(columns="id")})'
    #print(f'select tasks: {select_tasks}')
    tasks = tuple(
        dict(
            task_row,
            completed=bool(task_row['completed'])
        )
        for task_row in db.execute(select_tasks, limit_skip)
    )
    return jsonify(
        tuple(
            dict(
                todo_list_row,
                tasks=tuple(
                    task for task in tasks if task['list_id'] == todo_list_row['id']
                )
            )
            for todo_list_row in todo_list_rows
        )
    )


@bp.route('/lists', methods=['POST'])
def new_list():
    '''
        Creates a new list
    '''
    input_data = request.get_json()
    # first, validate the input data
    if not set(('name', 'description')) < set(input_data.keys()):
        abort(400) 
    if 'tasks' in input_data:
        tasks = input_data['tasks']
        if not isinstance(tasks, list):
            abort(400)
        for task in tasks:
            if set(task.keys()) < set(('name', 'completed')):
                abort(400)
    # first create the new list
    name = input_data['name']
    description = input_data['description']
    db = get_db()
    if db.execute('SELECT id FROM todo_list WHERE name = ?', (name,)).fetchone():
        abort(409)
    list_id = uuid4().hex
    input_data['id'] = list_id
    db.execute(
        'INSERT INTO todo_list (id, name, description) VALUES (?, ?, ?)',
        (list_id, name, description)
    )
    # if the input data contained tasks, go ahead and create them
    if 'tasks' in input_data:
        params = []
        for task in input_data['tasks']:
            # save the generated ids into input_data
            # so we can serialize it as the response
            task['id'] = uuid4().hex
            task['list_id'] = list_id
            params.append(tuple(task.values()))
        db.executemany(
            'INSERT INTO task VALUES (?, ?, ?, ?)',
            params
        )
    db.commit()
    return jsonify(input_data)


@bp.route('/list/<list_id>')
def todo_list(list_id):
    '''
        Return the specified todo list
    '''
    db = get_db()
    todo_list_row = db.execute('SELECT id, name, description from todo_list WHERE id=?', (list_id,)).fetchone()
    if not todo_list_row:
        abort(404)
    tasks_rows = db.execute('SELECT id, name, completed from task WHERE list_id=?', (list_id,))
    # the following lines:
    # . convert todo_list_row into a JSON-serializable dict
    # . add a 'tasks' field to this dict
    # . convert task_row into a JSON-serializable dict and 'completed' column value into bool
    return jsonify(
        dict(
            todo_list_row,
            tasks= tuple(
                dict(
                    task_row,
                    completed=bool(task_row['completed'])
                ) for task_row in tasks_rows
            )
        )
    )


@bp.route('/list/<list_id>/tasks', methods=['POST'])
def add_new_task(list_id):
    '''
        Add a new task to the todo list
    '''
    db = get_db()
    todo_list = db.execute(
        'SELECT id FROM todo_list WHERE id=?', (list_id,)
    ).fetchone()
    if not todo_list:
        abort(404)
    input_data = request.get_json()
    if set(input_data.keys()) < set(('name', 'completed')):
        abort(400)
    name, completed = map(lambda k: input_data[k], ('name', 'completed'))
    if not name or not isinstance(name, str) or not isinstance(completed, bool):
        abort(400)
    elif db.execute(
        'SELECT id FROM task WHERE name=?', (name,)
    ).fetchone():
        abort(409)
    task_id = uuid4().hex
    db.execute(
        'INSERT INTO task (id, list_id, name, completed) VALUES (?,?,?,?)',
        (task_id, list_id, name, completed)
    )
    db.commit()
    input_data['id'] = task_id
    input_data['list_id'] = list_id
    return jsonify(input_data), 201


@bp.route('/list/<list_id>/task/<task_id>/complete', methods=['POST'])
def set_task_completed(list_id, task_id):
    '''
        Updates the completed state of a task
    '''
    db = get_db()
    task = db.execute(
        'SELECT id FROM task WHERE id=? AND list_id=?',
        (task_id, list_id)
    ).fetchone()
    if not task:
        abort(404)
    input_data = request.get_json()
    if 'completed' not in input_data:
        abort(400)
    completed = input_data['completed']
    if not isinstance(completed, bool):
        abort(400)
    db.execute(
        'UPDATE task SET completed=? WHERE id=? AND list_id=?',
        (completed, task_id, list_id)
    )
    db.commit()
    return jsonify( { 'completed': completed } )
