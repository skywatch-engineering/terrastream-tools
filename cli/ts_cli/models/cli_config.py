from pydantic import BaseModel
from pydantic import Field


class CliConfigModel(BaseModel):
    api_base_url: str = Field(description="Api base url")
    api_username: str = Field(description="Api user name. Example: user@domain.com")
    api_password: str = Field(description="TS user api password")

    @staticmethod
    def example() -> dict:
        return {
            "api_base_url": "https://api.provider-stage.terrastream.ca",
            "api_password": "<password here>",
            "api_username": "user@domain.com",
        }
