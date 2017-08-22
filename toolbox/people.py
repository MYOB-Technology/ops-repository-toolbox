# -*- coding: utf-8 -*-
import json
from toolbox.connect_api import get_github_api_host, retrieve_data
from settings import KNOWN_MACHINE_MEMBERS, KNOWN_MACHINE_OUTSIDE_CONTRIBUTORS
import re

def retrieve_users(args, get_2fa_disabled=False):
    '''get all members from an Organization'''
    single_request = False
    query_args = None

    if get_2fa_disabled:
        query_args = {'filter':'2fa_disabled'}
        # get those who don't enable 2FA in our Org
        print('retrieve users who DID NOT enable 2fa from an organization')

    else:
        print('retrieve all members from an organization')

    template = 'https://{0}/orgs/{1}/members'.format(
        get_github_api_host(args),
        args.user)

    return retrieve_data(args, template, single_request=single_request, query_args=query_args)


def retrieve_outsidecontributors(args, get_2fa_disabled=False):
    single_request = False
    query_args = None

    if get_2fa_disabled:
        query_args = {'filter':'2fa_disabled'}
        # get those who don't enable 2FA in our Org
        print('retrieve outside_contributors who DID NOT enable 2fa from an organization')

    else:
        print('retrieve users from an organization')

    template = 'https://{0}/orgs/{1}/outside_collaborators'.format(
        get_github_api_host(args),
        args.user)

    return retrieve_data(args, template, single_request=single_request, query_args=query_args)


def retrieve_user_details(args, github_acct_name, keys):
    '''get a specific user detail info, given his github acct name'''
    single_request = True
    template = 'https://{0}/users/{1}'.format(
        get_github_api_host(args),
        github_acct_name)

    userinfo = retrieve_data(args, template, single_request=single_request)[0]
    returning_results = ({key:userinfo[key] for key in keys})
    print(returning_results)
    return returning_results


def expand_user_details(args, namelist, keys):
    if namelist['two_fa_status']:
        return [retrieve_user_details(args,github_acct_name,keys) for github_acct_name in namelist['parsed_results']]
    else:
        ## TODO : add a key value to the dict
        return [retrieve_user_details(args,github_acct_name,keys) for github_acct_name in namelist['parsed_results']]

def get_2fa_disabled_members(args):
    ''' Members who don't do 2FA, excluding easily identifiable machine users
        return: github login name
    '''
    result = retrieve_users(args, get_2fa_disabled=True)
    parsed_results = [ item['login'] for item in result if item['login'] not in KNOWN_MACHINE_MEMBERS ]
    print (len(parsed_results))
    return {'parsed_results': parsed_results, 'two_fa_status': False}


def get_2fa_disabled_outside_contributors(args):
    ''' OutsideContributors who don't do 2FA, excluding easily identifiable machine users
        return: github login name
    '''
    result = retrieve_outsidecontributors(args, get_2fa_disabled=True)
    parsed_results = [ item['login'] for item in result if item['login'] not in KNOWN_MACHINE_OUTSIDE_CONTRIBUTORS ]
    print (len(parsed_results))
    return {'parsed_results': parsed_results, 'two_fa_status': False}


def get_nameless_members(args,keys):
    result = retrieve_users(args)
    # a list of org member login, excluding logins from an exemption list.
    parsed_results = [ item['login'] for item in result if item['login'] not in KNOWN_MACHINE_MEMBERS ]
    nameless_members = []

    for individual_login in parsed_results:
        details = retrieve_user_details(args=args, github_acct_name=individual_login, keys=keys)
        if not details['name']:
            print('NAMELESS!!! ')
            nameless_members.append(details)
    return nameless_members


def get_nameless_outside_contributors(args, keys):
    result = retrieve_outsidecontributors(args)
    # a list of org member login, excluding logins from an exemption list.
    parsed_results = [ item['login'] for item in result if item['login'] not in KNOWN_MACHINE_OUTSIDE_CONTRIBUTORS ]
    nameless_outside_contributors = []

    for individual_login in parsed_results:
        details = retrieve_user_details(args=args, github_acct_name=individual_login, keys=keys)
        if not details['name']:
            print('NAMELESS GUY FOUND...')
            nameless_outside_contributors.append(details)
    return nameless_outside_contributors


def remove_member(args, github_acct_name):
    single_request = True
    print('verifying membership for {}...'.format(github_acct_name))
    template = 'https://{0}/orgs/{1}/outside_collaborators'.format(
        get_github_api_host(args),
        args.user)

    result = retrieve_data(args, template, single_request=single_request)
    namelist = [item['login'] for item in result]
    if github_acct_name in namelist:
        print ('login name verified...')
        template = 'https://{0}/orgs/{1}/outside_collaborators/{2}'.format(
            get_github_api_host(args),
            args.user,
            github_acct_name)
        # TODO: send http-delete
    else:
        print ('login name NOT verified...')
        return None
