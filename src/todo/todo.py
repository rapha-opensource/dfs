from logging import getLogger
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
    value = args.get(param, default)
    if value:
        try:
            value = int(value)
        except ValueError:
            value = default
    return value


@bp.route('/lists', methods=('GET', 'POST'))
def lists():
    if request.method == 'POST':
        pass
        #input_data = request.get_json()
        #if 'name' not in input_data or 'description' not in input_data:
            #abort(400)

        #name = input_data['name']
        #description = input_data['description']
        #db = get_db()
        #error = None

        #if not name:
            #abort(400)
        #elif db.execute(
            #'SELECT id FROM todo_list WHERE name = ?', (name,)
        #).fetchone() is not None:
            #abort(409)
        #db.execute(
            #'INSERT INTO todo_list (name, description) VALUES (?, ?)',
            #(name, description)
        #)
        #db.commit()
    elif request.method == 'GET':
        searchString = request.args.get('searchString', None)
        skip = _int(request.args, 'skip')
        limit = _int(request.args, 'limit', default=-1)
        db = get_db()
        select = 'SELECT id, name, description from todo_list'
        if searchString:
            select += f' WHERE name LIKE "{searchString}"'
        select += f' LIMIT {limit} OFFSET {skip}'
        #print(f'SQL: {select}')
        lists = db.execute(select)
        return jsonify( [ dict(zip(todo_list.keys(), todo_list)) for todo_list in lists ] )


@bp.route('/list/<list_id>')
def todo_list(list_id):
        db = get_db()
        todo_list = db.execute('SELECT id, name, description from todo_list WHERE id=?', (list_id,)).fetchone()
        if not todo_list:
            abort(404)
        tasks = db.execute('SELECT id, name, completed from task WHERE list_id=?', (list_id,))
        return jsonify(
            id=todo_list[0],
            name=todo_list[1],
            description=todo_list[2],
            tasks=[ dict(zip(task.keys(), task)) for task in tasks ]
        )


@bp.route('/list/<list_id>/tasks', methods=['POST'])
def add_new_task(list_id):
    db = get_db()
    todo_list = db.execute(
        'SELECT id FROM todo_list WHERE id=?', (list_id,)
    ).fetchone()
    print(f'>> {todo_list}')
    if not todo_list:
        abort(404)
    input_data = request.get_json()
    if 'name' not in input_data:
        abort(400)
    name = input_data['name']
    if not name or not isinstance(name, str):
        abort(400)
    elif db.execute(
        'SELECT id FROM todo_list WHERE name=?', (name,)
    ).fetchone() is not None:
        abort(409)
    task_id = uuid4().hex
    db.execute(
        'INSERT INTO task (id, list_id, name) VALUES (?,?,?)',
        (task_id, list_id, name)
    )
    db.commit()
    return jsonify(
        {
            'id': task_id,
            'name': name,
            'completed': False
        }
    ), 201
