https://developers.redhat.com/blog/2019/04/24/how-to-run-systemd-in-a-container#other_cool_features_about_podman_and_systemd

```
podman build -t systemd .
podman run -ti -p 8080:80 systemd
curl localhost:8080
```
