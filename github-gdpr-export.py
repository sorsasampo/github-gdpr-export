#!/usr/bin/env python3
# Copyright (c) 2018 Sampo Sorsa <sorsasampo@protonmail.com>
import argparse

import requests


def delete(args):
    headers = {
        'Accept': 'application/vnd.github.wyandotte-preview+json',
        'Authorization': 'token %s' % args.token,
    }
    r = requests.delete('https://api.github.com/user/migrations/%d/archive' % args.id, headers=headers)
    r.raise_for_status()
    print('Migration archive %d deleted' % args.id)


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


def start(args):
    headers = {
        'Accept': 'application/vnd.github.wyandotte-preview+json',
        'Authorization': 'token %s' % args.token,
    }
    data = {'repositories': args.repository}
    if args.lock:
        data['lock_repositories'] = True
    r = requests.post('https://api.github.com/user/migrations', json=data, headers=headers)
    r.raise_for_status()
    print('Migration id %d created' % r.json()['id'])


parser = argparse.ArgumentParser(description='Export GitHub projects using migration API')
parser.add_argument('--token', help='GitHub personal access token\nhttps://github.com/settings/tokens')
subparsers = parser.add_subparsers(help='command')

parser_delete = subparsers.add_parser('delete', description='Delete a migration archive')
parser_delete.add_argument('id', type=int, help='Migration id')
parser_delete.set_defaults(func=delete)

parser_download = subparsers.add_parser('download', description='Fetch URL for downloading the migration archive')
parser_download.add_argument('id', type=int, help='Migration id')
parser_download.add_argument('filename', help='Filename to save as')
parser_download.set_defaults(func=download)

parser_list = subparsers.add_parser('list', description='List user migrations')
parser_list.set_defaults(func=list_migrations)

parser_list_user_repos = subparsers.add_parser('list-user-repos', description='List user repositories')
parser_list_user_repos.add_argument('username', help='GitHub username')
parser_list_user_repos.set_defaults(func=list_user_repos)

parser_start = subparsers.add_parser('start', description='Initiate generation of a user migration archive')
parser_start.add_argument('--lock', action='store_const', const=True, help='Lock the repositories to prevent changes during migration')
parser_start.add_argument('repository', nargs='+', help='Repository to include in archive')
parser_start.set_defaults(func=start)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
