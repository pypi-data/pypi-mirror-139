from enum import Enum
from typing import Optional, Any, AnyStr

import requests
from requests import Session, Request, Response
from requests.auth import AuthBase

from .service_registry import ServiceRegistry
from ..auth import OAuthTokenAuth, DeviceCodeAuth
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import ServiceTypeNotFoundError, ServiceException


class BaseServiceClient:
    """
    The base class for all DNAStack Clients

    :param parent: The parent :class:`PublisherClient` instance of the client. If a parent is not defined, the
    service client will create its own :class:`AuthClient` for authorization
    :param url: The url of the service to be configured
    :param **kwargs: Additional keyword arguments to be passed to the :class:`AuthClient` if necessary
    """

    def __init__(
        self,
        auth: AuthBase = None,
        url: AnyStr = None,
        registry_url: AnyStr = DEFAULT_SERVICE_REGISTRY,
        **kwargs,
    ):
        self.url = url

        self.__client = requests.Session()

        self.__registry = ServiceRegistry(registry_url)

        if auth:
            self.auth = auth
        else:
            self.auth = None

    @property
    def auth(self) -> AuthBase:
        return self.__auth

    @auth.setter
    def auth(self, auth: AuthBase) -> None:
        self.__auth = auth
        self.__client.auth = auth

    @property
    def client(self) -> Session:
        return self.__client

    def authorize(self):
        if isinstance(self.__auth, OAuthTokenAuth):
            self.__auth.authorize(Request(url=self.url))
        else:
            raise AttributeError(
                "The service auth must be a OAuthTokenAuth in order to authorize"
            )

    def _raise_error(self, res: Response, primary_reason: str):
        error_msg = primary_reason

        if res.status_code == 401:
            error_msg += ": The request was not authenticated"
        elif res.status_code == 403:
            error_msg += ": Access Denied"
        else:
            error_json = res.json()
            if "errors" in error_json:
                error_msg += f' ({error_json["errors"][0]["title"]})'

        raise ServiceException(msg=error_msg, url=self.url)
