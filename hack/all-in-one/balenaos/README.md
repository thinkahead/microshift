Login to https://dashboard.balena-cloud.com/ and create a fleet microshift
```
balena login
# Build microshift image on the Raspberry Pi 4
balena deploy microshift -h mydevice.local -p 2375 --build
balena ssh mydevice.local

balena-engine volume rm microshift-data;balena-engine volume create microshift-data
mkdir /mnt/data/hpvolumes
balena-engine volume rm microshift-data;balena-engine run -d --rm --name microshift -h microshift.example.com --privileged -v /lib/modules:/lib/modules -v microshift-data:/var/lib -v /mnt/data/hpvolumes:/var/hpvolumes -p 6443:6443 -p 8000:80 balenaos_main
balena-engine exec -it microshift bash
export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
watch "oc get nodes;oc get pods -A;crictl images;crictl pods"
exit # From microshift container
exit # From balenaOS device

balena-engine volume inspect microshift-data
mkdir ~/balena-microshift
cd ~/balena-microshift
scp -P 22222 root@mydevice.local:/var/lib/docker/volumes/microshift-data/_data/microshift/resources/kubeadmin/kubeconfig .
export KUBECONFIG=~/balena-microshift/kubeconfig
alias oc="oc --insecure-skip-tls-verify"
ping mydevice.local # Get the ipaddress and replace in line below
sed -i "s|127.0.0.1|$ipaddress|g" $KUBECONFIG
watch "oc --insecure-skip-tls-verify get nodes;oc --insecure-skip-tls-verify get pods -A"



```
