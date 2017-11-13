## Docker: docker_registry-hook

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/registry-hook/

-	Python 3 BASEHTTPSERVER for docker registry notifications. The server send a message when the image pushed to registry.
-	Base image python:3

### Install

```console
git clone https://github.com/rlagutinhub/docker_registry-hook.git
cd registry-hook
```

#### Configure Docker private registry


##### Docker network:

```console
docker network create -d bridge registry_net-prod
```

##### Docker volume:

```console
docker volume create registry-data
docker volume create registry-certs
docker volume create registry-auth
docker volume create registry-conf
```

##### Self-signed certificate:
https://docs.docker.com/engine/security/https/
https://docs.docker.com/registry/insecure/#using-self-signed-certificates
https://docs.docker.com/registry/insecure/#troubleshooting-insecure-registry

```console
cd /var/lib/docker/volumes/registry-certs/_data/
openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 3650 -out domain.crt
cp domain.crt /etc/pki/ca-trust/source/anchors/hub.docker.example.com.crt
update-ca-trust
systemctl restart docker.service
```

##### Auth:

```console
cd /var/lib/docker/volumes/registry-auth/_data/
docker run --entrypoint htpasswd registry:2 -Bbn hubadm1 1qaz@WSX > htpasswd
docker run --entrypoint htpasswd registry:2 -Bbn hubadm2 1qaz@WSX >> htpasswd
docker run --entrypoint htpasswd registry:2 -Bbn hubadm3 1qaz@WSX >> htpasswd
docker container prune
```

##### Config:
https://github.com/docker/distribution/blob/master/cmd/registry/config-example.yml

```console
cd /var/lib/docker/volumes/registry-conf/_data/
cat <<EOF > config.yml
version: 0.1
log:
  fields:
    service: registry
  hooks:
    - type: mail
      levels:
        - panic
      options:
        smtp:
          addr: mail.example.com:25
          insecure: true
        from: registry@example.com
        to:
          - username@example.com
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
notifications:
 endpoints:
   - name: mailer
     url: http://registry-hook:8000?token=replace-token-name&hook=mailer
     timeout: 1000ms
     threshold: 1
     backoff: 1s
   - name: logger
     url: http://registry-hook:8000?token=replace-token-name&hook=logger
     timeout: 1000ms
     threshold: 1
     backoff: 1s
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3

EOF
```

##### Replace token
In the config.yml replace value "replace-token-name" by echo $(openssl rand -base64 30 | sed 's=/=\\/=g')

Example token EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu
http://registry-hook:8000?token=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu&hook=mailer

##### Docker container registry:

```console
docker run -dit \
 -v registry-data:/var/lib/registry \
 -v registry-auth:/auth \
 -e "REGISTRY_AUTH=htpasswd" \
 -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
 -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
 -v registry-certs:/certs \
 -e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt" \
 -e "REGISTRY_HTTP_TLS_KEY=/certs/domain.key" \
 -e "REGISTRY_STORAGE_DELETE_ENABLED=true" \
 -v registry-conf:/etc/docker/registry \
 --network=registry_net-prod -p 5000:5000/tcp \
 --restart=always \
 --name registry \
 registry:2
```

#### Configure Docker private registry hook:

##### Docker Image:

```console
docker build -t rlagutinhub/registry-hook:201710161400 .
```

##### Docker network:

```console
docker network create -d bridge registry_net-prod
```

##### Docker volume:

```console
docker volume create registry_hook-scr
```

##### Docker container registry-hook:
Replace value "replace-token-name" by token (see above) !!!

Example: -e "TOKEN=EyZhNUYfvrcxrxIEmhoFMD5GByZpvWRm60YJCBvu"

```console
docker run -dit \
 -e "TOKEN=replace-token-name" \
 -e "MAILSERVER=mail.example.com" \
 -e "HOOKS=mailer /scr/mailer.py logger /scr/logger.sh" \
 -e "MAILPORT=25" \
 -e "MAILFROM=registry-hook@example.com" \
 -e "MAILTO=username@example.com" \
 -v registry_hook-scr:/scr \
 --network=registry_net-prod -p 8000:8000/tcp \
 --restart=always \
 --name registry-hook \
 rlagutinhub/registry-hook:201710161400
```

Other:

```console
docker ps -a
docker container ls -a
docker image ls -a
docker exec -it registry sh (After complete work input: exit)
docker exec -it registry-hook bash (After complete work input: exit)
docker logs -f registry
docker logs -f registry-hook
docker container stop registry
docker container stop registry-hook
docker container rm registry
docker container rm registry-hook
docker network rm registry_net-prod
docker volume rm registry-data
docker volume rm registry-certs
docker volume rm registry-auth
docker volume rm registry-conf
docker volume rm registry_hook-scr
docker image rm registry:2
docker image rm rlagutinhub/registry-hook:201710161400
```
