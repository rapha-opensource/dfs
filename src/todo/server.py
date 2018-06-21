from configparser import ConfigParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from logging import getLogger, Formatter, StreamHandler
from sys import stdout
from uuid import uuid4


log = getLogger(__name__)


def log_to_stdout(level):
    root_logger = getLogger()
    root_logger.setLevel(level)
    streamingHandler = StreamHandler(stdout)
    streamingHandler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s %(message)s'
        )
    )
    root_logger.addHandler(streamingHandler)


class Task(object):

    def __init__(self, _id, name):
        '''
            _id:    UUID4 str object to uniquely identify this task.
            name:   a str object to describe the task to be accomplished.
        '''
        assert isinstance(_id, str)
        assert isinstance(name, str)
        self.id = _id
        self.name = name
        self.completed = False


class TodoList(object):

    def __init__(self, _id, name, description=None):
        '''
            _id:            UUID4 str object to act as the unique identifier for this list instance.
            name:           a short name to visually identify the list.
            description:    an optional description
        '''
        self.id = _id
        self.name = name
        self.description = description
        self.tasks = defaultdict(Task)

    def create(self, name):
        assert isinstance(name, str)
        _id = uuid4().hex
        self.tasks[_id] = _id, name


class AllTodoLists(object):

    def __init__(self, path):
        self.url = url
        self.lists = defaultdict(TodoList)

    def create(self, name, description=None):
        assert isinstance(name, str)
        if description:
            assert isinstance(description, str)
        _id = uuid4().hex
        self.lists[_id] = _id, name, description


def serve():
    conf = ConfigParser()
    conf.read(filenames=['conf/mesh.conf'])
    log_to_stdout(conf['log']['level'])
    inet = conf['inet']
    ip, port = inet['ip'], int(inet['port'])
    db_url = database['url']
    TodoRequestHandler.app = App(db_url)
    server = HTTPServer((ip, port), TodoRequestHandler)
    log.info(f'Todo List Server running at http://{ip}:{port}/')
    server.serve_forever() # TODO add ctrl-c support for cleaner exits...


if __name__ == '__main__':
    serve()

