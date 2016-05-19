import abc

import colorama

import twitterpibot.hardware.myhardware

from twitterpibot.logic import conversation_helper
from twitterpibot.logic.admin_commands import ImportTokensResponse, ExportTokensResponse, DropCreateTablesResponse
from twitterpibot.logic.anagram_solver import AnagramBotResponse
from twitterpibot.logic.april_fools_day import AprilFoolsDayScheduledTask
from twitterpibot.logic.conversation import ConversationScheduledTask
from twitterpibot.logic.cypher_game import DecypherResponse, DecypherScheduledTask
from twitterpibot.logic.ed_balls_day import TweetEdBallsDayScheduledTask, StreamEdBallsDayScheduledTask, \
    TweetBeforeEdBallsDayScheduledTask
from twitterpibot.responses.weather_response import WeatherResponse
from twitterpibot.schedule.JudgementDayScheduledTask import JudgementDayScheduledTask
from twitterpibot.logic.morse_code import MorseCodeResponse
from twitterpibot.logic.statstics import Statistics
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.PhotoResponse import PhotoResponse
from twitterpibot.responses.ReplyResponse import ReplyResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse

from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.x_or_y_response import X_Or_Y_Response
from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
from twitterpibot.schedule.common.usersscheduledtasks import FollowScheduledTask, ScoreUsersScheduledTask
from twitterpibot.schedule.common.IdentityMonitorScheduledTask import IdentityMonitorScheduledTask
from twitterpibot.schedule.common.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.common.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.common.SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
from twitterpibot.schedule.common.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.schedule.common.ratelimitsscheduledtask import RateLimitsScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import twitterhelper
from twitterpibot.users import users

__author__ = 'andrewtatham'


class Identity(object):
    def __init__(self, screen_name, id_str):
        self.admin_screen_name = "andrewtatham"
        self.colour = colorama.Fore.WHITE
        self.screen_name = screen_name
        self.id_str = id_str
        self.tokens = None
        self.streamer = None
        self.profile_image_url = None
        self.twitter = twitterhelper.TwitterHelper(self)

        self.users = users.Users(self)
        self.statistics = Statistics()
        self.conversations = conversation_helper.ConversationHelper(self)
        self.converse_with = None

    @abc.abstractmethod
    def get_tasks(self):
        return [
            StreamTweetsTask(self)
        ]

    @abc.abstractmethod
    def get_scheduled_jobs(self):
        return [
            TweetEdBallsDayScheduledTask(self),
            SuggestedUsersScheduledTask(self),
            ScoreUsersScheduledTask(self),
            RateLimitsScheduledTask(self)

        ]

    @abc.abstractmethod
    def get_responses(self):
        return [
        ]


class BotIdentity(Identity):
    def __init__(self, screen_name, id_str, admin_identity):
        super(BotIdentity, self).__init__(screen_name, id_str)
        self.admin_identity = admin_identity

    def get_scheduled_jobs(self):
        jobs = super(BotIdentity, self).get_scheduled_jobs()
        jobs.extend([
            IdentityMonitorScheduledTask(self),
            UserListsScheduledTask(self, self.admin_identity),
            SubscribedListsScheduledTask(self, self.admin_identity),
            FollowScheduledTask(self),

        ])
        return jobs

    def get_responses(self):
        responses = super(BotIdentity, self).get_responses()
        responses.extend([
            # RestartResponse(self),
            ImportTokensResponse(self),
            ExportTokensResponse(self),
            DropCreateTablesResponse(self),
        ])
        return responses


class PiIdentity(BotIdentity):
    def __init__(self, screen_name, id_str, admin_identity):
        super(PiIdentity, self).__init__(screen_name, id_str, admin_identity)
        self.converse_with = None

    def get_scheduled_jobs(self):
        jobs = super(PiIdentity, self).get_scheduled_jobs()
        jobs.extend([
            WikipediaScheduledTask(self),
            TalkLikeAPirateDayScheduledTask(self),
            WeatherScheduledTask(self),
            JokesScheduledTask(self),
            SongScheduledTask(self),
            ConversationScheduledTask(self, self.converse_with),
            HappyBirthdayScheduledTask(self),
            # LocationScheduledTask(self),
            # RaiseExceptionScheduledTask(self),
            TweetBeforeEdBallsDayScheduledTask(self),
            StreamEdBallsDayScheduledTask(self),
            AprilFoolsDayScheduledTask(self),
            JudgementDayScheduledTask(self),
            DecypherScheduledTask(self),
        ])

        if twitterpibot.hardware.myhardware.is_linux and (
                    twitterpibot.hardware.myhardware.is_webcam_attached or twitterpibot.hardware.myhardware.is_picam_attached):
            jobs.append(PhotoScheduledTask(self))
        if twitterpibot.hardware.myhardware.is_piglow_attached \
                or twitterpibot.hardware.myhardware.is_unicornhat_attached \
                or twitterpibot.hardware.myhardware.is_blinksticknano_attached:
            jobs.append(LightsScheduledTask(self))
        return jobs

    def get_responses(self):
        responses = []
        responses.extend([
            TalkLikeAPirateDayResponse(self),
            AnagramBotResponse(self),
            MorseCodeResponse(self),
            DecypherResponse(self),
            # LocationResponse(self),
            WeatherResponse(self),
            X_Or_Y_Response(self),
            Magic8BallResponse(self),
        ])
        if twitterpibot.hardware.myhardware.is_picam_attached or twitterpibot.hardware.myhardware.is_webcam_attached:
            responses.append(PhotoResponse(self))
        responses.extend([
            ReplyResponse(self),
            FavoriteResponse(self),
            RetweetResponse(self),
        ])
        responses.extend(super(PiIdentity, self).get_responses())
        return responses
