import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.logic import birthday
from twitterpibot.songs import songhelper


class HappyBirthdayScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="8-20/2", minute=random.randint(0, 59))

    def on_run(self):
        birthday_users = birthday.get_birthday_users()
        if birthday_users:
            for birthday_user in birthday_users:
                birthday_song_key = random.choice(songhelper.birthday_song_keys())
                birthday_song = songhelper.get_song(song_key=birthday_song_key)
                self.identity.twitter.sing_song(
                    song=birthday_song,
                    target=birthday_user,
                    text="Happy Birthday @" + birthday_user + " !!!",
                    hashtag="#HappyBirthday")
