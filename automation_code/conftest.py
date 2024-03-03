import pytest
import requests
from requests_oauthlib import OAuth1


@pytest.fixture(scope="session")
def api_client():
    """Fixture to authenticate and return an API session."""
    session = requests.Session()

    # Assuming your API requires a POST request to authenticate
    auth_url = "https://yourapi.com/auth"
    credentials = {"username": "user", "password": "pass"}
    response = session.post(auth_url, json=credentials)

    if response.status_code == 200:
        token = response.json().get('token')
        session.headers.update({'Authorization': f'Bearer {token}'})
        session.auth = OAuth1(wc_creds['wc_key'], wc_creds['wc_secret'])
        return session
    else:
        pytest.fail("Authentication failed. Can't proceed with tests.")


# session utility