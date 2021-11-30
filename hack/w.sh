export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
watch "docker ps;kubectl get nodes;kubectl get pods -A;crictl pods;crictl images"
