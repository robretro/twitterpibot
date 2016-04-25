from twitterpibot.tasks.Task import Task
import time
import twitterpibot.hardware.myhardware


class FadeTask(Task):
    def __init__(self):
        Task.__init__(self, None)
        self.core = True

    def on_run(self):
        twitterpibot.hardware.myhardware.on_fade_task()
        time.sleep(1)
