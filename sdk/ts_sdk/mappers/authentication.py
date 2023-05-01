from ts_sdk.models.api.model import BodyLoginAccessTokenApiV1LoginAccessTokenPost
from ts_sdk.models.provider import ConfigModel


class AuthenticationMapper:
    @staticmethod
    def map_config_auth(
        payload: ConfigModel,
    ) -> BodyLoginAccessTokenApiV1LoginAccessTokenPost:

        request_payload = BodyLoginAccessTokenApiV1LoginAccessTokenPost(
            username=payload.username,
            password=payload.password,
        )
        return request_payload
