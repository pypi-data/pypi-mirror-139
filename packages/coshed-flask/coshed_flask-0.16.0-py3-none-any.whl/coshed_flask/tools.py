#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tempfile
import uuid
import logging
from logging.handlers import RotatingFileHandler
import datetime
import time
from wsgiref.handlers import format_date_time

from flask import request
from flask_cors import CORS
from flask_compress import Compress
import six


ROTATING_LOG_BACKUP_COUNT = 1
ROTATING_LOG_MAX_BYTES = 20000

#: custom log formatter
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)-16s %(levelname)-8s %(funcName)-15s "
    "(#%(lineno)04d): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

WANT_DEV = ("i-like-my-sugar-with", "coffee-and-cream")


def drop_dev(want_dev=None):
    if want_dev is None:
        want_dev = WANT_DEV

    try:
        (arg_name, expectation) = want_dev
        return not request.args.get(arg_name) == expectation
    except Exception:
        pass

    return True


def rotating_app_log(flask_app_instance, app_name=None, **kwargs):
    """
    Set up a rotating log file for flask instance.

    Args:
        flask_app_instance (flask.Flask): flask instance
        app_name (str): app name

    Keyword Args:
        maxBytes (int): maximum bytes threshold for rollover
        backupCount (int): maximum number of rotations to keep

    Returns:
        str: log path
    """
    if app_name is None:
        app_name = uuid.uuid4().hex

    log_trunk = "{:s}-webapp.log".format(app_name)
    log_filename = os.path.join(tempfile.gettempdir(), log_trunk)
    handler = RotatingFileHandler(
        log_filename,
        maxBytes=kwargs.get("maxBytes", ROTATING_LOG_MAX_BYTES),
        backupCount=kwargs.get("backupCount", ROTATING_LOG_BACKUP_COUNT),
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    flask_app_instance.logger.addHandler(handler)
    flask_app_instance.logger.setLevel(logging.INFO)
    logging.getLogger("iotta.boarding_queue").addHandler(handler)

    return log_filename


def wolfication(flask_app_instance, **kwargs):
    """
    Set up a flask instance with CORS and compression enabled and set some
    default configuration values.

    Args:
        flask_app_instance (flask.Flask): flask instance

    Keyword Args:
        jinja_filters (dict, optional): jinja filters to be installed
        app_name (str, optional): application name
        maxBytes (int, optional): maximum bytes threshold for log rollover
        backupCount (int, optional): maximum number of log rotations to keep
        config (dict, optional): configuration overrides

    Returns:
        flask.Flask: flask instance
    """
    flask_app_instance.jinja_env.trim_blocks = True
    flask_app_instance.jinja_env.lstrip_blocks = True
    flask_app_instance.jinja_env.strip_trailing_newlines = True
    flask_app_instance.config["SEND_FILE_MAX_AGE_DEFAULT"] = 24 * 3600 * 365
    flask_app_instance.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
    flask_app_instance.config["CORS_SUPPORTS_CREDENTIALS"] = True

    if kwargs.get("config"):
        flask_app_instance.config.update(kwargs.get("config"))

    if kwargs.get("jinja_filters"):
        jinja_filters = kwargs.get("jinja_filters")

        for (filter_key, filter_func) in six.iteritems(jinja_filters):
            flask_app_instance.jinja_env.filters[filter_key] = filter_func

    CORS(flask_app_instance)
    Compress(flask_app_instance)

    if kwargs.get("app_name"):
        log_kwargs = dict(
            maxBytes=kwargs.get("maxBytes", ROTATING_LOG_MAX_BYTES),
            backupCount=kwargs.get("backupCount", ROTATING_LOG_BACKUP_COUNT),
        )
        rotating_app_log(
            flask_app_instance, kwargs.get("app_name"), **log_kwargs
        )

    return flask_app_instance


def request_wants_mimetype(mtb, other="text/html"):
    best = request.accept_mimetypes.best_match([mtb, other])
    return (
        best == mtb
        and request.accept_mimetypes[best] > request.accept_mimetypes[other]
    )


def request_wants_json():
    return request_wants_mimetype("application/json")


def generate_expires_header(expires=False):
    """
    Generate HTTP expiration header.

    Args:
        expires: expiration in seconds or False for *imediately / no caching*

    Returns:
        dict: key/value pairs defining HTTP expiration information
    """
    headers = {}

    if expires is False:
        headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, "
            "post-check=0, pre-check=0, max-age=0"
        )
        headers["Expires"] = "-1"
    else:
        now = datetime.datetime.now()
        expires_time = now + datetime.timedelta(seconds=expires)
        headers["Cache-Control"] = "public"
        headers["Expires"] = format_date_time(
            time.mktime(expires_time.timetuple())
        )

    return headers
