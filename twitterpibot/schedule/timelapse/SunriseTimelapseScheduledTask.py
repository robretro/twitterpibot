import datetime

from apscheduler.triggers.cron import CronTrigger

from twitterpibot import schedule
import twitterpibot.logic.astronomy as astronomy
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.logic.timelapses import Timelapse


class SunriseTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=3)

    def on_run(self):
        sun = astronomy.get_today_times()

        timelapse = Timelapse(
            identity=self.identity,
            name='sunrise',
            start_time=sun['dawn'] + datetime.timedelta(minutes=-20),
            end_time=sun['sunrise'] + datetime.timedelta(minutes=+20),
            interval_seconds=90,
            tweet_text="Morning!")

        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            schedule.add(task)
