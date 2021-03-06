from twitterpibot.movies import moviehelper
from twitterpibot.responses.MarkovResponse import MarkovResponse
from twitterpibot.responses.Response import mentioned_reply_condition


class MovieMarkovResponse(MarkovResponse):
    def __init__(self, identity, movie_name):
        super(MovieMarkovResponse, self).__init__(identity, moviehelper.get_lines(movie_name))

    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item=inbox_item)

    def respond(self, inbox_item):
        super(MovieMarkovResponse, self).respond(inbox_item=inbox_item)
