import base64
from enum import Enum
import json
import logging
import os
import pathlib
import signal
from calendar import timegm
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode

import click
import jwt
import requests
import uvicorn
from fastapi import FastAPI, Query, Request

from cricket_cookie import env

from cricket_cookie.utils.network import find_free_network_port

logger = logging.getLogger(__name__)


class Keys(Enum):
    USERNAME = "LIGHTNING_USERNAME"
    USER_ID = "LIGHTNING_USER_ID"
    API_KEY = "LIGHTNING_API_KEY"
    JWT_TOKEN = "LIGHTNING_JWT_TOKEN"

    @property
    def suffix(self):
        return self.value.lstrip("LIGHTNING_").lower()


@dataclass
class JWTToken:
    @classmethod
    def is_expired(cls, token) -> bool:
        try:
            claim = jwt.decode(token, options={"verify_signature": False})
            now = timegm(datetime.now(tz=timezone.utc).utctimetuple())
            # if token is about to expire, refresh
            expired = claim["exp"] < now - env.LEEWAY
            if expired:
                logger.debug("token is expired")
            return expired
        except BaseException:
            return True


@dataclass
class Auth:
    username: Optional[str] = None
    user_id: Optional[str] = None
    api_key: Optional[str] = None
    jwt_token: Optional[str] = None

    secrets_file = pathlib.Path(env.LIGHTNING_CREDENTIAL_PATH)

    def __post_init__(self):
        for key in Keys:
            setattr(self, key.suffix, os.environ.get(key.value, None))

        self._with_env_var = bool(
            self.jwt_token
            or self.user_id and self.api_key)  # used by authenticate method
        if self.api_key and not self.user_id:
            raise ValueError(
                f"{Keys.USER_ID.value} is missing from env variables. "
                "To use env vars for authentication "
                f"both {Keys.USER_ID.value} and {Keys.API_KEY.value} should be set."
            )

    def load(self) -> bool:
        """Load credentials from disk and update properties with credentials.

        Returns
        ----------
        True if credentials are available.
        """
        if not self.secrets_file.exists():
            logger.debug("Credentials file not found.")
            return False
        with self.secrets_file.open() as creds:
            credentials = json.load(creds)
            for key in Keys:
                setattr(self, key.suffix, credentials.get(key.suffix, None))
            return True

    def save(self,
             token: str,
             username: str = "",
             user_id: str = "",
             api_key="") -> None:
        """save credentials to disk."""
        self.secrets_file.parent.mkdir(exist_ok=True, parents=True)
        with self.secrets_file.open("w") as f:
            json.dump(
                {
                    f"{Keys.JWT_TOKEN.suffix}": token,
                    f"{Keys.USERNAME.suffix}": username,
                    f"{Keys.USER_ID.suffix}": user_id,
                    f"{Keys.API_KEY.suffix}": api_key
                },
                f,
            )

        self.username = username
        self.jwt_token = token
        self.user_id = user_id
        self.api_key = api_key
        logger.debug("credentials saved successfully")

    @classmethod
    def clear(cls) -> None:
        """remove credentials from disk and env variables."""
        if cls.secrets_file.exists():
            cls.secrets_file.unlink()
        for key in Keys:
            os.environ.pop(key.value, None)
        logger.debug("credentials removed successfully")

    @property
    def auth_header(self) -> Optional[str]:
        """authentication header used by lightning-cloud client."""
        if self.jwt_token:
            return f"Bearer {self.jwt_token}"
        if self.api_key:
            token = f"{self.user_id}:{self.api_key}"
            return f"Basic {base64.b64encode(token.encode('ascii')).decode('ascii')}"  # noqa E501
        raise AttributeError(
            "Authentication Failed, no authentication header available. "
            "This is most likely a bug in the LightningCloud Framework")

    def _run_server(self) -> None:
        """start a server to complete authentication."""
        AuthServer().login_with_browser(self)

    def authenticate(self) -> Optional[str]:
        """Performs end to end authentication flow.

        Returns
        ----------
        authorization header to use when authentication completes.
        """
        if self._with_env_var:
            logger.debug("successfully loaded credentials from env")
            return self.auth_header

        if not self.load():
            logger.debug(
                "failed to load credentials, opening browser to get new.")
            self._run_server()

        elif JWTToken.is_expired(self.jwt_token):
            logger.debug("token has expired, opening browser to get new.")
            self._run_server()
        return self.auth_header


class AuthServer:
    def get_auth_url(self, port: int) -> str:
        redirect_uri = f"http://localhost:{port}/login-complete"
        params = urlencode(dict(redirectTo=redirect_uri))
        return f"{env.LIGHTNING_WEB_APP_URL}/sign-in?{params}"

    def login_with_browser(self, auth: Auth) -> None:
        app = FastAPI()
        port = find_free_network_port()
        url = self.get_auth_url(port)
        try:
            # check if server is reachable or catch any network errors
            requests.head(url, verify=not env.IS_DEV_ENV)
        except requests.ConnectionError as e:
            raise requests.ConnectionError(
                f"No internet connection available. Please connect to a stable internet connection \n{e}"  # noqa E501
            )
        except requests.RequestException as e:
            raise requests.RequestException(
                f"An error occurred with the request. Please report this issue to Lightning Team \n{e}"  # noqa E501
            )

        logger.info(f"login started for lightning.ai, opening {url}")
        click.launch(url)

        @app.get("/login-complete")
        async def save_token(request: Request,
                             token="",
                             key="",
                             user_id: str = Query("", alias="userID")):
            if token:
                auth.save(token,
                          username=user_id,
                          user_id=user_id,
                          api_key=key)
                logger.info("Authentication Successful")
                response = "login complete you can close the tab now"
            else:
                logger.warning(
                    "Authentication Failed. This is most likely because you're using an older version of the cli. \n"  # noqa E501
                    "Please try to update the cli or open an issue with this information \n"  # noqa E501
                    f"expected token in {request.query_params.items()}")
                response = "login failed, look at terminal/cmd for more info"
            # redirect them to lightning.ai with auth credentials
            # or getting started guide.
            os.kill(os.getpid(), signal.SIGTERM)
            return response

        server = uvicorn.Server(
            config=uvicorn.Config(app, port=port, log_level="error"))
        server.run()
