import os
import tempfile

import pytest
from todo import create_app
from todo.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    '''
    yields a Flask() object initialized with a temporary database
    and some test data coming from 'data.sql'
    '''
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    '''
    returns a Flask test_client object to call the Flask server
    '''
    return app.test_client()


@pytest.fixture
def runner(app):
    '''
    returns a Flask CLI runner
    '''
    return app.test_cli_runner()
