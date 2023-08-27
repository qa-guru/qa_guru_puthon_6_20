import json

import allure
from allure_commons.types import AttachmentType
from jsonschema.validators import validate
from requests import sessions
from curlify import to_curl


def reqres_api(method, url, **kwargs):
    base_url = "https://reqres.in"
    new_url = base_url + url
    method = method.upper()
    with allure.step(f"{method} {url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT, extension='txt')
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json", attachment_type=AttachmentType.JSON, extension='json')
    return response


def test_users_per_page():
    per_page = 2

    response = reqres_api(
        "get",
        url="/api/users",
        params={"per_page": per_page}
    )

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_users_schema():
    with open('get_users_schema.json') as file:
        schema = json.loads(file.read())

    response = reqres_api("get", "/api/users")

    validate(instance=response.json(), schema=schema)
