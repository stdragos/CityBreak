from flask import *
from pathlib import Path

resources = Path(__file__).parent / 'resources'


def test_get_all_weather(client):
    response = client.get('/weather')
    assert response.status_code == 200


def test_get_weather_city1(client):
    response = client.get('/weather?city=ploiesti')
    assert response.status_code == 200


def test_get_weather_city2(client):
    response = client.get('/weather?city=zzzzzzz')
    assert response.status_code == 200


def test_put_weather(client):
    response = client.put('/weather?id=-1')
    assert response.status_code == 404


def test_post_weather(client):
    response = client.post('/weather?id=10&city=brasov&date=2024-10-10&temperature=10&description=dasda&humidity=10')
    id = response.json['id']
    assert response.get_json() == {
        'active': 'True',
        'city': 'brasov',
        'date': '2024-10-10',
        'description': 'dasda',
        'humidity': '10.0',
        'id': id,
        'temperature': '10.0'}
    assert response.status_code == 201


def test_put_weather2(client):
    response = client.put('/weather?id=10&city=brasov&date=2024-10-10&temperature=10&description=dasda&humidity=10')

    assert response.status_code == 201
