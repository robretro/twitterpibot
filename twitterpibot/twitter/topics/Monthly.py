from twitterpibot.twitter.topics.Topic import Topic

_months = [
    "Jan(uary)",
    "Feb(ruary)",
    "Mar(ch)",
    "Apr(il)",
    "May",
    "Jun(e)",
    "Jul(y)",
    "Aug(ust)",
    "Nov(ember)",
    "Dec(ember)"
]


class FirstOfMonth(Topic):
    def __init__(self):
        super(FirstOfMonth, self).__init__(
           ["Happy New Month", "(first|1(st)) of (%s)".format("|".join(_months))]
        )


def get():
    return [
        FirstOfMonth()
    ]