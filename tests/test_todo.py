from json import dumps


def test_get_lists(client):
    response = client.get('/todo/1.0.0/lists')
    assert response.is_json
    lists = response.get_json()
    for todo_list in lists:
        assert 'id' in todo_list
        assert 'name' in todo_list
        assert 'description' in todo_list


def test_get_lists_limit(client):
    limit=1
    lists = client.get(f'/todo/1.0.0/lists?limit={limit}').get_json()
    assert len(lists) == limit


def test_get_lists_skip(client):
    skip = 1
    lists = client.get(f'/todo/1.0.0/lists?skip={skip}').get_json()
    assert len(lists) == 1


def test_get_lists_search(client):
    searchString = 'mama'
    lists = client.get(f'/todo/1.0.0/lists?searchString={searchString}').get_json()
    assert len(lists) == 1


def test_get_list(client):
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
    assert not task0['completed']
    assert task1['name'] == 'get sugar'
    assert task1['completed']


def test_post_task(client):
    list_id = 'e8f83d1b5d3e437d8674a93cd9087a2b'
    task_name = 'get salad'
    response = client.post(
        f'/todo/1.0.0/list/{list_id}/tasks',
        data=dumps(
            {
                'name': task_name
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
    assert not new_task['completed']
