import pytest
import requests

from config import API_BASE_URL, API_TIMEOUT


@pytest.fixture
def api():
    # Session giữ kết nối và header chung cho mọi request trong test.
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.mark.api
def test_get_post_by_id(api):
    response = api.get(f"{API_BASE_URL}/posts/1", timeout=API_TIMEOUT)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["userId"] == 1
    assert body["title"].strip() != ""


@pytest.mark.api
def test_get_posts_filtered_by_user(api):
    response = api.get(f"{API_BASE_URL}/posts", params={"userId": 1}, timeout=API_TIMEOUT)

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


@pytest.mark.api
def test_create_post(api):
    new_post = {"title": "Automation test", "body": "Created by pytest", "userId": 1}

    response = api.post(f"{API_BASE_URL}/posts", json=new_post, timeout=API_TIMEOUT)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == new_post["title"]
    assert body["body"] == new_post["body"]
    assert body["userId"] == new_post["userId"]
    assert "id" in body


@pytest.mark.api
@pytest.mark.negative
def test_get_post_not_found(api):
    response = api.get(f"{API_BASE_URL}/posts/99999", timeout=API_TIMEOUT)

    assert response.status_code == 404
