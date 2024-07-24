import pytest
from gateway.CityBreak import gateway_app


@pytest.fixture()
def main_client():
    """Configures the app for testing

        Sets app config variable ``TESTING`` to ``True``

        :return: App for testing
        """

    gateway_app.config['TESTING'] = True
    main_client = gateway_app.test_client()

    yield main_client


@pytest.fixture()
def weather_client():
    gateway_app.config['TESTING'] = True
    weather_client = gateway_app.test_client()

    yield weather_client

@pytest.fixture()
def event_client():
    gateway_app.config['TESTING'] = True
    event_client = gateway_app.test_client()

    yield event_client

@pytest.fixture()
def runner(application):
    return application.test_cli_runner()

