#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Python send email https://docs.python.org/3/library/email.examples.html

./mailer.py \
  "nginx" \
  "https://hub.docker.example.com:5000/v2/nginx/manifests/sha256:e3bcb0baf5cea75c897ef4a5b360d9331ebc6d44d3b53fc5c340ab1719e4ec3a" \
  "application/vnd.docker.distribution.manifest.v2+json" \
  "1806" \
  "sha256:e3bcb0baf5cea75c897ef4a5b360d9331ebc6d44d3b53fc5c340ab1719e4ec3a" \
  "2017-09-27T16:31:36.973015849Z" \
  "hubadm1" \
  "push"
'''

import sys
import time
import json
import smtplib
from email.message import EmailMessage


def main(argv):

    repository = argv[0]
    url = argv[1]
    mediaType = argv[2]
    tag = argv[3]
    digest = argv[4]
    timestamp = argv[5]
    actor = argv[6]
    action = argv[7]

    hub = url.split('/')

    config = load_config()
    mailserver = config['mailserver']
    mailport = config['mailport']
    mailfrom = config['mailfrom']
    mailto = config['mailto']

    if (repository
            and url
            and mediaType == "application/vnd.docker.distribution.manifest.v2+json"
            and tag
            and digest
            and timestamp
            and actor
            and action == "push"
            and hub):

        msg = EmailMessage()
        msg['Subject'] = "docker-registry-notification" + " - " + hub[2]
        msg['From'] = mailfrom
        msg['To'] = mailto
        msg.set_content("""\
repository: %s
url: %s
mediaType: %s
tag: %s
digest: %s
timestamp: %s
actor: %s
action: %s
""" % (repository, url, mediaType, tag, digest, timestamp, actor, action))

        try:
            s = smtplib.SMTP(mailserver, mailport)
            s.send_message(msg)
            print(time.asctime() + " " + "Success sendmail - %s:%s" %
                  (mailserver, mailport))
            return True
        except:
            print(time.asctime() + " " + "Failed sendmail - %s:%s" %
                  (mailserver, mailport))
            return False


def load_config():

    with open('config.json', 'r') as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
