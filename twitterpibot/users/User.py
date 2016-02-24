import datetime




def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


class User(object):
    def __init__(self, data, my_screen_name):

        self.id_str = data.get("id_str")
        self.name = data.get("name")
        self.screen_name = data.get("screen_name")
        self.description = data.get("description")
        self.url = data.get("url")
        self.profile_image_url = data.get("profile_image_url")
        self.profile_banner_url = data.get("profile_banner_url")
        if self.profile_banner_url:
            self.profile_banner_url += "/300x100"

        self.isMe = bool(self.screen_name == my_screen_name)

        self.following = bool(data.get("following"))
        self.verified = bool(data.get("verified"))
        self.location = data.get("location")
        self.protected = bool(data.get("protected"))

        self.friends_count = parse_int(data.get("friends_count"))
        self.followers_count = parse_int(data.get("followers_count"))
        self.statuses_count = parse_int(data.get("statuses_count"))

        self.updated = None

        self.is_arsehole = False
        self.is_do_not_retweet = False
        self.is_retweet_more = False
        self.is_bot = False
        self.is_friend = False
        self.is_reply_less = False

    def is_stale(self):
        if self.updated:
            delta = datetime.datetime.utcnow() - self.updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            return mins > 45
        else:
            return True
