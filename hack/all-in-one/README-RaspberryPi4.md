Fedora 34 on a Raspberry Pi 4
=============================

## Instructions for running MicroShift
MicroShift Nightly Fedora 34 aarch64 https://download.copr.fedorainfracloud.org/results/@redhat-et/microshift-nightly/fedora-34-aarch64/

### On the Mac
Download Fedora Server 34 raw image for aarch64 https://download.fedoraproject.org/pub/fedora/linux/releases/34/Server/aarch64/images/Fedora-Server-34-1.2.aarch64.raw.xz
```
Use the balenaEtcher on Mac to write the above image to MicroSDXC card
Attach the MicroSDXC card to the Raspberry Pi 4
```

### On the RPI4/ARM64
- Have a Keyboard and Monitor connected to the Raspberry Pi
- During first boot, create user fedora. Also set root password
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

hostnamectl set-hostname fedora.example.com # the host needs a fqdn domain for MicroShift to work well
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

# Install kubectl
ARCH=arm64
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/$ARCH/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin

# Install the oc client
wget https://mirror.openshift.com/pub/openshift-v4/arm64/clients/ocp/candidate/openshift-client-linux.tar.gz
mkdir tmp;cd tmp
tar -zxvf ../openshift-client-linux.tar.gz
mv -f oc /usr/local/bin
cd ..;rm -rf tmp

