# tests/test_basic.py
import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200

def test_shorten_url(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not_a_valid_url"})
    assert response.status_code == 400

def test_redirect_and_stats(client):
   
    post_response = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = post_response.get_json()['short_code']

    
    redirect_response = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_response.status_code == 302

   
    stats_response = client.get(f'/api/stats/{short_code}')
    stats_data = stats_response.get_json()
    assert stats_data['url'] == "https://example.com"
    assert stats_data['clicks'] == 1

def test_404_on_invalid_code(client):
    response = client.get('/api/stats/invalid123')
    assert response.status_code == 404
