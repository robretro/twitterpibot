from twitterpibot.twitter.topics.Topic import DontCareTopic


class OneDirection(DontCareTopic):
    def __init__(self):
        super(OneDirection, self).__init__([
            "1D",
            "One Direction",
            "Niall", "Horan",
            "Payne",
            "Harry Styles",
            "Louis Tomlinson",
            "Zayn", "Malik"

        ], [
            "Liam",
            "Harry", "Styles",
            "Louis"
        ])


class FiveSecondsOfSummer(DontCareTopic):
    def __init__(self):
        super(FiveSecondsOfSummer, self).__init__([
            "5SOS",
            "five seconds of summer",
            "Luke Hemmings",
            "Michael Clifford",
            "Calum Hood",
            "Ashton Irwin",
            "The New Broken Scene"
        ], [
            "Luke", "Hemmings",
            "Michael", "Clifford",
            "Calum", "Hood",
            "Ashton", "Irwin"
        ])


class Kardashians(DontCareTopic):
    def __init__(self):
        super(Kardashians, self).__init__([
            "Kardashian",
            "Kim",
            "Khloe",
            "Kourtney",
            "Kylie",
            "Kendall",
            "Caitlyn",
            "Jenner"

        ])


class CelebrityOther(DontCareTopic):
    def __init__(self):
        super(CelebrityOther, self).__init__([
            "Justin Bieber", "BELIEBERS", "jb(i|e)ebs",
            "Miley Cyrus",
            "Taylor Swift",
            "Britney Spears",
            "Ariana Grande"
        ])


def get():
    return [
        OneDirection(),
        FiveSecondsOfSummer(),
        Kardashians(),

        CelebrityOther()
    ]
