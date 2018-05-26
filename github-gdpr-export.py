#!/usr/bin/env python3
# Copyright (c) 2018 Sampo Sorsa <sorsasampo@protonmail.com>
import argparse

import requests


def list_user_repos(args):
    r = requests.get('https://api.github.com/users/%s/repos' % args.username)
    r.raise_for_status()
    for repo in r.json():
        print(repo[u'full_name'])


parser = argparse.ArgumentParser(description='Export GitHub projects using migration API')
subparsers = parser.add_subparsers(help='command')

parser_list_user_repos = subparsers.add_parser('list-user-repos', description='List user repositories')
parser_list_user_repos.add_argument('username', help='GitHub username')
parser_list_user_repos.set_defaults(func=list_user_repos)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
