from unittest import TestCase

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse

__author__ = 'Andrew'


class TestMagic8BallResponse(TestCase):
    def test_condition(self):
        response = Magic8BallResponse(None)

        self.assertFalse(response.condition(IncomingTweet({
            "text": "blah?"
        }, None)))
