import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot import schedule
from twitterpibot.logic import astronomy
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.logic.timelapses import Timelapse

messages = [
    "Worst timelapse ever",
    "Isn't greyscale ideal for sky timelapses?",
    "I should put some tranquil piano music over this",
    "Why do all timelapses have dubstep music on them?",
    "Here's another"
]


class RegularTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour='3')

    def on_run(self):
        n = 20

        sun = astronomy.get_today_times()

        dawn = sun['dawn']
        dusk = sun['dusk']
        delta = (dusk - dawn) / n

        for i in range(n):
            start = dawn + delta * i
            end = dawn + delta * (i + 1)

            timelapse = Timelapse(
                identity=self.identity,
                name='timelapse%s' % i,
                start_time=start,
                end_time=end,
                interval_seconds=120,
                tweet_text=random.choice(messages))

            tasks = timelapse.get_scheduled_tasks()
            for task in tasks:
                schedule.add(task)
