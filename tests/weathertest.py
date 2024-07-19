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
    response = client.get('/weather?city=zzdasd231aszzzzzzzz')
    assert len(response.json) == 0
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
        'description': 'dasda',
        'date': '2024-10-10',
        'humidity': '10.0',
        'id': id,
        'temperature': '10.0'}
    assert response.status_code == 201


def test_put_weather2(client):
    response0 = client.post('/weather?city=brasov&date=2024-10-10&temperature=10&description=dasda&humidity=10')
    id = response0.json['id']
    response = client.put(f'/weather?id={id}&city=brasov&date=2024-10-10&temperature=10&description=dasda&humidity=10')

    assert response.status_code == 201


def test_delete_weather(client):
    response0 = client.post('/weather?city=brasov&date=2024-10-10&temperature=10&description=dasda&humidity=10')
    id = response0.json['id']
    response1 = client.delete(f'/weather?id={id}')
    response2 = client.delete(f'/weather?id={id}')

    assert response1.status_code == 201
    assert response2.status_code == 404
