
from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
from OutgoingDirectMessage import OutgoingDirectMessage

from Statistics import GetStatistics, Reset

class MidnightScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = 0)
 
    def onRun(args):

        stats = GetStatistics()
        tweet = OutgoingDirectMessage(
            text=stats,
            screen_name = "andrewtatham", 
            user_id = "19201332")
        Send(tweet)
        Reset()