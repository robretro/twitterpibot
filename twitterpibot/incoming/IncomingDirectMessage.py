import logging
import colorama

from twitterpibot.incoming.InboxItem import InboxItem

logger = logging.getLogger(__name__)


class IncomingDirectMessage(InboxItem):
    # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages
    # https://dev.twitter.com/rest/reference/get/direct_messages
    def __init__(self, data, identity):
        super(IncomingDirectMessage, self).__init__(data, identity)
        self.is_direct_message = "direct_message" in data

        dm = data.get("direct_message")
        if dm:
            self.sender = identity.users.get_user(user_data=dm.get("sender"))
            self.recipient = identity.users.get_user(user_data=dm["recipient"])
            self.from_me = self.sender.isMe
            self.to_me = self.recipient.isMe
            self.targets = [self.sender.screen_name]
            self.text = dm.get("text")
            self.text_stripped = self.text
            self.words = self.text.split()

    def display(self):
        colour = self.identity.colour + colorama.Style.BRIGHT
        text = u" * DM from @" + self.sender.screen_name + u" to @" + self.recipient.screen_name + u": " + self.text
        logger.info(colour + text)
