import json
from toolbox.connect_api import get_github_api_host, retrieve_data
import csv

def retrieve_users(args, get_2fa_disabled=False):
    '''get all members from an Organization'''
    single_request = False
    query_args = None

    if get_2fa_disabled:
        query_args = {'filter':'2fa_disabled'}
        # get those who don't enable 2FA in our Org
        print('retrieve users who DID NOT enable 2fa from an organization')

    else:
        print('retrieve users from an organization')

    template = 'https://{0}/orgs/{1}/members'.format(
        get_github_api_host(args),
        args.user)

    return retrieve_data(args, template, single_request=single_request, query_args=query_args)


def retrieve_user_details(args,github_acct_name,keys):
    '''get a specific user detail info, given his github acct name'''
    print('\n','getting user detailed info for Github user: {}'.format(github_acct_name))

    single_request = True
    template = 'https://{0}/users/{1}'.format(
        get_github_api_host(args),
        # args.user,
        github_acct_name)

    userinfo = retrieve_data(args, template, single_request=single_request)[0]
    returning_results = ({key:userinfo[key] for key in keys})
    print("returning result: ", returning_results)
    return returning_results


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
