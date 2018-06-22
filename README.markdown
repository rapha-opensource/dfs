# ToDo List Web Server

Please read ./docs/design.markdown for notes on design choices.

# Development Installation

```bash
# first create a virtual environment

python3 -m venv ~/venv

. ~/venv/bin/activate

# install the server in development mode:

python setup.py develop

# set the Flask app name in the environment

export FLASK_APP=todo

# initialize the database

flask init-db


# launch the server

flask run

```

## Testing

### Install the unit test frame and the code coverage too

```bash
pip install -U pip pytest coverage
```

### Execute all the tests
```bash
pytest
```

### Produce a coverage report
```bash
coverage run -m pytest
coverage report
```

## Deploy to production

### Build and install
The main idea here is to produce a Python wheel file.
That file can be installed inside a container in a virtual environment.

```bash
pip install wheel
python setup.py bdist_wheel

# will produce a dist/todo-1.0.0-py3-none-any.whl file

# inside the container, this file can be installed:

pip install todo-1.0.0-py3-none-any.whl
```
