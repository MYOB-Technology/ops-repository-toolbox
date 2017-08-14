#!/usr/bin/env python

import json
from toolbox.connect_api import get_github_api_host, retrieve_data


def retrieve_users(args):
    '''get all members from an Organization'''
    single_request = False

    if args.organization:

        print('retrieve users from an organization')
        template = 'https://{0}/orgs/{1}/members'.format(
        get_github_api_host(args),
        args.user)
    else:
        print('retrieve users from a personal repo')
        template = 'https://{0}/user/repos'.format(
            get_github_api_host(args))

    return retrieve_data(args, template, single_request=single_request)
