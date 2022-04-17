# Provisioning Fedora CoreOS on the Raspberry Pi 4
To run FCOS on a Raspberry Pi 4 via U-Boot the SD card or USB disk needs to be prepared on another system and then the disk moved to the RPi4. We will create this disk in a Fedora VM on the MacBook Pro, then copy the disk out from the VM and write to MicroSDXC card

## Create a Fedora VM in VirtualBox using the Vagrantfile
```
vagrant up
vagrant ssh
sudo su -
git clone https://github.com/thinkahead/microshift.git
cd microshift/raspberry-pi/coreosbuilder
```

## Create the FCOS Image within the VM
Install the dependencies for creating a coreos image on the VM
```
dnf -y install butane coreos-installer make rpi-imager
```

Update the password and key in the build/coreos.bu. You can generate the secure password hash with mkpasswd
```
podman run -ti --rm quay.io/coreos/mkpasswd --method=yescrypt
```

Create the ignition config
```
rm -rf dist;mkdir dist
cp -r build/etc dist/
butane --files-dir dist --pretty --strict build/coreos.bu > dist/coreos.ign
```

Prepare the disk with partitions
```
tmp_rpm_dest_path=/tmp/rpi4boot
tmp_pi_boot_path="/tmp/rpi4boot/boot/efi"
tmp_efipart_path=/tmp/fcosefipart
rm -rf $tmp_rpm_dest_path $tmp_efipart_path

fedora_release=35 # The target Fedora Release
# Grab RPMs from the Fedora Linux repositories
mkdir -p $tmp_pi_boot_path
dnf install -y --downloadonly --release=$fedora_release --forcearch=aarch64 --destdir=$tmp_rpm_dest_path  uboot-images-armv8 bcm283x-firmware bcm283x-overlays
# Now extract the contents of the RPMs and copy the proper u-boot.bin for the RPi4 into place
for filename in `ls $tmp_rpm_dest_path/*.rpm`; do rpm2cpio $filename | cpio -idv -D $tmp_rpm_dest_path; done
cp $tmp_rpm_dest_path/usr/share/uboot/rpi_4/u-boot.bin $tmp_pi_boot_path/rpi4-u-boot.bin

# Create raw image
dd if=/dev/zero of=/home/my-coreos.img bs=1024 count=4194304
losetup -fP /home/my-coreos.img
losetup --list

# Run coreos-installer to install to the target disk
coreos-installer install -a aarch64 -i dist/coreos.ign /dev/loop0
lsblk /dev/loop0 -J -oLABEL,PATH
efi_part=`lsblk /dev/loop0 -J -oLABEL,PATH | jq -r '.blockdevices[] | select(.label == "EFI-SYSTEM")'.path`
echo $efi_part
mkdir -p $tmp_efipart_path
mount $efi_part $tmp_efipart_path
unalias cp
cp -r $tmp_pi_boot_path/* $tmp_efipart_path
ls $tmp_efipart_path/start.elf
umount $efi_part
```

## Copy the my-coreos.img from the VM to the MacOS
```
vagrant scp :/home/my-coreos.img .
open .
```

## Write to MicroSDXC card using balenaEtcher

## Insert the MicroSDXC card into the Raspberry Pi 4 and boot

## Reference
https://docs.fedoraproject.org/en-US/fedora-coreos/provisioning-raspberry-pi4/
