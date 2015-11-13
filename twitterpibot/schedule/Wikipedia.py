import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
import wikipedia
from wikipedia.exceptions import DisambiguationError
from twitterpibot.twitter.TwitterHelper import send


class Wikipedia(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*")

    def onRun(self):

        # https://wikipedia.readthedocs.org/en/latest/quickstart.html

        is_disambiguation_page = True
        rand = wikipedia.random(pages=1)
        page = None
        while is_disambiguation_page:
            try:
                page = wikipedia.page(title=rand)
                is_disambiguation_page = False
            except DisambiguationError as e:
                rand = random.choice(e.options)
                is_disambiguation_page = True

        if page:
            text = cap(page.summary, 100) + page.url
            tweet = OutgoingTweet(text=text)
            send(tweet)


def cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'
