import logging
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

from hartware_lib.exceptions.slack import ApiError

logger = logging.getLogger(__name__)


class SlackAdapter:
    def __init__(self, config):
        self.config = config
        self.client = WebClient(token=self.config.api_token)

    def send(self, msg: str, channel: Optional[str] = None) -> SlackResponse:
        if not channel and self.config.default_channel:
            channel = self.config.default_channel

        try:
            return self.client.chat_postMessage(
                channel=channel or self.config.default_channel, text=msg
            )
        except SlackApiError:
            api_error = ApiError()
            logger.warning(api_error.message)
            raise api_error
