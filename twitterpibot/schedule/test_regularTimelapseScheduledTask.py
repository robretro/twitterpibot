from unittest import TestCase
from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask




class TestRegularTimelapseScheduledTask(TestCase):
    def test_onRun(self):
        task = RegularTimelapseScheduledTask()
        task.on_run()
