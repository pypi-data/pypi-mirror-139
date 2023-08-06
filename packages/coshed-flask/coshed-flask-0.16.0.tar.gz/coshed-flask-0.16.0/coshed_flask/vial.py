#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import pprint
import datetime

import flask

import coshed_flask
from coshed_flask.tools import generate_expires_header

API_VERSION = os.environ.get("API_VERSION")
API_VERSION_FALLBACK = "0.0.42"

if API_VERSION is None:
    try:
        API_VERSION = coshed_flask.__version__
    except Exception:
        API_VERSION = API_VERSION_FALLBACK

NAVIGATION_ITEMS = [
    ("/", "Home"),
    ("/doc", "Documentation"),
]


class AppResponse(dict):
    """
    Container class for flask app responses.
    """

    def __init__(self, *args, **kwargs):
        self.drop_dev = kwargs.get("drop_dev")

        try:
            del kwargs["drop_dev"]
        except Exception:
            pass

        dict.__init__(self, *args, **kwargs)

        if "_dev" not in self:
            self["_dev"] = dict()

        try:
            self["version"] = API_VERSION
        except NameError:
            self["version"] = API_VERSION_FALLBACK

        self["python_version"] = sys.version_info.major
        self["_now"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        if "navigation" not in list(self.keys()):
            nav_items = list(self.navigation)
            if nav_items:
                self["navigation"] = nav_items

    @property
    def navigation(self):
        for data in NAVIGATION_ITEMS:
            try:
                (i_url, i_label, whitelist_key) = data
            except ValueError:
                whitelist_key = None
                (i_url, i_label) = data

            if whitelist_key and whitelist_key not in self.get(
                "whitelist", []
            ):
                continue
            yield i_url, i_label

    def flask_obj(
        self,
        status_code=200,
        drop_dev=None,
        with_version=True,
        expires=None,
        headers=None,
        not_to_be_exposed=None,
    ):
        """
        Generate a :py:class:`flask.Response` object for current application
        response object.

        Args:
            status_code (int): HTTP status code, default 200
            drop_dev (bool): Drop development information
            with_version (bool): include version information
            expires: expiration specification
            headers (dict): headers
            not_to_be_exposed (iterable, optional): key/value pairs not to be exposed

        Returns:
            flask.Response: HTTP response object
        """
        del_keys = []

        if drop_dev is None:
            drop_dev = self.drop_dev

        if drop_dev:
            del_keys.append("_dev")

        if with_version is False:
            del_keys.append("version")

        if not_to_be_exposed:
            for ntbe in not_to_be_exposed:
                del_keys.append(ntbe)

        for del_key in del_keys:
            try:
                del self[del_key]
            except KeyError:
                pass

        if headers is None:
            headers = dict()

        headers["Content-Type"] = "application/json"

        if expires is not None:
            headers.update(generate_expires_header(expires))

        try:
            body = json.dumps(self, indent=2, sort_keys=True)
        except TypeError:
            body = pprint.pformat(self)
            headers["Content-Type"] = "text/plain"
            status_code = 500

        return flask.Response(
            status=status_code, headers=headers, response=body
        )
