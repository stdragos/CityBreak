import pytest
from CityBreak import gateway_app

@pytest.fixture()
def client():
    """Configures the app for testing

        Sets app config variable ``TESTING`` to ``True``

        :return: App for testing
        """

    gateway_app.config['TESTING'] = True
    client = gateway_app.test_client()

    yield client


@pytest.fixture()
def runner(application):
    return application.test_cli_runner()
