from flask import *
from pathlib import Path

resources = Path(__file__).parent / 'resources'


def test_get_all_events(client):
    response = client.get('/event')
    assert response.status_code == 200


def test_get_event(client):
    response = client.get('/event?name=test&price=0&location=test')
    assert response.status_code == 200


def test_put_event(client):
    response = client.put('/event?id=-1')
    assert response.status_code == 404


def test_delete_event1(client):
    response = client.delete('/event?id=-1')
    assert response.status_code == 404


def test_delete_event2(client):
    response0 = client.post('/event?city=brasov&date=2024-10-10&location=test&description=dasda&title=test&price=10.5')
    id = response0.json['id']
    response1 = client.delete(f'/event?id={id}')
    response2 = client.delete(f'/event?id={id}')

    assert response1.status_code == 201
    assert response2.status_code == 404


