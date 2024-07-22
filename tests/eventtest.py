from flask import *
from pathlib import Path

resources = Path(__file__).parent / 'resources'


def test_get_all_events(main_client):
    response = main_client.get('/event')
    assert response.status_code == 200


def test_get_event(main_client):
    response = main_client.get('/event?name=test&price=0&location=test')
    assert response.status_code == 200


def test_put_event(main_client):
    response = main_client.put('/event?id=-1')
    assert response.status_code == 404


def test_delete_event1(main_client):
    response = main_client.delete('/event?id=-1')
    assert response.status_code == 404


def test_delete_event2(main_client):
    response0 = main_client.post(
        '/event?city=brasov&date=2024-10-10&location=test&description=dasda&title=test&price=10.5')
    id = response0.json['id']
    response1 = main_client.delete(f'/event?id={id}')
    response2 = main_client.delete(f'/event?id={id}')

    assert response1.status_code == 201
    assert response2.status_code == 404


def test_post_event(main_client):
    response = main_client.post(
        '/event?city=brasov&date=2020-10-10&title=test title&description=test description&price=9999&location=test location')
    id = response.json['id']
    assert response.get_json() == {
        "id": id,
        "city": "brasov",
        "date": "2020-10-10",
        "title": "test title",
        "description": "test description",
        "price": "9999.0",
        "location": "test location",
        "active": "True"
    }
    assert response.status_code == 201


def test_post_invalid_event(main_client):
    response = main_client.post(
        '/event?city=brasov&date=2020-10-10&title=test title&description=test description&price=9999')
    assert response.status_code == 404
    assert response.get_json() == 'Missing value for location'


def test_put_event(main_client):
    response1 = main_client.post(
        '/event?city=brasov&date=2020-10-10&title=test title&description=test description&price=9999&location=test location')
    id = response1.json['id']
    response2 = main_client.put(
        f'/event?id={id}&city=ploiesti&date=2000-9-10&title=test title2&description=test description2&price=666666&location=test location2')
    assert response2.status_code == 201
    assert response2.json['id'] == id
    assert response2.json['city'] == 'ploiesti'
    assert response2.json['date'] == '2000-09-10'
    assert response2.json['title'] == 'test title2'
    assert response2.json['description'] == 'test description2'
    assert float(response2.json['price']) == 666666
    assert response2.json['location'] == 'test location2'
