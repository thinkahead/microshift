# Containerized Microshift running on MacBook Pro

Instructions
```
docker pull docker.io/rootfs/ushift:macos
docker volume rm ushift-vol;docker volume create ushift-vol
docker run -d --rm --name ushift --privileged -v /lib/modules:/lib/modules -v ushift-vol:/var/lib -p 6443:6443 docker.io/rootfs/ushift:macos
docker exec -ti ushift bash
export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
journalctl -u microshift -f
systemctl status microshift
kubectl get nodes -w
kubectl get pods -A -w
watch "kubectl get nodes;kubectl get pods -A"
```

- Demo video for Containerized Microshift running on MacBook Pro https://asciinema.org/a/MJZ69vE544HEUi2fpmwtcGpZe
- All Microshift Recordings https://gist.github.com/rootfs/5f1fb90d88fb08182b9d51d99282efd9

