#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# ----------------------------------------------------------------------------
# NAME:    REGISTRY-HOOK.PY
# DESC:    PYTHON 3 BASEHTTPSERVER FOR DOCKER REGISTRY NOTIFICATIONS. THE SERVER SEND A MESSAGE WHEN THE IMAGE PUSHED TO REGISTRY.
# DATE:    13.10.2017
# LANG:    PYTHON
# AUTOR:   LAGUTIN R.A.
# CONTACT: RLAGUTIN@MTA4.RU
# ----------------------------------------------------------------------------

'''
BaseHTTPServer for Docker Registry Notifications.
The server sends a message when the image pushed to private docker registry.

https://docs.docker.com/registry/configuration/
https://docs.docker.com/registry/notifications
https://docs.python.org/3/library/http.server.html

----- Request Start ----->

Request: /?token=replace-token-name&hook=hello
Host: 192.168.1.254:8000
User-Agent: Go-http-client/1.1
Content-Length: 1241
Content-Type: application/vnd.docker.distribution.events.v1+json
Accept-Encoding: gzip

{
   "events": [
      {
         "id": "938360cd-0ea6-4b99-af1a-2de513045f0e",
         "timestamp": "2017-10-05T17:31:52.044234167Z",
         "action": "push",
         "target": {
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "size": 948,
            "digest": "sha256:e3bcb0baf5cea75c897ef4a5b360d9331ebc6d44d3b53fc5c340ab1719e4ec3a",
            "length": 948,
            "repository": "nginx",
            "url": "https://hub.docker.example.com:5000/v2/nginx/manifests/sha256:e3bcb0baf5cea75c897ef4a5b360d9331ebc6d44d3b53fc5c340ab1719e4ec3a",
            "tag": "1806"
         },
         "request": {
            "id": "5164005d-1a77-44d9-adb4-186621a5291f",
            "addr": "172.17.0.1:48164",
            "host": "hub.docker.example.com:5000",
            "method": "PUT",
            "useragent": "docker/17.06.0-ce go/go1.8.3 git-commit/02c1d87 kernel/4.12.13-300.fc26.x86_64 os/linux arch/amd64 UpstreamClient(Docker-Client/17.06.0-ce \\(linux\\))"
         },
         "actor": {
            "name": "hubadm1"
         },
         "source": {
            "addr": "c1e8fc89a82b:5000",
            "instanceID": "c546ff65-e7d0-4def-92aa-b9e45af732d3"
         }
      }
   ]
}
<----- Request End -----
'''

import sys
import time
import json
import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):

        self._set_headers()

        return True

    def do_GET(self):

        request_path = self.path

        # print("\n----- Request Start ----->\n")
        # print(request_path)
        # print(self.headers)
        # print("<----- Request End -----\n")

        self._set_headers()

        self.wfile.write(
            "<html><head><titleDocker Registry Notifications</title></head>".encode("utf-8"))
        self.wfile.write(
            "<body><b>BaseHTTPServer for Docker Registry Notifications.</b><br><i>The server sends a message when the image pushed to private docker registry.</i>".encode("utf-8"))
        self.wfile.write("<br><br>".encode("utf-8"))
        self.wfile.write(
            "<a href='https://docs.docker.com/registry/configuration/'>Docker registry configuration</a><br>".encode("utf-8"))
        self.wfile.write(
            "<a href='https://docs.docker.com/registry/notifications'>Docker registry notifications</a><br>".encode("utf-8"))
        self.wfile.write(
            "<a href='https://docs.python.org/3/library/http.server.html'>Python 3 HTTP servers</a><br>".encode("utf-8"))
        self.wfile.write("<br><hr>".encode("utf-8"))
        self.wfile.write(("You accessed Request: <b>%s</b>" %
                          request_path).encode("utf-8"))
        self.wfile.write("</body></html>".encode("utf-8"))

        return True

    def do_POST(self):

        config = load_config()

        request_path = self.path
        request_path_parse = url_to_dict(request_path)
        token = str(request_path_parse['token'])
        hook = str(request_path_parse['hook'])

        request_headers = self.headers
        # content_length = request_headers.getheaders('content-length')
        content_length = request_headers.get_all('content-length', 0)
        content_length_check = int(content_length[0]) if content_length else 0

        content_body = self.rfile.read(content_length_check)
        content_body_json = json.loads(content_body)

        # print("\n----- Request Start ----->\n")
        # print('Request: ' + request_path)
        # print(request_headers)
        # print(content_body)
        # print("<----- Request End -----\n")

        self._set_headers()

        if content_body_json:

            repository = content_body_json['events'][0]['target']['repository']
            url = content_body_json['events'][0]['target']['url']
            mediaType = content_body_json['events'][0]['target']['mediaType']

            try:
                tag = content_body_json['events'][0]['target']['tag']

            except KeyError:
                tag = None

            digest = content_body_json['events'][0]['target']['digest']
            timestamp = content_body_json['events'][0]['timestamp']
            actor = content_body_json['events'][0]['actor']['name']
            action = content_body_json['events'][0]['action']

            # print(repository, url, mediaType, tag,
            #       digest, timestamp, actor, action)

        if token == config['token']:
            if hook:
                hook_value = config['hooks'].get(hook)

                # print(token, hook, hook_value)

                if hook_value:
                    try:
                        subprocess.call([hook_value, str(repository), str(url),
                                         str(mediaType), str(tag), str(digest),
                                         str(timestamp), str(actor), str(action)])
                        return True
                    except OSError:
                        print(time.asctime() + " " + "Error: exec hook ",
                              hook_value, str(repository), str(url),
                              str(mediaType), str(tag), str(digest),
                              str(timestamp), str(actor), str(action))
                        return False
                else:
                    print(time.asctime() + " " + "Error: hook not defined.")
                    return False

            else:
                print(time.asctime() + " " +
                      "Error: hook not found in config.json.")
                return False
        else:
            print(time.asctime() + " " +
                  "Error: token is not equal to token in config.json.")
            return False


def url_to_dict(url):

    url_dict = dict()

    for item in url.split("&"):
        item = item.replace("/", "")
        item = item.replace("?", "")
        url_dict[item.split("=")[0]] = item.split("=")[1]

    return url_dict


def load_config():

    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def main(server_class=HTTPServer, handler_class=RequestHandler, server='0.0.0.0', port=8000):

    server_address = (server, port)
    httpd = server_class(server_address, handler_class)
    print(time.asctime() + " " + "Server Starts - %s:%s" %
          (server, port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime() + " " + "Server Stops - %s:%s" %
          (server, port))

    return True


if __name__ == '__main__':

    if len(sys.argv) == 2:
        sys.exit(main(port=int(sys.argv[1])))
    else:
        sys.exit(main())
