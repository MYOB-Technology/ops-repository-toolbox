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


def retrieve_user_details(args,github_acct_name):
    '''get a specific user detail info, given his github acct name'''
    print('\n','getting user detailed info for Github user: {}'.format(github_acct_name))

    single_request = True
    template = 'https://{0}/orgs/{1}/users/{2}'.format(
        get_github_api_host(args),
        args.user,
        github_acct_name)

    userinfo = retrieve_data(args, template, single_request=single_request)[0]
    print (userinfo)

    info_keys = [
        # 'two_factor_authentication',
        'email',
        'name']
    returning_results = ({key:userinfo[key] for key in info_keys})
    print("returning_results: ", returning_results)
    return returning_results
