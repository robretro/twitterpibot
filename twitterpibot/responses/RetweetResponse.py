import logging

from twitterpibot.responses.Response import Response, retweet_condition

logger = logging.getLogger(__name__)


class RetweetResponse(Response):
    def condition(self, inbox_item):
        return retweet_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("retweeting status id %s", inbox_item.id_str)
        self.identity.twitter.retweet(inbox_item.id_str)
