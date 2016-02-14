import random

from twitterpibot.logic import webscraper
from twitterpibot.responses.Response import Response

quotes = webscraper.get_malcolm_tucker_quotes()


class MalcolmTuckerResponse(Response):
    def condition(self, inbox_item):
        return super(MalcolmTuckerResponse, self).reply_condition(inbox_item=inbox_item) \
               and inbox_item.sender.screen_name == self.identity.admin_screen_name

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item=inbox_item, text=random.choice(quotes))