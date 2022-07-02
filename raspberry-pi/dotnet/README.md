Build the image using docker
```
docker build -t karve/sensehat-dotnet .
docker push karve/sensehat-dotnet
```

Build the image using podman 
```
buildah bud -t docker.io/karve/sensehat-dotnet .
skopeo copy --dest-creds='user:password' containers-storage:docker.io/karve/sensehat-dotnet:latest docker://karve/sensehat-dotnet:latest
```
or
```
podman build docker.io/karve/sensehat-dotnet
podman push docker.io/karve/sensehat-dotnet
```
