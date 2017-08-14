import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Manage a github account')
    parser.add_argument('user',
                        metavar='USER',
                        type=str,
                        help='github username')
    parser.add_argument('-t',
                        '--token',
                        dest='token',
                        help='personal access or OAuth token, or path to token (file://...)')
    parser.add_argument('-O',
                        '--organization',
                        # action='store_true',
                        dest='organization',
                        help='whether or not this is an organization user')
    return parser.parse_known_args()
