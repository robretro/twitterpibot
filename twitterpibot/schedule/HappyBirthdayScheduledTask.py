from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import twitterpibot.processing.Birthdays as Birthdays


class HappyBirthdayScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="8-20/2")

    def onRun(self):
        birthday_users = Birthdays.get_birthday_users()
        if birthday_users:
            for birthdayUser in birthday_users:
                Birthdays.sing_birthday_song(birthdayUser)
