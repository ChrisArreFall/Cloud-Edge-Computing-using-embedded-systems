# Steps to create images for intel-x86-64 and raspberrypi3 BSPs

For these builds it is neccessary to buy a licence for Wind River Linux LTS 19. I am in no way owner of anything or any code that is included in this step by step.
You will need some knowledge in the Yocto project and a basic understaning in layers and packagea

# Intel-x86-64 BSP 

For this BSP it is necassary to first initialize the WRL LTS 19 project.

```sh
$ mkdir -p k3sLTS19_x86_64
$ cd k3sLTS19_x86_64
$ git clone --branch WRLINUX_10_19_BASE https://github.com/WindRiver-Labs/wrlinux-x.git
$ ./wrlinux-x/setup.sh --machines intel-x86-64 --templates feature/docker
```
Then we need to enable internet downoads, simply vim to conf/local.conf and change:
```sh
BB_NO_NETWORK ?= '0'
```
to
```sh
BB_NO_NETWORK ?= '1'
```

To build this, simply use this command from build:
```sh
$ . environment-setup-x86_64-wrlinuxsdk-linux
$ . oe-init-build-env
$ bitbake wrlinux-image-std
```

# Raspberry pi 3

For this BSP, we have to add some layers and make some changes.

For this BSP it is necassary to first initialize the WRL LTS 19 project.
```sh
$ mkdir -p k3sLTS19_x86_64
$ cd k3sLTS19_x86_64
$ git clone --branch WRLINUX_10_19_BASE https://github.com/WindRiver-Labs/wrlinux-x.git
$ ./wrlinux-x/setup.sh --all-layers --dl-layers --templates feature/docker
```
After that we need to add the meta-raspberrypi layer
```sh
$ cd layers
$ git clone -b zeus git://git.yoctoproject.org/meta-raspberrypi
$ . environment-setup-x86_64-wrlinuxsdk-linux
$ . oe-init-build-env
$ bitbake-layers add-layer ../layers/meta-raspberrypi
$ ./wrlinux-x/setup.sh --all-layers --dl-layers --templates feature/docker
```
Then we need to enable internet downoads, simply vim to conf/local.conf and change:

```sh
BB_NO_NETWORK ?= '0'
```
to
```sh
BB_NO_NETWORK ?= '1'
```

Then we have to change/add our machine or BSP to that same file, in this case:
```sh
MACHINE ??= "raspberrypi3"
```
After that we need to check that our distro is set to wrlinux:
```sh
DISTRO ??= "wrlinux"
```
And add rpi-sdimg to out fstypes
```sh
IMAGE_FSTYPES += "tar.bz2 tar.xz ext3 rpi-sdimg"
```
We also need to let WRL accept layers that are not supported:
```sh
INHERIT_DISTRO_remove = "whitelist"
```
We need to change the version of docker we are using:
```sh
IMAGE_INSTALL_remove = "docker"
IMAGE_INSTALL_append = " docker-ce"
```
We need to add the virtualization packages from the virtualizatin layer
```sh
DISTRO_FEATURES_append = " virtualization"
```
Finally we add change the kernel and enable UART
```sh
ENABLE_UART = "1"
SECURITY_CFLAGS_pn-tini_append = " ${SECURITY_NOPIE_CFLAGS}"
PREFERRED_PROVIDER_virtual/kernel = 'linux-raspberrypi-rt'
```
To build this, simply use this command from build:
```sh
$ bitbake wrlinux-image-std
```




























