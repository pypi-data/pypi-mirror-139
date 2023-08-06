from typing import Optional

from pydantic import BaseModel, BaseSettings, Field


class SlackConfig(BaseModel):
    api_token: str
    default_channel: str


class SlackEnvConfig(BaseSettings):
    api_token: Optional[str] = Field(env="SLACK_BOT_TOKEN")
    default_channel: Optional[str] = Field(env="SLACK_BOT_DEFAULT_CHANNEL")
