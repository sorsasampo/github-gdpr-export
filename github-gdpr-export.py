#!/usr/bin/env python3
# Copyright (c) 2018 Sampo Sorsa <sorsasampo@protonmail.com>
import argparse

import requests


def download(args):
    headers = {
        'Accept': 'application/vnd.github.wyandotte-preview+json',
        'Authorization': 'token %s' % args.token,
    }
    r = requests.get('https://api.github.com/user/migrations/%d/archive' % args.id, headers=headers, stream=True)
    r.raise_for_status()
    print('Downloading "%s" into "%s"' % (r.url, args.filename))
    with open(args.filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)


def list_migrations(args):
    headers = {
        'Accept': 'application/vnd.github.wyandotte-preview+json',
        'Authorization': 'token %s' % args.token,
    }
    r = requests.get('https://api.github.com/user/migrations', headers=headers)
    r.raise_for_status()
    print('{:8} {:9} {:5}'.format('id', 'state', 'lock'))
    for migration in r.json():
        print('{0[id]:<8} {0[state]:9} {0[lock_repositories]:<5}'.format(migration))


def list_user_repos(args):
    r = requests.get('https://api.github.com/users/%s/repos' % args.username)
    r.raise_for_status()
    for repo in r.json():
        print(repo[u'full_name'])


parser = argparse.ArgumentParser(description='Export GitHub projects using migration API')
parser.add_argument('--token', help='GitHub personal access token\nhttps://github.com/settings/tokens')
subparsers = parser.add_subparsers(help='command')

parser_download = subparsers.add_parser('download', description='Fetch URL for downloading the migration archive')
parser_download.add_argument('id', type=int, help='Migration id')
parser_download.add_argument('filename', help='Filename to save as')
parser_download.set_defaults(func=download)

parser_list = subparsers.add_parser('list', description='List user migrations')
parser_list.set_defaults(func=list_migrations)

parser_list_user_repos = subparsers.add_parser('list-user-repos', description='List user repositories')
parser_list_user_repos.add_argument('username', help='GitHub username')
parser_list_user_repos.set_defaults(func=list_user_repos)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
