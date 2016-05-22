import datetime
import logging
import random

from twitterpibot.users import lists
from twitterpibot.users.user import User

logger = logging.getLogger(__name__)


class Users(object):
    def __init__(self, identity):
        self._identity = identity
        self._users = {}

        self._following = set()
        self._followers = set()
        self._lists = lists.Lists(self._identity)

        self._lists.update_lists()
        self.get_followers()
        self.get_following()

    def get_user(self, user_id=None, user_data=None):

        if user_id and user_id in self._users:
            user = self._users[user_id]
        else:
            # make new user
            if user_id and not user_data:
                logger.debug("looking up user %s" % user_id)
                user_data = self._identity.twitter.lookup_user(user_id=user_id)[0]
            elif not user_id and user_data:
                user_id = user_data.get("id_str")
            user = User(user_data, self._identity)
            self._users[user_id] = user

        if user.is_stale():
            self.update_user(user=user)

        return self._users[user_id]

    def get_users(self, user_ids):
        users = []
        cached = list(filter(lambda u: u in self._users, user_ids))
        to_lookup = list(filter(lambda u: not u in self._users, user_ids))

        for user_id in cached:
            users.append(self.get_user(user_id=user_id))

        n = 100
        for chunk in [to_lookup[i:i + n] for i in range(0, len(to_lookup), n)]:
            ids_csv = ",".join(chunk)
            user_datas = self._identity.twitter.lookup_user(user_id=ids_csv)
            for user_data in user_datas:
                users.append(self.get_user(user_data=user_data))

        return users

    def update_user(self, user):

        self._lists.update_user_list_memberships(user)

        user.follower = user.id_str in self._followers
        user.following = user.id_str in self._following

        user.updated = datetime.datetime.utcnow()

    def friends(self, friends):
        logger.info("[%s] Friends %s" % (self._identity.screen_name, len(friends)))
        self._following = set([str(f) for f in friends])

    def get_following(self):
        if not self._following:
            self._following = self._identity.twitter.get_following()
            logger.info("[%s] following %s" % (self._identity.screen_name, len(self._following)))
        return self._following

    def get_followers(self):
        if not self._followers:
            self._followers = self._identity.twitter.get_followers()
            logger.info("[%s] followers %s" % (self._identity.screen_name, len(self._followers)))
        return self._followers

    def score_users(self, n=None):
        user_ids = list(self._users)
        random.shuffle(user_ids)
        if n:
            user_ids = user_ids[:n]
        for user_id in user_ids:
            if not self._users[user_id]._user_score:
                user_score = self._users[user_id].get_user_score()
                # todo should not be needed
                self._users[user_id]._user_score = user_score

        users_with_scores = list(filter(lambda u: u._user_score, list(self._users.values())))
        return len(users_with_scores)

    def get_leaderboard(self, n=3):

        users_with_scores = list(filter(lambda u: u._user_score, list(self._users.values())))

        users_with_scores.sort(key=lambda u: u._user_score.total())
        worst = users_with_scores[:n]
        best = users_with_scores[-n:]
        logger.info("USER LEADERBOARD")
        logger.info("BEST")
        for best_user in best:
            logger.info(best_user.long_description())
        logger.info("WORST")
        for worst_user in worst:
            logger.info(worst_user.long_description())

    def follow(self, user_id):
        self._identity.twitter.follow(user_id=user_id)
        self._following.add(user_id)

    def unfollow(self, user_id):
        self._identity.twitter.unfollow(user_id=user_id)
        if user_id in self._following:
            self._following.remove(user_id)

    def block(self, user_id):
        self._identity.twitter.block(user_id=user_id)
        if user_id in self._following:
            self._following.remove(user_id)

    def report(self, user_id):
        self._identity.twitter.report(user_id=user_id)
        if user_id in self._following:
            self._following.remove(user_id)


if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPi2Identity(None)

    all_user_ids = set()
    all_user_ids.update(identity.users.get_following())
    all_user_ids.update(identity.users.get_followers())
    all_user_ids = list(all_user_ids)
    print(len(all_user_ids))
    random.shuffle(all_user_ids)
    all_user_ids = all_user_ids[:20]

    identity.users.get_users(all_user_ids)

    try:
        no_of_scores = identity.users.score_users()
        print(no_of_scores)
    except Exception as ex:
        print(ex)
    finally:
        identity.users.get_leaderboard()
