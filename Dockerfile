# vendor="Lagutin R.A."
# maintainer="Lagutin R.A. <rlagutin@mta4.ru>"
# name="docker_registry-hook"
# description="Python 3 BASEHTTPSERVER for docker registry notifications. The server send a message when the image pushed to registry."
# version="v.2-prod."
# release-date="201711111400"

# ---------------------------------------------------------------------------

# https://docs.docker.com/registry/configuration/
# https://docs.docker.com/registry/notifications/

# https://hub.docker.com/_/python/
# https://docs.docker.com/get-started/part2/
# https://docs.python.org/3/library/http.server.html
# https://gist.github.com/bradmontgomery/2219997

# ---------------------------------------------------------------------------
# Configure Docker private registry:

# Docker network:
# docker network create -d bridge registry_net-prod

# Docker volume:
# docker volume create registry-data
# docker volume create registry-certs
# docker volume create registry-auth
# docker volume create registry-conf

# Self-signed certificate
# https://docs.docker.com/engine/security/https/
# https://docs.docker.com/registry/insecure/#using-self-signed-certificates
# https://docs.docker.com/registry/insecure/#troubleshooting-insecure-registry
# cd /var/lib/docker/volumes/registry-certs/_data/
# openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 3650 -out domain.crt
# cp domain.crt /etc/pki/ca-trust/source/anchors/hub.docker.example.com.crt
# update-ca-trust
# systemctl restart docker.service

# Auth
# cd /var/lib/docker/volumes/registry-auth/_data/
# docker run --entrypoint htpasswd registry:2 -Bbn hubadm1 1qaz@WSX > htpasswd
# docker run --entrypoint htpasswd registry:2 -Bbn hubadm2 1qaz@WSX >> htpasswd
# docker run --entrypoint htpasswd registry:2 -Bbn hubadm3 1qaz@WSX >> htpasswd
# docker container prune

# Config
# https://github.com/docker/distribution/blob/master/cmd/registry/config-example.yml
# cd /var/lib/docker/volumes/registry-conf/_data/
# cat <<EOF > config.yml
# version: 0.1
# log:
#   fields:
#     service: registry
#   hooks:
#     - type: mail
#       levels:
#         - panic
#       options:
#         smtp:
#           addr: mail.example.com:25
#           insecure: true
#         from: registry@example.com
#         to:
#           - username@example.com
# storage:
#   cache:
#     blobdescriptor: inmemory
#   filesystem:
#     rootdirectory: /var/lib/registry
# http:
#   addr: :5000
#   headers:
#     X-Content-Type-Options: [nosniff]
# notifications:
#  endpoints:
#    - name: mailer
#      url: http://registry-hook:8000?token=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu&hook=mailer
#      timeout: 1000ms
#      threshold: 1
#      backoff: 1s
#    - name: logger
#      url: http://registry-hook:8000?token=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu&hook=logger
#      timeout: 1000ms
#      threshold: 1
#      backoff: 1s
# health:
#   storagedriver:
#     enabled: true
#     interval: 10s
#     threshold: 3
#
# EOF

# Replace token
# In the config.yml replace value "replace-token-name" by echo $(openssl rand -base64 30 | sed 's=/=\\/=g')
# Example token EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu - http://registry-hook:8000?token=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu&hook=mailer

# Docker container registry:
# docker run -dit \
#  -v registry-data:/var/lib/registry \
#  -v registry-auth:/auth \
#  -e "REGISTRY_AUTH=htpasswd" \
#  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
#  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
#  -v registry-certs:/certs \
#  -e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt" \
#  -e "REGISTRY_HTTP_TLS_KEY=/certs/domain.key" \
#  -e "REGISTRY_STORAGE_DELETE_ENABLED=true" \
#  -v registry-conf:/etc/docker/registry \
#  --network=registry_net-prod -p 5000:5000/tcp \
#  --restart=always \
#  --name registry \
#  registry:2

# ---------------------------------------------------------------------------
# Configure Docker private registry hook:

# Docker Image:
# docker build -t rlagutinhub/docker_registry-hook .

# Docker network:
# docker network create -d bridge registry_net-prod

# Docker volume:
# docker volume create registry_hook-scr

# Docker container registry-hook:
# Replace value "replace-token-name" by token (see above) !!! Example: -e "TOKEN=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu"
# docker run -dit \
#  -e "TOKEN=replace-token-name" \
#  -e "MAILSERVER=mail.example.com" \
#  -e "HOOKS=mailer /scr/mailer.py logger /scr/logger.sh" \
#  -e "MAILPORT=25" \
#  -e "MAILFROM=registry-hook@example.com" \
#  -e "MAILTO=username@example.com" \
#  -v registry_hook-scr:/scr \
#  --network=registry_net-prod -p 8000:8000/tcp \
#  --restart=always \
#  --name registry-hook \
#  rlagutinhub/docker_registry-hook:latest

# ---------------------------------------------------------------------------
# Other:

# docker ps -a
# docker container ls -a
# docker image ls -a
# docker exec -it registry sh (After complete work input: exit)
# docker exec -it registry-hook bash (After complete work input: exit)
# docker logs -f registry
# docker logs -f registry-hook
# docker container stop registry
# docker container stop registry-hook
# docker container rm registry
# docker container rm registry-hook
# docker network rm registry_net-prod
# docker volume rm registry-data
# docker volume rm registry-certs
# docker volume rm registry-auth
# docker volume rm registry-conf
# docker volume rm registry_hook-scr
# docker image rm registry:2
# docker image rm rlagutinhub/docker_registry-hook:latest

FROM python:3

LABEL rlagutinhub.community.vendor="Lagutin R.A." \
	rlagutinhub.community.maintainer="Lagutin R.A. <rlagutin@mta4.ru>" \
	rlagutinhub.community.name="docker_registry-hook" \
	rlagutinhub.community.description="Python 3 BASEHTTPSERVER for docker registry notifications. The server send a message when the image pushed to registry." \
	rlagutinhub.community.version="v.2-prod." \
	rlagutinhub.community.release-date="201711111400"

COPY scr /scr
COPY app /app

WORKDIR /app

RUN chmod +x *.sh *.py /scr/* && pip3 install -U -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python3", "app.py", "8000"]
