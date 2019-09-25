from .common import get_app_and_client


@get_app_and_client
def test_docs(app=None, client=None):
    response = client.get("/docs")
    assert response.status_code == 200
