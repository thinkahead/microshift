Build the image using docker
```
docker build -t karve/sensehat-dotnet .
docker push karve/sensehat-dotnet
```

Build the image using podman 
```
buildah bud -t docker.io/karve/sensehat-dotnet .
podman push docker.io/karve/sensehat-dotnet
```
