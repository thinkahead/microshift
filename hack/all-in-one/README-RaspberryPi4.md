Fedora 34 on a Raspberry Pi 4
=============================

## Instructions for running microshift

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

hostnamectl set-hostname fedora.example.com # the host needs a fqdn domain for microshift to work well
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

## Samples
Run the mysql and nginx samples as mentioned at https://github.com/thinkahead/microshift/blob/main/hack/all-in-one/README-Jetson-Nano.md#samples-to-run-on-microshift

CentOS 8 on a Raspberry Pi 4
=============================

1. Download the CentOS image and write to Microsdxc
    1. Either use the image from https://people.centos.org/pgreco/CentOS-Userland-8-stream-aarch64-RaspberryPI-Minimal-4/ or
https://people.centos.org/pgreco/CentOS-Userland-8-aarch64-RaspberryPI-Minimal-4/ and convert to stream https://ostechnix.com/how-to-migrate-to-centos-stream-8-from-centos-linux-8/
    2. Write to Microsdxc card
    3. Insert Microsdxc into Raspberry Pi4 and poweron
    4. Login using root/centos

2. Extend the disk
```
sudo growpart /dev/mmcblk0 3
sudo fdisk -lu
resize2fs /dev/mmcblk0p3
```

If you used the non-stream image, convert to stream as follows after boot
```
cat /etc/redhat-release
dnf install centos-release-stream
dnf swap centos-{linux,stream}-repos
dnf distro-sync
```

3. Add you public key
```
mkdir ~/.ssh
vi ~/.ssh/authorized_keys
chmod 600 ~/.ssh
chmod 644 ~/.ssh/authorized_keys
```

4. Set the hostname with a domain
```
hostnamectl set-hostname centos.example.com
```

5. Update kernel and kernel parameters
    1. To avoid the "Error: Following Cgroup subsystem not mounted: [memory]", append the following to /boot/cmdline.txt
```
 cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
```
    2. Update the kernel to avoid the "Error cannot access '/sys/fs/cgroup/cpu/cpu.cfs_quota_us': No such file or directory"
        - https://github.com/cri-o/cri-o/issues/4307
        - https://github.com/kubernetes/kubeadm/issues/2335#issuecomment-716989252
        - https://forums.centos.org/viewtopic.php?f=55&t=76363#p321465
        - https://people.centos.org/pgreco/rpi_aarch64_el8/
    Change kernel from raspberrypi2-kernel4-5.4.60-v8.1.el8.aarch64 to raspberrypi2-kernel4.5.4.155-v8.1.el8
Create /etc/yum.repos.d/pgrepo.repo
```
[pgrepo]
name=Raspberry Pi Kernel raspberrypi2-kernel4.5.4.155-v8.1.el8
type=rpm-md
baseurl=https://people.centos.org/pgreco/rpi_aarch64_el8/
gpgcheck=0
enabled=1
dnf -y update

reboot

ls -l /sys/fs/cgroup/cpu/cpu.cfs_quota_us # This should be present for microshift to work
```

6. Setup crio and microshift
```
rpm -qi selinux-policy # selinux-policy-3.14.3-82.el8
dnf -y install 'dnf-command(copr)'
# dnf -y copr enable rhcontainerbot/container-selinux
# dnf copr enable @redhat-et/microshift-nightly # Do not use this
curl https://copr.fedorainfracloud.org/coprs/g/redhat-et/microshift-nightly/repo/centos-stream-8/   -o /etc/yum.repos.d/microshift-nightly-centos-stream-8.repo
cat /etc/yum.repos.d/microshift-nightly-centos-stream-8.repo

VERSION=1.22
curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/CentOS_8/devel:kubic:libcontainers:stable.repo
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:${VERSION}.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:${VERSION}/CentOS_8/devel:kubic:libcontainers:stable:cri-o:${VERSION}.repo
cat /etc/yum.repos.d/devel\:kubic\:libcontainers\:stable\:cri-o\:${VERSION}.repo

dnf -y install cri-o cri-tools microshift
systemctl enable --now crio
```

7. Check that cni plugins
```
ls /opt/cni/bin/ # empty
ls  /usr/libexec/cni # cni plugins
```

8. Download kubectl and test microshift
```
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/$ARCH/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin
watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods"
journalctl -u microshift -f
journalctl -u crio -f
```
