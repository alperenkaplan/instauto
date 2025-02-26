from instauto.api.client import ApiClient
from instauto.api.actions.structs.friendships import GetFollowers, Create, GetFollowing, Destroy
from instauto.helpers.search import get_user_id_from_username
from instauto.helpers.common import is_resp_ok
from instauto.helpers import models

import typing
import logging

logger = logging.getLogger(__name__)


def get_followers(client: ApiClient, user_id: str, username: str, limit: int) -> typing.List[models.User]:
    """Retrieve the first x amount of followers from an account.

    Either `user_id` or `username` need to be provided. If both are provided,
    the user_id takes precedence.

    Args:
        client: your ApiClient
        user_id: the user_id of the account to retrieve followers from
	    username: the username of the account to retrieve followers from
        limit: the maximum amount of followers to retrieve

    Returns:
        A list containing Instagram user objects (examples/objects/user.json).
    """
    if user_id is None and username is not None:
        user_id = get_user_id_from_username(client, username)

    if user_id is None:
        raise ValueError("Both `user_id` and `username` are not provided.")

    obj = GetFollowers(user_id)

    obj, result = client.followers_get(obj)
    followers = []
    while result and len(followers) < limit:
        followers.extend(
            result.json()["users"]
        )
        logger.info("Retrieved {} followers, {} more to go.".format(len(followers), limit - len(followers)))
        obj, result = client.followers_get(obj)
    return [models.User.parse(f) for f in followers[:min(len(followers), limit)]]


def get_following(client: ApiClient, user_id: str, username: str, limit: int) -> typing.List[models.User]:
    """Retrieve the first x amount of users that an account is following.

    Either `user_id` or `username` need to be provided. If both are provided,
    the user_id takes precedence.

    Args:
        client: your ApiClient
        user_id: the user_id of the account to retrieve following from
	    username: the username of the account to retrieve following from
        limit: the maximum amount of users to retrieve

    Returns:
        A list containing Instagram user objects (examples/objects/user.json).
    """
    if user_id is None and username is not None:
        user_id = get_user_id_from_username(client, username)

    if user_id is None:
        raise ValueError("Both `user_id` and `username` are not provided.")

    obj = GetFollowing(user_id)

    obj, result = client.following_get(obj)
    following = []
    while result and len(following) < limit:
        following.extend(
            result.json()["users"]
        )
        logger.info("Retrieved {} of following, {} more to go.".format(len(following), limit - len(following)))
        obj, result = client.following_get(obj)
    return [models.User.parse(f) for f in following[:min(len(following), limit)]]


def follow_user(client: ApiClient, user_id: str = None, username: str = None) -> bool:
    """Send a follow request to a user.

    Either `user_id` or `username` need to be provided. If both are provided,
    the user_id takes precedence.

    Args:
        client: your ApiClient
        user_id: the user_id of the account to follow
        username: the username of the account to follow
    Returns:
        True if success else False
    """
    if user_id is None and username is not None:
        user_id = get_user_id_from_username(client, username)

    if user_id is None:
        raise ValueError("Both `user_id` and `username` are not provided.")

    obj = Create(str(user_id))
    resp = client.user_follow(obj)
    return is_resp_ok(resp)


def unfollow_user(client: ApiClient, user_id: str = None, username: str = None) -> bool:
    """Unfollow a user.

    Either `user_id` or `username` need to be provided. If both are provided,
    the user_id takes precedence.

    Args:
        client: your ApiClient
        user_id: the user_id of the account to unfollow
        username: the username of the account to unfollow
    Returns:
        True if success else False
    """
    if user_id is None and username is not None:
        user_id = get_user_id_from_username(client, username)

    if user_id is None:
        raise ValueError("Both `user_id` and `username` are not provided.")

    obj = Destroy(str(user_id))
    resp = client.unfollow_user(obj)
    return is_resp_ok(resp)

