from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

import datetime
from twitterpibot.twitter.TwitterHelper import Send


class EdBallsDay(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(month=4, day=28, hour=16, minute=20)

    def onRun(self):
        year = str(datetime.date.today().year)
        text = "@edballs ED BALLS #EdBallsDay #EdBallsDay" + year
        tweet = OutgoingTweet(text=text)
        Send(tweet)