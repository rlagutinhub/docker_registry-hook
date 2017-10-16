#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
python3 gen_config.py \
 -token "replace-token-name" \
 -mailserver "mail.example.com" \
 -hooks "mailer1" "./mailer1.py" \
 -hooks "mailer2" "./mailer2.py" \
 -hooks "mailer3" "./mailer3.py" \
 -mailport 25 \
 -mailfrom "registry-hook@example.com" \
 -mailto "username@example.com"

{
    "token": "replace-token-name",
    "hooks": {
        "hello": "./mailer.py"
    },
    "mailserver": "mail.example.com",
    "mailport": 25,
    "mailfrom": "registry-hook@example.com",
    "mailto": "username@example.com"
}
"""

import os
import sys
import json
import datetime

config_file = './config.json'


def gen_config(argv):

    opts = dict()
    hooks = dict()

    while argv:

        if argv[0][0] == '-' and argv[0][1:] == 'token':
            opts[argv[0][1:]] = argv[1]
        elif argv[0][0] == '-' and argv[0][1:] == 'mailserver':
            opts[argv[0][1:]] = argv[1]
        elif argv[0][0] == '-' and argv[0][1:] == 'mailport':
            opts[argv[0][1:]] = argv[1]
        elif argv[0][0] == '-' and argv[0][1:] == 'mailfrom':
            opts[argv[0][1:]] = argv[1]
        elif argv[0][0] == '-' and argv[0][1:] == 'mailto':
            opts[argv[0][1:]] = argv[1]
        elif argv[0][0] == '-' and argv[0][1:] == 'hooks':

            for index, item in enumerate(argv[1:]):
                if list(item)[0] != '-':
                    if index % 2 == 0:
                        hooks[item] = argv[1:][index + 1]
                else:
                    break

        argv = argv[1:]

    opts['hooks'] = hooks

    return opts


def old_config(filename):

    if os.path.exists(filename):
        os.rename(filename, filename + '.' +
                  datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f') + '.old')


def new_config(filename, jsondata):

    # with open(filename, 'w') as f:
    #     json.dump(jsondata, f, indent=4)

    f = open(filename, 'w')
    json.dump(jsondata, f, indent=4)
    f.close()

    return True


if __name__ == '__main__':

    old_config(config_file)
    new_config(config_file, gen_config(sys.argv[1:]))
