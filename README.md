# github-gdpr-export

Export GitHub projects using the experimental [user migrations](https://developer.github.com/v3/migrations/users/) API.

This tool allows exporting a copy of all your projects, something the user migrations API does not provide out of box.

## Personal access token

You need a personal access token to use the user migrations API.

1. Open https://github.com/settings/tokens
2. Generate new token
3. Token description: github-gdpr-export
4. Select scopes: [x] repo

Save this token somewhere.

## Usage

    $ ./github-gdpr-export.py --token $TOKEN list-users-repos > repolist.txt
    $ xargs ./github-gdpr-export.py --token $TOKEN start < repolist.txt
    Migration id 12345 created
    $ ./github-gdpr-export.py --token $TOKEN list
    id       state     lock
    12345    exported  0
    $ ./github-gdpr-export.py --token $TOKEN download 12345 export.tar.gz
    Downloading "<URL>" into "export.tar.gz"
