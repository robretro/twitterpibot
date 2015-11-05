from twitterpibot.twitter.topics.Topic import NewsTopic


class PoliticsUK(NewsTopic):
    def __init__(self):
        super(PoliticsUK, self).__init__([
            "(David)? Cameron",
            "(George)? Osborne",
            "Jeremy Hunt",
            "Conservative",
            "Tor(y|ies)",

            "(Jeremy)? Corbyn",
            "Labour",

            "(Nigel)? Farage",
            "UKIP",

            "PMQ",
            "Prime Minister",
            "Westminster",
            "Downing"
        ], ["politic", "PM"])


class PoliticsUS(NewsTopic):
    def __init__(self):
        super(PoliticsUS, self).__init__([

            "President",
            "POTUS",
            "Barack", "Obama",

            "Hilary", "Clinton",
            "Bernie", "Sanders",
            "Democrat",

            "Donald", "Trump",
            "Jeb", "Bush",
            "Marco", "Rubio",
            "Republican",
            "GOP",
            "Tea Party",

            "Senate",
            "House of Representatives"

        ], ["politic"])


def get():
    return [PoliticsUK(), PoliticsUS()]
