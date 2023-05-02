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

from requests import Response

logger = logging.getLogger()


### Undocumented errors from TS API


class UndocumentedError(Exception):
    pass


class InvalidCredentials(UndocumentedError):
    """
    The correct information was provided for
    """

    pass


class NotAuthenticatedError(UndocumentedError):
    """
    TS api request is not sending authorization headers
    """

    pass


class NotFoundError(UndocumentedError):
    """
    TS api request could not find the appropriate resource
    """

    pass


class CannotTransitionError(UndocumentedError):
    """
    TS api request could not send the request
    """

    pass


### Generic errors for unknown responses


class ApiResponseErrorBase(Exception):
    def __init__(self, *, response: Response):
        super().__init__()
        logger.error(
            f"ApiResponseErrorBase: status: {response.status_code}, text: {response.text}"
        )


class ApiResponseError(ApiResponseErrorBase):
    """An exception raised when an unknown response occurs"""

    def __init__(self, *, response: Response):
        super().__init__(response=response)

        if (
            response.status_code == 403
            and "Could not validate credentials" in response.text
        ):
            raise InvalidCredentials("Could not validate credentials")

        if response.status_code == 401 and "Not authenticated" in response.text:
            raise NotAuthenticatedError(response.text)

        if response.status_code == 404:
            raise NotFoundError(response.text)

        if response.status_code == 400 and "cannot transition to" in response.text:
            raise CannotTransitionError(response.text)

        if response.status_code == 422:
            raise ApiValidationError(response=response)


### TS api specific errors based on status code error and documentation provided by TS


class ApiNotFoundError(ApiResponseErrorBase):
    """
    TS api endpoint could not be found
    """

    pass


class ApiInvalidCredentialsError(ApiResponseErrorBase):
    """
    TS api could not validate information provided for authentication like user and/or password
    """

    pass


class ApiValidationError(ApiResponseErrorBase):
    """
    TS api could not validate the payload
    """

    pass


class SourceFileHttpError(Exception):
    def __init__(self, *, message: str):
        super().__init__()
        logger.error(f"Could not retrieve file information: {message}")
        self.message = message


### Step function errors


class SfnRecoverableError(Exception):
    """
    Indicates whether a call can be retried or not.
    It is meant to be used when handling calls from Stepfunctions using lambdas
    """

    pass


class SfnUnrecoverableError(Exception):
    """
    Indicates whether a call can be retried or not.
    It is meant to be used when handling calls from Stepfunctions using lambdas
    """

    pass
