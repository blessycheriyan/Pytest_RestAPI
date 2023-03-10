import requests

Endpoints = 'https://todo.pixegami.io/'


def test_can_call_endpoints():
    response = requests.get(Endpoints)
    assert response.status_code == 200


def test_can_create_task():
    payload = {
        "content": "my test content",
        "user_id": "test_user",
        "task_id": "test_task_id",
        "is_done": False
    }
    create_task_response = requests.put(Endpoints + '/create-task', json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data['task']['task_id']
    get_task_response = requests.get(Endpoints + f"/get-task/{task_id}")
    assert get_task_response.status_code == 200
    get_task_response = get_task_response.json()
    print(get_task_response)
    assert get_task_response['content'] == payload['content']
    assert get_task_response['user_id'] == payload['user_id']
