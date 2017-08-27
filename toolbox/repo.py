from toolbox.connect_api import get_github_api_host, retrieve_data
import json
from hurry.filesize import size, alternative


def get_readible_file_size(filesize):
    return size(filesize, system=alternative)


def get_repo_size(args):

    print('\n','getting info for SUM size of ',
        'Github repo for org : {}'.format(args.user))
    single_request = False
    template = 'https://{0}/orgs/{1}/repos'.format(
        get_github_api_host(args),
        args.user)

    repoinfo = retrieve_data(args, template, single_request=single_request)

    with open('repo_size.data', 'w') as outfile:
        json.dump(repoinfo, outfile)

    size_sum = 0
    for repo in repoinfo:
        size_sum += repo['size']
    return get_readible_file_size(size_sum)
