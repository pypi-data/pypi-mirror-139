from typing import Optional
from cricket_cookie import env
from cricket_cookie.login.auth import Credentials
from cricket_cookie.openapi import V1LoginRequest, ApiClient, Configuration
import json
import os
from pathlib import Path

from cricket_cookie.rest_client import GridRestClient


def lightning_login(
    username: Optional[str] = None,
    user_id: Optional[str] = None,
    api_key: Optional[str] = None,
    *,
    _url=env.
    LIGHTNING_CLOUD_URL  # noqa - For testing purposes only. not user facing.
):
    """
    Log in with your grid.ai credentials for usage of the SDK in the running process.

    All parameters are optional. Calling ``login()`` without parameters will check if
    the ``GRID_USER_ID`` and ``GRID_API_KEY`` env vars have been set (using those if
    available), otherwise it will check for the file ``credentials.json`` in the
    machines ``$HOME/.lightning`` directory (if it exists).

    Parameters
    ----------
    username
        your grid username. This is either be your github username or email address,
        depending on what you use when signing into the grid platform at
    """
    configuration = Configuration()
    configuration.host = _url
    configuration.ssl_ca_cert = env.SSL_CA_CERT
    client = GridRestClient(ApiClient(configuration=configuration))

    if username and api_key:
        token_resp = client.auth_service_login(
            V1LoginRequest(
                username=username,
                api_key=api_key,
            ))
        client.api_client.set_default_header("Authorization",
                                             f"Bearer {token_resp.token}")

        # now that we're authenticated, get the user ID
        user_resp = client.auth_service_get_user()
        creds = Credentials(user_id=user_resp.id, api_key=api_key)
        _create_credentials_file(creds)
    else:
        raise ValueError("Username and api key is required")

    # set the GRID_URL before new api clients are created
    os.environ['GRID_URL'] = _url
    env.reset_global_variables()

    # Set the user credentials in the os env
    os.environ['GRID_USER_ID'] = creds.user_id
    os.environ['GRID_API_KEY'] = creds.api_key
    creds = Credentials.from_locale()
    return True


def _create_credentials_file(creds: 'Credentials'):
    Path(env.LIGHTNING_CREDENTIAL_PATH).parent.mkdir(parents=True,
                                                     exist_ok=True)
    with Path(env.LIGHTNING_CREDENTIAL_PATH).open('w') as file:
        json.dump({
            'UserID': creds.user_id,
            'APIKey': creds.api_key
        },
                  file,
                  ensure_ascii=False,
                  indent=4)