export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods"
```

## Samples
Run the mysql and nginx samples as mentioned at https://github.com/thinkahead/microshift/blob/main/hack/all-in-one/README-Jetson-Nano.md#samples-to-run-on-microshift

CentOS 8 on a Raspberry Pi 4
=============================
## Steps to install and run MicroShift
1. Download the CentOS image and write to Microsdxc card
    1. Either use the image from https://people.centos.org/pgreco/CentOS-Userland-8-stream-aarch64-RaspberryPI-Minimal-4/ (I did not use this image) or
https://people.centos.org/pgreco/CentOS-Userland-8-aarch64-RaspberryPI-Minimal-4/ (I used this image). For latter, we will convert to stream as documented at https://ostechnix.com/how-to-migrate-to-centos-stream-8-from-centos-linux-8/ in Section 3 below.
    2. Write to Microsdxc card
    3. Insert Microsdxc into Raspberry Pi4 and poweron
    4. Login using root/centos

2. Extend the disk
    ```
    sudo growpart /dev/mmcblk0 3
    sudo fdisk -lu
    resize2fs /dev/mmcblk0p3
    ```
    or (I haven't tried this)
    ```
    rootfs-expand
    ```

3. If you used the non-stream image, convert to stream
    ```
    cat /etc/redhat-release
    dnf install centos-release-stream
    dnf swap centos-{linux,stream}-repos
    dnf distro-sync
    ```

4. Add your public key, enable wifi
    ```
    mkdir ~/.ssh
    vi ~/.ssh/authorized_keys
    chmod 600 ~/.ssh
    chmod 644 ~/.ssh/authorized_keys

    nmcli device wifi list
    nmcli device wifi connect $ssid -ask
    ```

5. Set the hostname with a domain
    ```
    hostnamectl set-hostname centos.example.com
    ```

6. Update kernel and kernel parameters
    1. To avoid the "Error: Following Cgroup subsystem not mounted: [memory]", append the following to /boot/cmdline.txt
        ```
         cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
        ```
    2. Update the kernel to avoid the "Error cannot access '/sys/fs/cgroup/cpu/cpu.cfs_quota_us': No such file or directory"
        ```
        ls -l /sys/fs/cgroup/cpu/cpu.cfs_quota_us # This needs to be present for MicroShift to work, Let's fix it
        ```

        Change kernel from raspberrypi2-kernel4-5.4.60-v8.1.el8.aarch64 to raspberrypi2-kernel4.5.4.155-v8.1.el8 as follows:

        Create /etc/yum.repos.d/pgrepo.repo
        ```
        [pgrepo]
        name=Raspberry Pi Kernel raspberrypi2-kernel4.5.4.155-v8.1.el8
        type=rpm-md
        baseurl=https://people.centos.org/pgreco/rpi_aarch64_el8/
        gpgcheck=0
        enabled=1
        ```

        Update and reboot
        ```
        dnf -y update
        reboot
        ```

        Verify
        ```
        mount | grep cgroup
        cat /proc/cgroups | column -t
        ls -l /sys/fs/cgroup/cpu/cpu.cfs_quota_us # This needs to be present for MicroShift to work
        ```

    3. References
        - https://github.com/cri-o/cri-o/issues/4307
        - https://github.com/kubernetes/kubeadm/issues/2335#issuecomment-716989252
        - https://forums.centos.org/viewtopic.php?f=55&t=76363#p321465
        - https://people.centos.org/pgreco/rpi_aarch64_el8/

7. Setup crio and MicroShift
    Microshift Nightly CentOS Stream 8 aarch64 https://download.copr.fedorainfracloud.org/results/@redhat-et/microshift-nightly/centos-stream-8-aarch64/
    ```
    rpm -qi selinux-policy # selinux-policy-3.14.3-82.el8
    dnf -y install 'dnf-command(copr)'
    # dnf -y copr enable rhcontainerbot/container-selinux
    # dnf copr enable @redhat-et/microshift-nightly # Do not use this
    curl https://copr.fedorainfracloud.org/coprs/g/redhat-et/microshift-nightly/repo/centos-stream-8/ -o /etc/yum.repos.d/microshift-nightly-centos-stream-8.repo
    cat /etc/yum.repos.d/microshift-nightly-centos-stream-8.repo

    VERSION=1.22 # We should probably be using the 1.21, but 1.22 works
    curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/CentOS_8/devel:kubic:libcontainers:stable.repo
    sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:${VERSION}.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:${VERSION}/CentOS_8/devel:kubic:libcontainers:stable:cri-o:${VERSION}.repo
    cat /etc/yum.repos.d/devel\:kubic\:libcontainers\:stable\:cri-o\:${VERSION}.repo

    dnf -y install cri-o cri-tools microshift
    ```

    Check that cni plugins are present and start MicroShift
    ```
    ls /opt/cni/bin/ # empty
    ls /usr/libexec/cni # cni plugins
    systemctl enable --now crio
    systemctl start crio
    systemctl enable --now microshift
    systemctl start microshift
    ```

8. Download kubectl/oc and test MicroShift
    ```
    # Install kubectl
    ARCH=arm64
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/$ARCH/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin

    # Install the oc client
    wget https://mirror.openshift.com/pub/openshift-v4/arm64/clients/ocp/candidate/openshift-client-linux.tar.gz
    mkdir tmp;cd tmp
    tar -zxvf ../openshift-client-linux.tar.gz
    mv -f oc /usr/local/bin
    cd ..;rm -rf tmp

    watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods"

    journalctl -u microshift -f
    journalctl -u crio -f
    ```
9. Cleanup MicroShift/cri-o images and pods
    ```
    systemctl stop microshift
    crictl rm --all --force
    crictl rmp --all --force
    crictl rmi --all
    pkill -9 conmon
    pkill -9 pause
    rm -rf /var/lib/microshift
    systemctl stop crio
    rm -rf /var/lib/containers/*
    systemctl start crio
    ```
## Errors
1. openshift-ingress router-default pod does not start - It is usually when you switch between wlan0 and eth0 or when the ipaddress gets changed. To fix this, run the "Cleanup" steps and restart MicroShift.

Downloading cni plugins
=======================
Required if you are missing the flannel plugin
- https://github.com/containernetworking/plugins/releases/ (Don't need this)
- https://github.com/flannel-io/cni-plugin/releases
```
wget https://github.com/containernetworking/plugins/releases/download/v1.0.1/cni-plugins-linux-arm64-v1.0.1.tgz # Don't need this
wget https://github.com/flannel-io/cni-plugin/releases/download/v1.0.0/flannel-arm64
mv flannel-arm64 /usr/libexec/cni/flannel
```

Installing sense_hat and RTIMULib on CentOS 8
=============================================
1. Install sensehat
    ```
    yum -y install zlib zlib-devel libjpeg-devel gcc gcc-c++ i2c-tools python3-devel python3 python3-pip
    pip3 install Cython Pillow numpy sense_hat
    ```
2. Install RTIMULib
    ```
    git clone https://github.com/RPi-Distro/RTIMULib.git
    # git clone https://github.com/HongshiTan/RTIMULib2.git # Not supported, does not work
    cd RTIMULib/
    cd Linux/python
    python3 setup.py build
    python3 setup.py install
    cd ../..
    cd RTIMULib
    mkdir build
    cd build
    cmake ..
    make -j4
    make install
    ldconfig
    cd /root/RTIMULib/Linux/RTIMULibDrive11
    make -j4
    make install
    RTIMULibDrive11
    cd /root/RTIMULib/Linux/RTIMULibDrive10
    make -j4
    make install
    RTIMULibDrive10

    yum -y install qt5-qtbase-devel
    cd /root/RTIMULib/Linux/RTIMULibDemoGL
    qmake-qt5
    make -j4
    make install
    ```

Samples to run on Raspberry Pi 4
================================
- Image using pygame and SenseHat sent to Node Red https://github.com/thinkahead/microshift/blob/main/raspberry-pi/sensehat/README.md
- Image using cv2, Object Detection using tflite and SenseHat temperature reading sent to Node Red  https://github.com/thinkahead/microshift/blob/main/raspberry-pi/object-detection/README.md

Problems
========
1. The pod cannot resolve external ip addresses, to fix this, run
    ```
    systemctl stop firewalld
    ```
    or https://github.com/k3s-io/k3s/issues/24#issuecomment-475567218
    ```
    firewall-cmd --permanent --direct --add-rule ipv4 filter INPUT 1 -i cni0 -s 10.42.0.0/16 -j ACCEPT
    firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 1 -s 10.42.0.0/15 -j ACCEPT
    firewall-cmd --reload
    ```
    or https://github.com/k3s-io/k3s/issues/24#issuecomment-614330334
    ```
    firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i cni0 -j ACCEPT
    firewall-cmd --reload
    ```

Installing pip and sense_hat on CentOS 7
========================================
I tried the armhfp (32 bit) image for CentOS 7 from http://isoredirect.centos.org/altarch/7/isos/armhfp/. The SenseHat worked on this image but I did not install MicroShift on it.
1. Installing pip
    ```
    wget https://files.pythonhosted.org/packages/0f/74/ecd13431bcc456ed390b44c8a6e917c1820365cbebcb6a8974d1cd045ab4/pip-10.0.1-py2.py3-none-any.whl
    python pip-10.0.1-py2.py3-none-any.whl/pip install --no-index pip-10.0.1-py2.py3-none-any.whl
    ```
2. SenseHat wheel https://pypi.org/project/sense-hat/#files
    ```
    wget https://files.pythonhosted.org/packages/13/cd/f30b6709e01cacd0f9e2882ce3c0633ea2862771a75f4a9d02a56db9ec9a/sense_hat-2.2.0-py2.py3-none-any.whl
    python pip-10.0.1-py2.py3-none-any.whl/pip install --no-index sense_hat-2.2.0-py2.py3-none-any.whl
    ```


