# Copyright 2023 Skywatch Space Applciations Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

logger = logging.getLogger()

from ts_sdk.api.errors import InvalidCredentials
from functools import wraps
from ts_sdk.controllers.client_controller import ClientController


def call_with_auth(func):
    """
    Decorator that provides a retry mechanism for TS api calls for when the TS access token is expired or inexistent
    Decorated functions should receive as parameter an instance of AuthenticatedClient with the name auth_client.

    If a InvalidCredentials exception is triggered by the decorated function the decorator logic will retry again
    but with a renewed token (result of calling TS /access_token endpoint).

    If an InvalidCredentials is raised again it won't retry and the exception will throw to the caller,
    as it's probably something else.

    Example:

    @call_with_auth
    def decorated_function(auth_client: AuthenticatedClient):
        # call TS with the given auth_client.
        # If TS returns a InvalidCredentials it will retry once with a renewed token
        return requests_tasking_get(client=auth_client, request_id="tasking-request-id")

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        authenticated_client = ClientController().auth(force_renew=False)

        try:
            kwargs["auth_client"] = authenticated_client
            return func(*args, **kwargs)

        except InvalidCredentials:
            authenticated_client = ClientController().auth(force_renew=True)
            kwargs["auth_client"] = authenticated_client

            return func(*args, **kwargs)

    return wrapper
