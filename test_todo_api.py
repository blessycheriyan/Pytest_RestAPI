import uuid

import requests

Endpoints = 'https://todo.pixegami.io/'


def test_can_call_endpoints():
    response = requests.get(Endpoints)
    assert response.status_code == 200


def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    data = create_task_response.json()
    print(data)

    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_response = get_task_response.json()
    print(get_task_response)
    assert get_task_response['content'] == payload['content']
    assert get_task_response['user_id'] == payload['user_id']


def test_can_update_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # update the task
    new_payload = {
        "user_id": payload['user_id'],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    # get and validate the changes

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_response = get_task_response.json()
    assert get_task_response['content'] == new_payload['content']
    assert get_task_response['is_done'] == new_payload['is_done']
    pass


def test_can_list_tasks():
    # Create N tasks
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List tasks , and check that there are N times
    user_id = payload['user_id']
    list_task_response = list_task(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    print(data)
    tasks = data['tasks']
    assert len(tasks) == n


def test_can_delete_task():
    # Create a Task

    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # Delete the task

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # Get the task and Check that it's n't found

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(Endpoints + '/create-task/', json=payload)


def update_task(payload):
    return requests.put(Endpoints + '/update-task/', json=payload)


def get_task(task_id):
    return requests.get(Endpoints + f'/get-task/{task_id}')


def list_task(user_id):
    return requests.get(Endpoints + f'/list-tasks/{user_id}')


def delete_task(task_id):
    return requests.delete(Endpoints + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "task_id": "test_task_id",
        "is_done": False
    }
