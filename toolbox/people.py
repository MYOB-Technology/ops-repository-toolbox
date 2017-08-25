# -*- coding: utf-8 -*-
import json
from toolbox.connect_api import get_github_api_host, retrieve_data
import re
from settings import RE_NAME


def retrieve_members(args, get_2fa_disabled=False):
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
    return [retrieve_user_details(args,github_acct_name,keys) for github_acct_name in namelist]


def get_2fa_disabled_members(args, input_users, whitelist):
    ''' Members who don't do 2FA, excluding easily identifiable machine users
        return: github login name
    '''
    parsed_results = [ item['login'] for item in input_users if item['login'] not in whitelist]
    print (len(parsed_results))
    return parsed_results


def get_nameless_users(args, keys, all_org_users, whitelist):
    # a list of org member login, excluding logins from an exemption list.
    parsed_results = [ item['login'] for item in all_org_users if item['login'] not in whitelist ]
    nameless_members = []

    for individual_login in parsed_results:
        details = retrieve_user_details(args=args, github_acct_name=individual_login, keys=keys)
        if not details['name']:
            print('NAMELESS!!! ')
            details['reject_reason'] = 'name missing'
            nameless_members.append(details)
        # https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name

        elif not re.match(RE_NAME, details['name']):
            print("INVALID NAME: {}".format(details['name']))
            details['reject_reason'] = 'invalid name'
            nameless_members.append(details)

    return nameless_members


def merge_2fa_nameless_users(args, list_2fa, list_nameless, keys):

    nameless_users_logins = []

    for user_detail in list_nameless:
        # user_detail['reject_reason'] = 'invalid name'
        nameless_users_logins.append(user_detail['login'])

    for two_fa_disabled_user in list_2fa:
        if two_fa_disabled_user not in nameless_users_logins:
            print('expanding original list with 2fa-disabled-only user: {}'.format(two_fa_disabled_user))
            details = retrieve_user_details(args, two_fa_disabled_user, keys)
            details['reject_reason']='2fa'
            list_nameless.append(details)
        else:
            print('merging an user who did not do 2fa && have no valid name.. do nothing')
            for item in list_nameless:
                if item['login'] == two_fa_disabled_user:
                    item['reject_reason'] += ',2fa'
    return list_nameless


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
