import sys
import logging

import colorama

import twitterpibot.MyLogging as MyLogging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.identities
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI

MyLogging.init()
logger = logging.getLogger(__name__)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

Tasks.set_tasks(twitterpibot.identities.get_all_tasks())
MySchedule.set_scheduled_jobs(twitterpibot.identities.get_all_scheduled_jobs())

Tasks.start()
MySchedule.start()

MyUI.start()

MySchedule.stop()
Tasks.stop()
hardware.stop()
logger.info("Done")
sys.exit(0)
