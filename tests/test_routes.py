import pytest

def test_routes(testapp):
    response = testapp.get('/')
    assert response.status_code == 200

    response = testapp.get('/instructions')
    assert response.status_code == 200

    response = testapp.get('/about')
    assert response.status_code == 200

    response = testapp.get('/privacy')
    assert response.status_code == 200

    response = testapp.get('/blog/')
    assert response.status_code == 200

    response = testapp.get('/error-test')
    assert response.status_code == 404
