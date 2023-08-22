import json

import requests
from jsonschema.validators import validate


def test_users_per_page():
    per_page = 'abc'

    response = requests.get(
        url="https://reqres.in/api/users",
        params={"per_page": per_page}
    )

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_users_schema():
    with open('get_users_schema.json') as file:
        schema = json.loads(file.read())

    response = requests.get("https://reqres.in/api/users")

    validate(instance=response.json(), schema=schema)
