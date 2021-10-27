Fedora 34 on a Raspberry Pi 4
=============================

### On the Mac
```
Download Fedora Server 34 raw image for aarch64 https://download.fedoraproject.org/pub/fedora/linux/releases/34/Server/aarch64/images/Fedora-Server-34-1.2.aarch64.raw.xz
Use the balenaEtcher on Mac to write the above image to MicroSDXC card
Attach the MicroSDXC card to the Raspberry Pi 4
```

### On the RPI4/ARM64
- Have a Keyboard and Monitor connected to the Raspberry Pi
- During first boot, create user fedora. Also set root password
- Nightly Builds for microshift rpms https://copr.fedorainfracloud.org/coprs/g/redhat-et/microshift-nightly/
```
# ssh as user fedora 
sudo su -

# Enlarge the 3rd partition
sudo growpart /dev/mmcblk0 3
# Resize the physical volume
sudo pvresize /dev/mmcblk0p3
# Extend the root filesystem
sudo lvextend -l +100%FREE /dev/fedora_fedora/root
# Resize root partition
sudo xfs_growfs -d /


curl https://copr.fedorainfracloud.org/coprs/g/redhat-et/microshift-nightly/repo/fedora-34/group_redhat-et-microshift-nightly-fedora-34.repo -o /etc/yum.repos.d/microshift-nightly-fedora34.repo
cat << EOF > /etc/cni/net.d/100-crio-bridge.conf
{
    "cniVersion": "0.4.0",
    "name": "crio",
    "type": "bridge",
    "bridge": "cni0",
    "isGateway": true,
    "ipMasq": true,
    "hairpinMode": true,
    "ipam": {
        "type": "host-local",
        "routes": [
            { "dst": "0.0.0.0/0" }
        ],
        "ranges": [
            [{ "subnet": "10.42.0.0/24" }]
        ]
    }
}
EOF
dnf install -y microshift

hostnamectl set-hostname fedora.example.com # This 
systemctl enable crio
systemctl start crio
systemctl enable microshift
systemctl start microshift

systemctl enable firewalld --now
firewall-cmd --zone=public --permanent --add-port=6443/tcp
firewall-cmd --zone=public --permanent --add-port=30000-32767/tcp
firewall-cmd --zone=public --permanent --add-port=2379-2380/tcp
firewall-cmd --zone=public --add-masquerade --permanent
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=443/tcp --permanent
firewall-cmd --zone=public --add-port=10250/tcp --permanent
firewall-cmd --zone=public --add-port=10251/tcp --permanent
firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16
firewall-cmd --reload
firewall-cmd --permanent --change-zone=eth0 --zone=public

ARCH=arm64
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/$ARCH/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin

export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods"
```
