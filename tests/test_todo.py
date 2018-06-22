from json import dumps
from pprint import pprint


def test_get_all_lists(client):
    response = client.get('/todo/1.0.0/lists')
    assert response.is_json
    lists = response.get_json()
    assert isinstance(lists, list)
    assert len(lists) == 2
    pprint(lists)
    for todo_list in lists:
        assert 'id' in todo_list
        assert 'name' in todo_list
        assert 'description' in todo_list
        if todo_list['id'] == 'a4e0e3bd8a0d45a9969074bdf4253852':
            assert 'tasks' in todo_list
            tasks = todo_list['tasks']
            assert len(tasks) == 3
        else:
            assert len(todo_list['tasks']) == 1


def test_get_lists_limit(client):
    limit=1
    lists = client.get(f'/todo/1.0.0/lists?limit={limit}').get_json()
    assert len(lists) == limit


def test_get_lists_skip(client):
    skip = 1
    lists = client.get(f'/todo/1.0.0/lists?skip={skip}').get_json()
    assert len(lists) == 1


def test_get_lists_skip_bad_value(client):
    # a bad skip will be treated as a 0
    skip = 'foobar'
    response = client.get(f'/todo/1.0.0/lists?skip={skip}')
    assert response.status_code == 200


def test_get_lists_search(client):
    searchString = 'mama'
    lists = client.get(f'/todo/1.0.0/lists?searchString={searchString}').get_json()
    assert len(lists) == 1


def test_get_one_list(client):
    list_id = 'a4e0e3bd8a0d45a9969074bdf4253852'
    response = client.get(f'/todo/1.0.0/list/{list_id}')
    assert response.is_json
    todo_list = response.get_json()
    assert 'id' in todo_list
    assert todo_list['id'] == list_id
    assert 'name' in todo_list
    assert todo_list['name'] == 'mama'
    assert 'description' in todo_list
    assert todo_list['description'] == 'house needs'
    assert 'tasks' in todo_list
    tasks = todo_list['tasks']
    assert len(tasks) == 3
    task0, task1, task2 = tasks
    assert 'id' in task0
    assert task0['id'] == '7f42c4ce43d44ca291eff92017966a28'
    assert 'name' in task0
    assert task0['name'] == 'get milk'
    assert 'completed' in task0
    assert isinstance(task0['completed'], bool)
    assert not task0['completed']
    assert task1['name'] == 'get sugar'
    assert task1['completed']


def test_get_one_list_not_found(client):
    list_id = 'foobar'
    response = client.get(f'/todo/1.0.0/list/{list_id}')
    assert response.status_code == 404


def test_post_task(client):
    list_id = 'e8f83d1b5d3e437d8674a93cd9087a2b'
    task_name = 'get salad'
    completed = True
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': task_name,
                'completed': completed
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.is_json
    new_task = response.get_json()
    assert 'id' in new_task
    assert 'name' in new_task
    assert new_task['name'] == task_name
    assert 'completed' in new_task
    assert isinstance(new_task['completed'], bool)
    assert new_task['completed'] == completed


def test_post_task_list_not_found(client):
    list_id = 'foobar'
    task_name = 'get salad'
    completed = True
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': task_name,
                'completed': completed
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 404


def test_post_task_missing_field(client):
    list_id = 'e8f83d1b5d3e437d8674a93cd9087a2b'
    task_name = 'get salad'
    completed = True
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': task_name,
                # missing 'completed' field here
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_post_task_completed_wrong_type(client):
    list_id = 'e8f83d1b5d3e437d8674a93cd9087a2b'
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': 'get salad',
                'completed': 'foobar'
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_post_task_already_exists(client):
    list_id = 'e8f83d1b5d3e437d8674a93cd9087a2b'
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': 'get beer',
                'completed': False
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 409


def test_post_task_completed(client):
    list_id = 'a4e0e3bd8a0d45a9969074bdf4253852'
    task_id = '7f42c4ce43d44ca291eff92017966a28'
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/task/{task_id}/complete',
        data=dumps(
            {
                'completed': True
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.is_json
    result = response.get_json()
    assert 'completed' in result
    assert isinstance(result['completed'], bool)
    assert result['completed']


def task_complete_negative_test(
    client,
    expected_status_code,
    task_id='7f42c4ce43d44ca291eff92017966a28',
    data={ 'completed': True },
):
    list_id = 'a4e0e3bd8a0d45a9969074bdf4253852'
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/task/{task_id}/complete',
        data=dumps(data),
        content_type='application/json'
    )
    assert response.status_code == expected_status_code


def test_task_completed_task_not_found(client):
    task_complete_negative_test(
        client,
        404,
        task_id='foobar',
    )


def test_post_task_completed_invalid_input_data(client):
    task_complete_negative_test(
        client,
        400,
        data={ 'completed': 'foobar' }
    )

def test_post_task_completed_missing_input_data(client):
    task_complete_negative_test(
        client,
        400,
        data={ 'foo': 'bar' }
    )


def test_new_list(client):
    new_list_input = {
        'name': 'foo',
        'description': 'bar',
        'tasks': [
            {
                'name': 'get chocolate',
                'completed': False
            },
            {
                'name': 'get wine',
                'completed': True
            }
        ]
    } 
    response = client.post(
        '/todo/1.0.0/lists',
        data=dumps(new_list_input),
        content_type='application/json'
    )
    assert response.is_json
    new_list = response.get_json()
    assert new_list_input['name'] == new_list['name']
    assert new_list_input['description'] == new_list['description']
    assert len(new_list_input['tasks']) == len(new_list['tasks'])
    for i in range(len(new_list['tasks'])):
        for field in ('name', 'completed'):
            assert new_list['tasks'][i][field] == new_list_input['tasks'][i][field]
    assert isinstance(new_list['tasks'][0]['completed'], bool)


def test_new_list_missing_name(client):
    new_list_input = {
        # missing 'name' field here
        'description': 'bar',
        'tasks': [
            {
                'name': 'get chocolate',
                'completed': False
            },
        ]
    } 
    response = client.post(
        '/todo/1.0.0/lists',
        data=dumps(new_list_input),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_new_list_tasks_not_a_sequence(client):
    new_list_input = {
        'name': 'foo',
        'description': 'bar',
        'tasks': 'not_a_sequence'
    } 
    response = client.post(
        '/todo/1.0.0/lists',
        data=dumps(new_list_input),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_new_list_tasks_incomplete(client):
    new_list_input = {
        'name': 'foo',
        'description': 'bar',
        'tasks': [
            {
                'name': 'get wine',
                # missing 'completed' field
            }
        ]
    } 
    response = client.post(
        '/todo/1.0.0/lists',
        data=dumps(new_list_input),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_new_list_duplicate_name(client):
    new_list_input = {
        'name': 'mama',
        'description': 'bar',
        'tasks': []
    } 
    response = client.post(
        '/todo/1.0.0/lists',
        data=dumps(new_list_input),
        content_type='application/json'
    )
    assert response.status_code == 409
