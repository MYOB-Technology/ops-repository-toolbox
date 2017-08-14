import base64
import json
import calendar
import codecs
import errno
import getpass
import json
import logging
import os
import re
import select
import subprocess
import sys
import time
import platform

from urllib.parse import urlparse
from urllib.parse import quote as urlquote
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.request import Request


def get_github_api_host(args):
    # Uncomment if your Org uses self-hosted Github api

    # if args.github_host:
    #     host = args.github_host + '/api/v3'
    # else:
    host = 'api.github.com'

    return host


def get_auth(args, encode=False):

    auth = None

    if args.token:
        # for 'using Personal-Token to auth against Github API V3'
        # scenario: the Org enforced 2FA where Username+Password
        # doesn't work programmatically
        auth = ' token ' + args.token
    if not auth:
        return None

    return auth


def _request_http_error(exc, auth, errors):
    # HTTPError behaves like a Response so we can
    # check the status code and headers to see exactly
    # what failed.

    should_continue = False
    headers = exc.headers
    limit_remaining = int(headers.get('x-ratelimit-remaining', 0))

    if exc.code == 403 and limit_remaining < 1:
        # The X-RateLimit-Reset header includes a
        # timestamp telling us when the limit will reset
        # so we can calculate how long to wait rather
        # than inefficiently polling:
        gm_now = calendar.timegm(time.gmtime())
        reset = int(headers.get('x-ratelimit-reset', 0)) or gm_now
        # We'll never sleep for less than 10 seconds:
        delta = max(10, reset - gm_now)

        limit = headers.get('x-ratelimit-limit')
        print('Exceeded rate limit of {} requests; waiting {} seconds to reset'.format(limit, delta))
            # ,file=sys.stderr)

        if auth is None:
            print('Hint: Authenticate to raise your GitHub rate limit') #, file=sys.stderr)

        time.sleep(delta)
        should_continue = True
    return errors, should_continue


def _request_url_error(template, retry_timeout):
    # Incase of a connection timing out, we can retry a few time
    # But we won't crash and not back-up the rest now
    print('{} timed out'.format(template))
    retry_timeout -= 1

    if retry_timeout >= 0:
        return True

    print('{} timed out to much, skipping!')
    return False


def get_query_args(query_args=None):
    if not query_args:
        query_args = {}
    return query_args


def _construct_request(per_page, page, query_args, template, auth):
    querystring = urlencode(dict(list({
        'per_page': per_page,
        'page': page
    }.items()) + list(query_args.items())))

    request = Request(template + '?' + querystring)
    if auth is not None:
        request.add_header('Authorization', auth)
    print("headers= ", request.headers)
    return request


def _get_response(request, auth, template):
    retry_timeout = 3
    errors = []
    # We'll make requests in a loop so we can
    # delay and retry in the case of rate-limiting
    while True:
        should_continue = False
        try:
            r = urlopen(request)
        except HTTPError as exc:
            errors, should_continue = _request_http_error(exc, auth, errors)
            r = exc
        except URLError:
            should_continue = _request_url_error(template, retry_timeout)
            if not should_continue:
                raise

        if should_continue:
            continue

        break
    return r, errors


def retrieve_data(args, template, query_args=None, single_request=False):
    auth = get_auth(args)
    query_args = get_query_args(query_args)
    per_page = 100
    page = 0
    data = []

    while True:
        page = page + 1
        request = _construct_request(per_page, page, query_args, template, auth)
        r, errors = _get_response(request, auth, template)
        status_code = int(r.getcode())

        if status_code != 200:
            # template = 'API request returned HTTP {0}: {1}'
            # errors.append(template.format(status_code, r.reason))
            # print(errors)
            # print(errors)
            print(status_code,r.reason)

        response = json.loads(r.read().decode('utf-8'))

        if len(errors) == 0:
            if type(response) == list:
                data.extend(response)
                if len(response) < per_page:
                    break
            elif type(response) == dict and single_request:
                data.append(response)

        if len(errors) > 0:
            print(errors)

        if single_request:
            break

    return data
