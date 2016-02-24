import random

import twitterpibot.identities

__author__ = 'andrewtatham'


def get_user_dto(user):
    return {
        "user_id": user.id,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "url": user.url,
        "profile_image_url": user.profile_image_url,
        "profile_banner_url": user.profile_banner_url

    }


def get_action_dto(label, url):
    return {
        "label": label,
        "url": url
    }


def get_identities_dto(identity):
    dto = {
        "screen_name": identity.screen_name,
        "id_str": identity.id_str,
        "url": "identity/" + identity.screen_name
    }
    return dto


def get_identity_dto(identity):
    dto = get_identities_dto(identity)
    if identity.following:
        dto["following"] = [{"follower_id": f} for f in identity.following]
    if identity.lists:
        dto["lists"] = [
            {
                "list_name": l,
                "members": [
                    {
                        "list_member_id": list_member_id
                    } for list_member_id in identity.lists._sets[l]]
            } for l in identity.lists._sets]
    if identity.users:
        dto["users"] = [get_user_dto(user)
                        for user_id, user in identity.users._users.items()]
    return dto


class Controller(object):
    def get_identities(self):
        return [get_identities_dto(i) for i in twitterpibot.identities.all_identities]

    def get_identity(self, screen_name=None):
        return [get_identity_dto(i) for i in twitterpibot.identities.all_identities
                if screen_name == i.screen_name][0]

    def get_actions(self):
        return [get_action_dto(a[0], a[1]) for a in [
            ("home", "/"),
            ("demo", "/demo"),
            ("init", "/init"),
            ("actions", "/actions"),
            ("identities", "/identities"),
            ("following", "/following"),
            ("followinggraph", "/followinggraph"),
            ("shutdown", "/shutdown")
        ]]

    def get_following(self):
        dto = []
        for identity in twitterpibot.identities.all_identities:
            if identity.following:
                for following in identity.following:
                    dto.append((identity.id_str, following))

        return dto

    def get_following_graph(self):
        nodes = {}
        edges = {}

        # add identity nodes
        for identity in twitterpibot.identities.all_identities:
            nodes[identity.id_str] = \
                {
                    "screen_name": identity.screen_name,
                    "profile_image_url": identity.profile_image_url
                }
            # init identity edges
            edges[identity.id_str] = {}

            # add edges between identities
            # for identity2 in twitterpibot.identities.all_identities:
            #     if identity2.id_str in identity.following:
            #         edge_data = {}
            #         edges[identity.id_str][identity2.id_str] = edge_data


        # get a list of users to add
        users_list = []
        for identity in twitterpibot.identities.all_identities:
            identity_users_list = []
            for k, v in identity.users._users.items():
                identity_users_list.append(v)
            random.shuffle(identity_users_list)
            users_list.extend(identity_users_list[:10])

        # add user nodes
        for user in users_list:
            nodes[user.id_str] = \
                {
                    "screen_name": user.screen_name,
                    "profile_image_url": user.profile_image_url
                }

            # add following edges
            for identity in twitterpibot.identities.all_identities:
                if user.id_str in identity.following:
                    edge_data = {}
                    edges[identity.id_str][user.id_str] = edge_data

        dto = {
            "nodes": nodes,
            "edges": edges
        }
        return dto
