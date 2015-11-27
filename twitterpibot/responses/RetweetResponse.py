import random
import re
from twitterpibot.incoming.InboxItem import InboxItem

from twitterpibot.responses.Response import Response
from twitterpibot.twitter import TwitterHelper

import logging

logger = logging.getLogger(__name__)


class RetweetResponse(Response):
    def __init__(self):
        self.bannedTopics = [

            # TODO move to topics

            # RT to Win
            "(RT|Retweet|chance|follow).*(to|2).*win",

            # RT/Fav voting
            "(RT|Retweet).*(Fav)",
            "(Fav).*(RT|Retweet)",

            # Football

            # Job Adverts
            "is.*(looking for|hiring)",
            "Jobs available",
            "Apply now"
        ]

        self.rx = re.compile("|".join(self.bannedTopics), re.IGNORECASE)

    def condition(self, inbox_item):
        return inbox_item.is_tweet \
               and not inbox_item.from_me \
               and not inbox_item.to_me \
               and not (inbox_item.retweeted or inbox_item.retweeted_status and inbox_item.retweeted_status.retweeted) \
               and not inbox_item.sender.protected \
               and not inbox_item.sender.is_arsehole \
               and not (inbox_item.sender.is_do_not_retweet
                        or inbox_item.retweeted_status
                        and inbox_item.retweeted_status.sender.is_do_not_retweet) \
               and not bool(self.rx.match(inbox_item.text)) \
               and (not inbox_item.topics or inbox_item.topics.retweet()) \
               and ((inbox_item.sender.is_bot and random.randint(0, 50) == 0) or
                    (inbox_item.sender.is_friend and random.randint(0, 3) == 0) or
                    (inbox_item.sender.is_retweet_more and random.randint(0, 9) == 0) or
                    (inbox_item.sourceIsTrend and random.randint(0, 20) == 0) or
                    (inbox_item.sourceIsSearch and random.randint(0, 20) == 0) or
                    (random.randint(0, 99) == 0))

    def favourite(self, inbox_item):
        return False

    def respond(self, inbox_item):
        logger.info("retweeting status id %s", inbox_item.status_id)
        TwitterHelper.retweet(inbox_item.status_id)
