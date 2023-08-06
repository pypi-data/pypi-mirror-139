#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import hashlib

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


def username_identifier(username):
    """
    Generate an identifier for given username

    Args:
        username (str): username

    Returns:
        str: user identifier
    """
    hasher = hashlib.sha1()
    hasher.update(username.encode("utf-8"))

    return f"u_{hasher.hexdigest()}".upper()


def check_password_hash_env(username, password):
    """
    Check if given credentials match user identifier/password hash pair
    in environment variables

    Args:
        username (str): username
        password (str): password

    Returns:
        bool: ``True`` if credentials match
    """
    user_id = username_identifier(username)
    challenge = os.environ.get(user_id)

    if not challenge:
        return False

    return check_password_hash(challenge, password)


def hash_tuple(username, password, method=None):
    """
    Generate a tuple containing user identifier and password hash for
    given credentials

    Args:
        username (str): username
        password (str): password
        method (str, optional): Password hashing method. \
            Defaults to ``pbkdf2:sha256:100000``.

    Returns:
        tuple: user identifier and password hash

    >>> user = "test 123"
    >>> password = "$wordfishöäü"
    >>> k, v = hash_tuple(user, password)
    >>> os.environ[k] = v
    >>> check_password_hash_env(user, password)
    True
    >>> check_password_hash_env(user, "wrong")
    False
    >>> check_password_hash_env("no-user", "wrong")
    False
    """
    if method is None:
        method = "pbkdf2:sha256:100000"

    password_hash = generate_password_hash(password, method)
    user_id = username_identifier(username)

    return (user_id, password_hash)


if __name__ == "__main__":
    import doctest

    (FAILED, SUCCEEDED) = doctest.testmod()
    print("[doctest] SUCCEEDED/FAILED: {:d}/{:d}".format(SUCCEEDED, FAILED))
