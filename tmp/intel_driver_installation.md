# Installation

This page describes software installation for Intel® Data Center GPU Max Series and
Intel® Data Center GPU Flex Series. For information about other Intel GPUs, see 
[Client GPU Installation](client/overview). The steps described here are not validated
for client GPUs.

**NOTE**: For readability purposes, Intel® Data Center GPU Max Series
might be refered to as Max, while Intel® Data Center GPU Flex Series
might be referred to as Flex.


```{contents} Table of Contents
:depth: 2
:local:
:backlinks: none
```

## Supported Hardware

Linux* operating system distribution support varies by hardware family. The following
table indicates which streams are supported for each hardware family and OS combination.
Support indicates Intel has validated that combination. Other combinations may work,
however they are not explicitly tested by Intel and issues reported against non-supported
combination are subject to Intel's evaluation prior to fixing in the corresponding release
stream.

### Intel® Data Center GPU Max Series and Intel® Data Center GPU Flex Series

| Usage  | Ubuntu Server            | Red Hat Enterprise Linux | SUSE Linux Enterprise Server | 
|:-------|:-------------------------|:-------------------------|:-----------------------------|
| Max    | LTS, Production, Rolling | LTS, Production, Rolling | LTS, Production, Rolling     |    
| Flex   | LTS, Production, Rolling | LTS, Production, Rolling | N/A                          |    

### Intel® Arc™ Graphics

| Usage  | Ubuntu Desktop (HWE)     | Red Hat Enterprise Linux | SUSE Linux Enterprise Server | 
|:-------|:-------------------------|:-------------------------|:-----------------------------|
| Client | Rolling                  | N/A                      | N/A                          |

For client install (Intel® Arc™ Graphics) steps see [Client GPU Installation](client/overview). 
To identify which hardware you have see [Hardware Devices](../devices/hardware-table).

## Release Streams

Three types of release streams are available for Intel® Data Center GPUs.

|                   | Rolling​ | Production​ | Long Term Support - LTS​ |
|:------------------|:--------|:-----------|:------------------------|
| Purpose​           | Early adopters who want to evaluate new features and where new hardware enablement first appears.​ | For production use with 6 months * of support of bug/security fixes, no new features​ | For production use with 3 years* support of bug/security fixes, no new features ​|
| Release lifetime*​ | Supported only until next published rolling release.​ | 6 months​* | 3 years​* |

The instructions on this page will install the LTS version, which is recommended
for most users. For information on configuring your system to install from a 
different stream, see [Release Streams](release-streams).

For client install steps see [Client GPU Installation](client/overview).

## Install Steps

Instructions for each OS follow this sequence:

1. Install the Intel GPU driver repository.
2. Install GPU drivers for bare metal access and management.
3. Adjust kernel boot parameters as needed.
4. Install the oneAPI toolkit and other components as required.

**NOTE**: The Intel GPU driver releases are designed to use your operating 
system's package manager for installation and dependency resolution.

### Red Hat Enterprise Linux Install Steps

These steps describe installation of the unified LTS driver release for
Intel® Data Center GPU Flex Series and Intel® Data Center GPU Max Series
on Red Hat Enterprise Linux.

Supported Red Hat Enterprise Linux (RHEL) versions: 
 - Red Hat Enterprise Linux 8.6, 8.8, 8.9, 9.0, 9.2, 9.3

**NOTE**: To install the kernel modules provided, your system needs
to support the Dynamic Kernel Module System (DKMS), which is not provided
by the official Red Hat Enterprise Linux package repositories. You can install
DKMS onto your system through the [Extra Packages for Enterprise Linux](https://docs.fedoraproject.org/en-US/epel/)
(EPEL) project.

If DKMS is not available, the following instructions will fail with a package
dependency not being met for DKMS.

The following steps pick one of the options for DKMS install, but this can be changed to any of the other 
methods described in the previous link to match your system setup.

#### Red Hat Enterprise Linux Package repository

To add the online network package repository for the **LTS** releases:

```bash
. /etc/os-release
if [[ ! " 8.6 8.8 8.9 9.0 9.2 9.3 " =~ " ${VERSION_ID} " ]]; then
  echo "RHEL version ${VERSION_ID} not supported"
else
  echo "Installing online network repository for ${VERSION_ID}"
  sudo dnf install -y 'dnf-command(config-manager)'
  sudo dnf config-manager --add-repo \
    https://repositories.intel.com/gpu/rhel/${VERSION_ID}/lts/2350/unified/intel-gpu-${VERSION_ID}.repo
fi
```

**Optional**: Instead of the online network package repository steps above, you can
download and use the offline repository:

```bash
. /etc/os-release
if [[ ! " 8.6 8.8 8.9 9.0 9.2 9.3 " =~ " ${VERSION_ID} " ]]; then
  echo "RHEL version ${VERSION_ID} not supported"
else
  wget https://repositories.intel.com/gpu/rhel/${VERSION_ID}/lts/2350/intel-gpu-rhel-${VERSION_ID}-2350.run
  chmod +x intel-gpu-rhel-${VERSION_ID}-2350.run
  sudo ./intel-gpu-rhel-${VERSION_ID}-2350.run
fi
```

This will extract and enable the Intel® Data Center GPU Flex Series and Intel® 
Data Center GPU Max Series repository in your OS repository management configuration.

**NOTE**: Apart from enabling the repository, the offline installer does not make any 
other changes to the OS configuration.

To add the EPEL repository needed for DKMS:

```bash
. /etc/os-release
sudo dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-${VERSION_ID%.*}.noarch.rpm
sudo dnf config-manager --disable epel
```

NOTE: After installing EPEL, it is disabled by default as EPEL currently has packages which conflict with
the packages provided by Intel. It is enabled for a single command below to allow DKMS to be installed.

#### Red Hat Enterprise Linux Package installation

The kernel and xpu-smi packages can be installed on a bare metal system.  Installation
on the host is sufficient for hardware management and support of the runtimes in containers 
and bare metal.

```bash
sudo dnf install -y kernel-headers flex bison 
sudo dnf install --enablerepo epel -y intel-fw-gpu intel-i915-dkms xpu-smi
sudo reboot 
```
**NOTE**: There are known limitations associated with the installation of the intel-i915-dkms package.
You may encounter a warning about an unknown symbol during the installation process.
Please be aware that this is a known issue and does not affect the functionality of the software.

**Compute and Media Runtimes**

```bash
sudo dnf install -y \
  intel-opencl intel-media intel-mediasdk libmfxgen1 libvpl2\
  level-zero intel-level-zero-gpu mesa-dri-drivers mesa-vulkan-drivers \
  mesa-vdpau-drivers libdrm mesa-libEGL mesa-libgbm mesa-libGL \
  mesa-libxatracker libvpl-tools intel-metrics-discovery \
  intel-metrics-library intel-igc-core intel-igc-cm \
  libva libva-utils intel-gmmlib libmetee intel-gsc intel-ocloc
```

**Development packages**

```bash
sudo dnf install -y --refresh \
  intel-igc-opencl-devel level-zero-devel intel-gsc-devel libmetee-devel \
  level-zero-devel 
```

**Install verification tools**
```bash
sudo dnf install -y hwinfo clinfo
```

### SUSE Linux Enterprise Server Install Steps 

These steps describe installation of the unified LTS driver release for
Intel® Data Center GPU Flex Series and Intel® Data Center GPU Max Series
on SUSE Linux Enterprise Server.

Supported SUSE Linux Enterprise Server (SLES) versions: 
 - SUSE Linux Enterprise Server 15 SP4, 15 SP5

#### SUSE Linux Enterprise Server Package repository

To add the online network package repository for the **LTS** releases:

```bash
. /etc/os-release
VERSION_SP=${VERSION_ID//./sp}
if [[ ! " 15sp4 15sp5 " =~ " ${VERSION_SP} " ]]; then
  echo "SLES version ${VERSION_ID} not supported"
else
  sudo zypper addrepo -r \
    https://repositories.intel.com/gpu/sles/${VERSION_SP}/lts/2350/unified/intel-gpu-${VERSION_SP}.repo
  sudo zypper --non-interactive --gpg-auto-import-keys refresh
fi
```

**Optional**: Instead of the online network package repository steps above, you can
download and use the offline repository:

```bash
. /etc/os-release
VERSION_SP=${VERSION_ID//./sp}
if [[ ! " 15sp4 15sp5 " =~ " ${VERSION_SP} " ]]; then
  echo "SLES version ${VERSION_ID} not supported"
else
  wget https://repositories.intel.com/gpu/sles/${VERSION_SP}/lts/2350/intel-gpu-sles-${VERSION_SP}-2350.run
  chmod +x intel-gpu-sles-${VERSION_SP}-2350.run
  sudo ./intel-gpu-sles-${VERSION_SP}-2350.run
fi
```

This will extract and enable the Intel® Data Center GPU Flex Series and Intel® 
Data Center GPU Max Series repository in your OS repository management configuration.

**NOTE**: Apart from enabling the repository, the offline installer does not make any 
other changes to the OS configuration.

#### SUSE Linux Enterprise Server Package installation

Prior to installing the packages for Intel GPUs on SUSE Linux Enterprise Server, 
you need to ensure the following Modules and Extensions are enabled in your 
SUSE subscription in order for all required packages to be available:

* Basesystem Module
* Development Tools Module
* Product-WE
* Package-HUB

For information on configuring extensions and modules, refer to [SUSE Modules Article](https://documentation.suse.com/sles/15-SP5/html/SLES-all/article-modules.html).

Once your system has the required modules and extensions enabled, you can continue
with installing the GPU packages.

The kernel and xpu-smi packages can be installed on a bare metal system.  Installation
on the host is sufficient for hardware management and support of the runtimes in containers and bare metal.

Prior to installing `intel-i915-dkms` below, if you are not running the latest kernel from SUSE,
you need to ensure your system has the kernel devel package for your kernel. To verify that 
package is installed, you can run: `zypper install --oldpackage kernel-default-devel-$(uname -r)`

```bash
sudo zypper install -y lsb-release linux-kernel-headers flex bison intel-fw-gpu intel-i915-dkms xpu-smi
```

NOTE: When installing a kernel module which has not been supplied by SUSE, for example the 
module that is built when installing the `intel-i915-dkms` package, you must set
the system configuration `allow_unsupported_modules` to `1`. Failure to enable that option will
prevent the kernel from loading the intel-i915-dkms generated kernel module.

The instructions below are based on the instructions supplied by SUSE:

```bash
# Copy the default into /etc.
sudo cp /lib/modprobe.d/10-unsupported-modules.conf /etc/modprobe.d/10-unsupported-modules.conf
# Modify the default to set allow_unsupported_modules to 1
sudo sed -i -E 's,allow_unsupported_modules 0,allow_unsupported_modules 1,g' \
  /etc/modprobe.d/10-unsupported-modules.conf
```

If you will be booting your system from an initrd and have dracut configured, make sure to
re-run dracut after changing the above parameter:

```bash
# Update the initrd
sudo dracut -f
```

For additional details related to the `allow_unsupported_modules` option, see [SUSE's Working with unsupported modules](https://documentation.suse.com/sles/15-SP4/html/SLES-all/cha-adm-support.html#sec-admsupport-kernel-unsupported).

Once you have installed intel-i915-dkms and ensured allow_unsupported_modules is 
set to 1, you can reboot the system to load the new module:

```bash
sudo reboot
```

**Compute and Media Runtimes**

```bash
sudo zypper install -y \
  intel-level-zero-gpu level-zero intel-gsc intel-opencl intel-ocloc \
  intel-media-driver libigfxcmrt7 libvpl2 libvpl-tools libmfxgen1 libmfx1
```

**Development Packages**

```bash
sudo zypper install -y \
  libigdfcl-devel intel-igc-cm libigfxcmrt-devel level-zero-devel
```

**Install Verification Tools**
```bash
sudo zypper install -y clinfo libOpenCL1 libva-utils hwinfo
```

### Ubuntu Install Steps

These steps describe installation of the unified LTS driver release for
Intel® Data Center GPU Flex Series and Intel® Data Center GPU Max Series
on Ubuntu Server.

**NOTE**: Datacenter installs are validated with Ubuntu Server.  Client 
installs are validated with Ubuntu Desktop using the Rolling Stable release.
For client usage, see [Client GPU Installation](client/overview).

Supported Ubuntu versions:
 - Ubuntu Server 22.04.1 (5.15 LTS kernel)

#### Ubuntu Package Repository

Make sure prerequisites to add repository access are available:

```bash
sudo apt update
sudo apt install -y gpg-agent wget
```

To add the online network package repository for the **LTS** releases:

```bash
. /etc/os-release
if [[ ! " jammy " =~ " ${VERSION_CODENAME} " ]]; then
  echo "Ubuntu version ${VERSION_CODENAME} not supported"
else
  wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    sudo gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu ${VERSION_CODENAME}/lts/2350 unified" | \
    sudo tee /etc/apt/sources.list.d/intel-gpu-${VERSION_CODENAME}.list
  sudo apt update
fi
```

**Optional**: Instead of the online network package repository steps above, you can
download and use the offline repository:

```bash
. /etc/os-release
if [[ ! " jammy " =~ " ${VERSION_CODENAME} " ]]; then
  echo "Ubuntu version ${VERSION_CODENAME} not supported"
else
  wget https://repositories.intel.com/gpu/ubuntu/dists/jammy/lts/2350/intel-gpu-ubuntu-${VERSION_CODENAME}-2350.run
  chmod +x intel-gpu-ubuntu-${VERSION_CODENAME}-2350.run
  sudo ./intel-gpu-ubuntu-${VERSION_CODENAME}-2350.run
fi
```

This will extract and enable the Intel® Data Center GPU Flex Series and Intel® 
Data Center GPU Max Series repository in your OS repository management configuration.

**NOTE**: Apart from enabling the repository, the offline installer does not make any 
other changes to the OS configuration.

#### Ubuntu Package Installation

The kernel and xpu-smi packages can be installed on a bare metal system.  Installation
on the host is sufficient for hardware management and support of the runtimes in containers and bare metal.

```bash
sudo apt install -y \
  linux-headers-$(uname -r) \
  linux-modules-extra-$(uname -r) \
  flex bison \
  intel-fw-gpu intel-i915-dkms xpu-smi 
sudo reboot 
```

**Compute and Media Runtimes**

```bash
sudo apt install -y \
  intel-opencl-icd intel-level-zero-gpu level-zero \
  intel-media-va-driver-non-free libmfx1 libmfxgen1 libvpl2 \
  libegl-mesa0 libegl1-mesa libegl1-mesa-dev libgbm1 libgl1-mesa-dev libgl1-mesa-dri \
  libglapi-mesa libgles2-mesa-dev libglx-mesa0 libigdgmm12 libxatracker2 mesa-va-drivers \
  mesa-vdpau-drivers mesa-vulkan-drivers va-driver-all vainfo hwinfo clinfo
```

**Development Packages**

```bash
sudo apt install -y \
  libigc-dev intel-igc-cm libigdfcl-dev libigfxcmrt-dev level-zero-dev
```

### Configuring Render Group Membership

To access GPU capabilities, the active user must be able to access DRM render nodes
in /dev/dri.

The following command will list the group assigned ownership of the render nodes and will also list the groups
the active user is a member of:

```bash
stat -c "%G" /dev/dri/render*
groups ${USER}
```

If the active user is not a member of the same group used by the DRM render nodes (usually 'render'), 
add the user to the render node group.

```bash
sudo gpasswd -a ${USER} render
```

This will be sufficient for shells created after this update.  To change the group ID of the current
shell:

```bash
newgrp render
```

## Verify Install 

### To Verify that Expected Hardware is Working with the i915 Driver (Flex and Max)

```bash
hwinfo --display
```

On SLES, `hwinfo` might be installed in `/usr/sbin` and not in the default
user path so you need to run via:

```bash
/usr/sbin/hwinfo --display
```

Here is an example output for Intel® Data Center GPU Max 1550 (device ID 0x0bd5):

```bash
51: PCI 8c00.0: 0380 Display controller
  [Created at pci.386]
  Unique ID: JefI.QAjErpDk4H4
  Parent ID: juVd.xbjkZcxCQYD
  SysFS ID: /devices/pci0000:89/0000:89:02.0/0000:8a:00.0/0000:8b:01.0/0000:8c:00.0
  SysFS BusID: 0000:8c:00.0
  Hardware Class: graphics card
  Model: "Intel Display controller"
  Vendor: pci 0x8086 "Intel Corporation"
  Device: pci 0x0bd5
  SubVendor: pci 0x8086 "Intel Corporation"
  SubDevice: pci 0x0000
  Revision: 0x2f
  Driver: "i915"
  Driver Modules: "i915"
  Memory Range: 0x23fe7e000000-0x23fe7fffffff (ro,non-prefetchable)
  Memory Range: 0x236000000000-0x237fffffffff (ro,non-prefetchable)
  IRQ: 138 (447 events)
  Module Alias: "pci:v00008086d00000BD5sv00008086sd00000000bc03sc80i00"
  Driver Info #0:
    Driver Status: i915 is active
    Driver Activation Cmd: "modprobe i915"
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #26 (PCI bridge)
```
A list of device IDs is included in the Graphics processor table section.

### xpu-smi Device Information and Telemetry

The Intel® XPU Manager (Intel® XPUM) tool provides a wide range of functionality covering system administration,
GPU monitoring, diagnostics, and configuration for Intel data center GPUs.  It can be used in full featured
mode with a RESTful API as well as via the simplified xpu-smi tool.

Some example xpu-smi command lines are shown next.


Available GPU device discovery:

```bash
$ xpu-smi discovery
+-----------+--------------------------------------------------------------------------------------+
| Device ID | Device Information                                                                   |
+-----------+--------------------------------------------------------------------------------------+
| 0         | Device Name: Intel(R) Data Center GPU Flex 170                                       |
|           | Vendor Name: Intel(R) Corporation                                                    |
|           | UUID: 00000000-0000-0000-6769-df256e271362                                           |
|           | PCI BDF Address: 0000:4d:00.0                                                        |
|           | DRM Device: /dev/dri/card1                                                           |
|           | Function Type: physical                                                              |
+-----------+--------------------------------------------------------------------------------------+
```


Detailed device information, including installed driver and firmware versions:

```bash
$ sudo xpu-smi discovery -d 0
+-----------+--------------------------------------------------------------------------------------+
| Device ID | Device Information                                                                   |
+-----------+--------------------------------------------------------------------------------------+
| 0         | Device Type: GPU                                                                     |
|           | Device Name: Intel(R) Data Center GPU Flex 170                                       |
|           | Vendor Name: Intel(R) Corporation                                                    |
|           | UUID: 00000000-0000-0000-6769-df256e271362                                           |
|           | Serial Number: LQAC13401787                                                          |
|           | Core Clock Rate: 2050 MHz                                                            |
|           | Stepping: C0                                                                         |
|           |                                                                                      |
|           | Driver Version: I915_23.4.15_PSB_230307.15                                           |
|           | Kernel Version: 5.15.0-47-generic                                                    |
|           | GFX Firmware Name: GFX                                                               |
|           | GFX Firmware Version: DG02_1.3267                                                    |
|           | GFX Firmware Status: normal                                                          |
|           | GFX Data Firmware Name: GFX_DATA                                                     |
|           | GFX Data Firmware Version: 0x46b                                                     |
|           | GFX PSC Firmware Name: GFX_PSCBIN                                                    |
|           | GFX PSC Firmware Version:                                                            |
|           | AMC Firmware Name: AMC                                                               |
|           | AMC Firmware Version:                                                                |
|           |                                                                                      |
|           | PCI BDF Address: 0000:4d:00.0                                                        |
|           | PCI Slot: J37 - Riser 1, Slot 1                                                      |
|           | PCIe Generation: 4                                                                   |
|           | PCIe Max Link Width: 16                                                              |
|           | OAM Socket ID:                                                                       |
|           |                                                                                      |
|           | Memory Physical Size: 14248.00 MiB                                                   |
|           | Max Mem Alloc Size: 4095.99 MiB                                                      |
|           | ECC State: enabled                                                                   |
|           | Number of Memory Channels: 2                                                         |
|           | Memory Bus Width: 128                                                                |
|           | Max Hardware Contexts: 65536                                                         |
|           | Max Command Queue Priority: 0                                                        |
|           |                                                                                      |
|           | Number of EUs: 512                                                                   |
|           | Number of Tiles: 1                                                                   |
|           | Number of Slices: 1                                                                  |
|           | Number of Sub Slices per Slice: 32                                                   |
|           | Number of Threads per EU: 8                                                          |
|           | Physical EU SIMD Width: 8                                                            |
|           | Number of Media Engines: 2                                                           |
|           | Number of Media Enhancement Engines: 2                                               |
|           |                                                                                      |
|           | Number of Xe Link ports:                                                             |
|           | Max Tx/Rx Speed per Xe Link port:                                                    |
|           | Number of Lanes per Xe Link port:                                                    |
+-----------+--------------------------------------------------------------------------------------+
```


GPU telemetry:

```bash
$sudo xpu-smi stats -d 0
+-----------------------------+--------------------------------------------------------------------+
| Device ID                   | 0                                                                  |
+-----------------------------+--------------------------------------------------------------------+
| GPU Utilization (%)         | 0                                                                  |
| EU Array Active (%)         |                                                                    |
| EU Array Stall (%)          |                                                                    |
| EU Array Idle (%)           |                                                                    |
|                             |                                                                    |
| Compute Engine Util (%)     | 0; Engine 0: 0, Engine 1: 0, Engine 2: 0, Engine 3: 0              |
| Render Engine Util (%)      | 0; Engine 0: 0                                                     |
| Media Engine Util (%)       | 0                                                                  |
| Decoder Engine Util (%)     | Engine 0: 0, Engine 1: 0                                           |
| Encoder Engine Util (%)     | Engine 0: 0, Engine 1: 0                                           |
| Copy Engine Util (%)        | 0; Engine 0: 0                                                     |
| Media EM Engine Util (%)    | Engine 0: 0, Engine 1: 0                                           |
| 3D Engine Util (%)          |                                                                    |
+-----------------------------+--------------------------------------------------------------------+
| Reset                       |                                                                    |
| Programming Errors          |                                                                    |
| Driver Errors               |                                                                    |
| Cache Errors Correctable    |                                                                    |
| Cache Errors Uncorrectable  |                                                                    |
| Mem Errors Correctable      |                                                                    |
| Mem Errors Uncorrectable    |                                                                    |
+-----------------------------+--------------------------------------------------------------------+
| GPU Power (W)               | 44                                                                 |
| GPU Frequency (MHz)         | 2050                                                               |
| GPU Core Temperature (C)    | 40                                                                 |
| GPU Memory Temperature (C)  |                                                                    |
| GPU Memory Read (kB/s)      | 1346                                                               |
| GPU Memory Write (kB/s)     | 286                                                                |
| GPU Memory Bandwidth (%)    | 0                                                                  |
| GPU Memory Used (MiB)       | 26                                                                 |
| Xe Link Throughput (kB/s)   |                                                                    |
+-----------------------------+--------------------------------------------------------------------+

```

For more information on Intel® XPUM, see

 - [Intel® XPUM README](https://github.com/intel/xpumanager/blob/master/README.md)
 - [xpu-smi user guide](https://github.com/intel/xpumanager/blob/master/doc/smi_user_guide.md)


### To Smoke Test the Compute Stack (Flex and Max)

```bash
clinfo | head -n 5
```

Example output:

```bash
Number of platforms                               1
  Platform Name                                   Intel(R) OpenCL HD Graphics
  Platform Vendor                                 Intel(R) Corporation
  Platform Version                                OpenCL 3.0
  Platform Profile                                FULL_PROFILE
```

Running the same command without 'head' should display many pages of GPGPU compute capability summary.

### To Smoke Test the Media Stack (Flex only)

```bash
vainfo
```

Intel® Data Center GPU Max Series does not include codec capabilities, so the
expected output has minimal entry points.

```bash
vainfo: VA-API version: 1.18 (libva 2.17.0)
vainfo: Driver version: Intel iHD driver for Intel(R) Gen Graphics - 23.1.4 (12e141d)
vainfo: Supported profile and entrypoints
      VAProfileNone                   : VAEntrypointVideoProc
      VAProfileNone                   : VAEntrypointStats
```

Intel® Data Center GPU Flex Series and client GPUs provide hardware codecs,
so many entrypoints are expected from vainfo output.

Example output from Intel® Data Center GPU Flex Series:
```bash
vainfo: VA-API version: 1.18 (libva 2.17.0)
vainfo: Driver version: Intel iHD driver for Intel(R) Gen Graphics - 23.1.4 (12e141d)
vainfo: Supported profile and entrypoints
      VAProfileNone                   : VAEntrypointVideoProc
      VAProfileNone                   : VAEntrypointStats
      VAProfileMPEG2Simple            : VAEntrypointVLD
      VAProfileMPEG2Main              : VAEntrypointVLD
      VAProfileH264Main               : VAEntrypointVLD
      VAProfileH264Main               : VAEntrypointEncSliceLP
      VAProfileH264High               : VAEntrypointVLD
      VAProfileH264High               : VAEntrypointEncSliceLP
      VAProfileJPEGBaseline           : VAEntrypointVLD
      VAProfileJPEGBaseline           : VAEntrypointEncPicture
      VAProfileH264ConstrainedBaseline: VAEntrypointVLD
      VAProfileH264ConstrainedBaseline: VAEntrypointEncSliceLP
      VAProfileHEVCMain               : VAEntrypointVLD
      VAProfileHEVCMain               : VAEntrypointEncSliceLP
      VAProfileHEVCMain10             : VAEntrypointVLD
      VAProfileHEVCMain10             : VAEntrypointEncSliceLP
      VAProfileVP9Profile0            : VAEntrypointVLD
      VAProfileVP9Profile0            : VAEntrypointEncSliceLP
      VAProfileVP9Profile1            : VAEntrypointVLD
      VAProfileVP9Profile1            : VAEntrypointEncSliceLP
      VAProfileVP9Profile2            : VAEntrypointVLD
      VAProfileVP9Profile2            : VAEntrypointEncSliceLP
      VAProfileVP9Profile3            : VAEntrypointVLD
      VAProfileVP9Profile3            : VAEntrypointEncSliceLP
      VAProfileHEVCMain12             : VAEntrypointVLD
      VAProfileHEVCMain422_10         : VAEntrypointVLD
      VAProfileHEVCMain422_12         : VAEntrypointVLD
      VAProfileHEVCMain444            : VAEntrypointVLD
      VAProfileHEVCMain444            : VAEntrypointEncSliceLP
      VAProfileHEVCMain444_10         : VAEntrypointVLD
      VAProfileHEVCMain444_10         : VAEntrypointEncSliceLP
      VAProfileHEVCMain444_12         : VAEntrypointVLD
      VAProfileHEVCSccMain            : VAEntrypointVLD
      VAProfileHEVCSccMain            : VAEntrypointEncSliceLP
      VAProfileHEVCSccMain10          : VAEntrypointVLD
      VAProfileHEVCSccMain10          : VAEntrypointEncSliceLP
      VAProfileHEVCSccMain444         : VAEntrypointVLD
      VAProfileHEVCSccMain444         : VAEntrypointEncSliceLP
      VAProfileAV1Profile0            : VAEntrypointVLD
      VAProfileAV1Profile0            : VAEntrypointEncSliceLP
      VAProfileHEVCSccMain444_10      : VAEntrypointVLD
      VAProfileHEVCSccMain444_10      : VAEntrypointEncSliceLP
```

### Verify VSEC is in use for Intel® Data Center GPU Max Series

To access the full range of Intel® Data Center GPU Max Series telemetry features the intel\_vsec module should be used
instead of intel\_pmt.  The intel\_vsec module supports Max telemetry features while intel\_pmt focuses 
on CPU telemetry.

To check if VSEC change is needed, review output from `xpu-smi discovery -d 0`.  
If you see output like the following, there may be a vsec issue for the device serial number.

```
    Serial Number: unknown
```

   
#### Test that the intel_vsec Module Loads and is Associated with a PCI Device:

```bash
for d in 8086:09A7 8086:4F93 8086:4F95; do sudo lspci -k -d $d; done
```

Should see:
05:00.0 Memory controller: Intel Corporation Device 09A7
  Kernel driver in use: intel-vsec
        Kernel modules: intel_vsec

If intel\_pmt is in use as a kernel driver instead of intel\_vsec(example below), 
change the kernel driver in use.

Example:
05:00.1 System peripheral: Intel Corporation Device 09a7
        Kernel driver in use: intel-pmt
        Kernel modules: intel_pmt, intel_vsec

#### To Change Kernel Driver Module:

Install driverctl tool:

For Red Hat Enterprise Linux:
```bash
sudo dnf install driverctl
```

For SUSE Linux Enterprise Server 15:
A driverctl package is not available for SUSE Linux Enterprise Server15.  Instead, install from the driverctl repo:
```bash
git clone https://gitlab.com/driverctl/driverctl.git
cd driverctl
sudo make install
```

For Ubuntu:
```bash
sudo apt install driverctl
```

Next, check which device the intel-pmt module is linked to.
```bash
sudo driverctl list-devices | grep -iE "pmt"
```

Should see:
0000:8e:00.1 intel-pmt

You may see a different device address than 0000:8e:00.1. 
Use your system's device address in the following command.

```bash
sudo driverctl set-override 0000:8e:00.1 "intel_vsec"
```




## IFWI Update

The Intel® XPUM utility can be used to flash IFWI to a Flex or Max GPU.

Check GFX FW version on devices (that is, for each GPU): 

```bash
sudo xpu-smi discovery -d 0 
sudo xpu-smi discovery -d 1
```

Find the latest firmware version for your hardware from your Intel or OEM portal.
If it is newer than what is currently on your device, install the new firmware with xpu-smi updatefw.
Example:

```bash
sudo xpu-smi updatefw -d 0 -t GFX -f 
/home/intel/ATS_M75_128_B0_PVT_ES_017_gfx_fwupdate_SOC2.bin -y

sudo xpu-smi updatefw -d 0 -t GFX_PSCBIN -f /home/test/PVC_Tuscany_oam_cbb_otf_53G_220803.pscbin
sudo xpu-smi updatefw -d 0 -t GFX -f /home/test/PVC.Fwupdate_Prod_2023.WW26.3_Tuscany_Pcie.bin

```

updatefw options:

```bash
sudo xpu-smi updatefw
Update GPU firmware

Usage: xpu-smi updatefw [Options]
  xpu-smi updatefw -d [deviceId] -t GFX -f [imageFilePath]
  xpu-smi updatefw -d [pciBdfAddress] -t GFX -f [imageFilePath]

Options:
  -h,--help                   Print this help message and exit
  -j,--json                   Print result in JSON format

  -d,--device                 The device ID or PCI BDF address
  -t,--type                   The firmware name. Valid options: GFX, GFX_DATA, GFX_CODE_DATA, GFX_PSCBIN, AMC. AMC firmware update just works on Intel M50CYP server (BMC firmware version is 2.82 or newer) and Supermicro SYS-620C-TN12R server (BMC firmware version is 11.01 or newer).
  -f,--file                   The firmware image file path on this server
  -u,--username               Username used to authenticate for host redfish access
  -p,--password               Password used to authenticate for host redfish access
  -y,--assumeyes              Assume that the answer to any question which would be asked is yes
  --force                     Force GFX firmware update. This parameter only works for GFX firmware.
```

## Architecture Overview

### Introduction
Solutions built using Intel GPU products rely on several software components working together. 
The Intel **GPU Base** (bottom rectangle) provides  standard interfaces to higher level use
cases (top rectangle).

![Software Stack](assets/generic-stack.svg)

The following sections describe the **GPU Base** block diagram components.

### Intel Data Center GPUs

 - [Intel® Data Center GPU Max Series](http://intel.com/maxseriesgpu) Intel’s highest performing, highest density, general-purpose discrete GPU, which packs over 100 billion transistors into a package and contains up to 128 Xe Cores – Intel’s foundational GPU compute building block.
 
 - [Intel® Data Center GPU Flex Series](http://intel.com/flexseriesgpu) Intel’s general-purpose GPU optimized for media stream density and quality. Infused with server capabilities, Intel® Data Center GPU Flex Series enable high levels of reliability, availability, and scalability.  Hardware includes Xe Cores and media acceleration.

### Intel Kernel Driver(s)

The Linux* kernel driver(s) provide the software connection to the Intel GPU hardware. 
The kernel driver(s) are provided today as Dynamic Kernel Module Support ([DKMS](https://github.com/dell/dkms))
drivers "out-of-tree" from the Linux kernel. See [Kernel Driver Types](kernel-driver-types)
for more information on the kernel driver.

### Compute and Media Stacks

The Compute and Media usermode library stacks provide higher level software support of
industry standard APIs. 

 - Compute: Both OpenCL and Level Zero are supported.  These are a foundation for oneAPI GPU acceleration.
 - Media: oneVPL is provided, with integrations for [GStreamer](https://gstreamer.freedesktop.org/)
and [ffmpeg](https://ffmpeg.org/).

### Intel® XPU Manager (Intel® XPUM)

Use [Intel® XPUM](https://github.com/intel/xpumanager) for managing the physical hardware, 
including firmware updates, monitoring,diagnostics, and configuration. Intel® XPUM uses 
the oneAPI Level Zero Sysman API, and exposes standard interfaces for telemetry, 
including [Prometheus](https://prometheus.io/).



## Additional Information

### Install the oneAPI Toolkit

For general instructions, see [Intel® oneAPI Toolkits and Components Installation Guide for Linux* OS](https://www.intel.com/content/www/us/en/docs/oneapi/installation-guide-linux/2023-1/overview.html).

For instructions specific to using the system package manager to install
oneAPI, see [Intel® oneAPI Toolkits and Components Install Using Package Managers](https://www.intel.com/content/www/us/en/docs/oneapi/installation-guide-linux/2023-1/install-using-package-managers.html).

### Kernel Boot Parameters

#### Long Running Compute Workloads

The Intel graphics kernel driver defaults to preventing long running
compute workloads from executing longer than four seconds in order to
prevent display usages from blocking desktop operations due to an errant
shader. This setting is controlled via the i915 kernel module parameter 
`enable_hangcheck`.

To check the current setting:

```
sudo cat /sys/module/i915/parameters/enable_hangcheck
```

A value of Y (default) indicates that the hang check is currently active.

You can change the setting at runtime via:

```
echo N | sudo tee /sys/module/i915/parameters/enable_hangcheck
```

To persist the value after reboot, the default setting can be changed by 
passing `i915.enable_hangcheck=0`​ in your `GRUB_CMDLINE_LINUX_DEFAULT`
setting. You can add the option using instructions provided by your operating 
system provider, or by editing the value of `GRUB_CMDLINE_LINUX_DEFAULT` in 
`/etc/default/grub` to include `i915.enable_hangcheck=0`. 


After editing, the line for GRUB_CMDLINE_LINUX_DEFAULT should look similar
to the following:

```
GRUB_CMDLINE_LINUX_DEFAULT="i915.enable_hangcheck=0"
```
After editing, update the GRUB boot files:
 - Ubuntu: `update-grub`
 - Red Hat Enterprise Linux and SUSE Linux Enterprise Server: `grub2-mkconfig -o /boot/grub2/grub.cfg`

After rebooting, you should now see `i915.enable_hangcheck=0` in `/proc/cmdline`
and the value in `/sys/module/i915/parameters/enable_hangcheck` should
be 0.

#### Multi-Card Deployments

Some systems may have compatibility issues between the system BIOS and the 
Linux kernel MMIO BAR re-allocation, which prevents the Intel® Data Center GPUs
from being accessible once the system has booted. If you are 
experiencing problems with multi-card solutions and the Intel GPU devices 
not initializing (entries for the device are not enumerating in `/dev/dri`), 
you can work around the issue by adding pci=realloc=off​ to your kernel's 
boot parameter.

To check if your system already has `pci=realloc=off`​, you can check for the 
string via `cat /proc/cmdline​`. If it does not, you can add the option 
using instructions provided by your operating system provider, or by
editing the value of `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`
to include `pci=realloc=off`. 

After editing, the line for GRUB\_CMDLINE\_LINUX\_DEFAULT should look similar
to the following:

```
GRUB_CMDLINE_LINUX_DEFAULT="pci=realloc=off"
```

After editing, update the GRUB boot files:
 - Ubuntu: `update-grub`
 - Red Hat Enterprise Linux and SUSE Linux Enterprise Server: `grub2-mkconfig -o /boot/grub2/grub.cfg`

After rebooting, you should now see `pci=realloc=off` in /proc/cmdline.

### Host System Support

Packages provided on this site have been validated with the following
platform configurations:

| Host system | GPU     |
| :-------- | :------- |
| 12th Generation Intel® Core™ Processors <br> (Codename Alder Lake-H, Alder Lake-P, Alder Lake-U, Alder Lake-S, Alder Lake-HX)| Intel® Arc™ A-Series Graphics (Codename Alchemist) |
| 11th Generation Intel® Core Processors <br> (Codename Tiger Lake)|Intel® Arc™ A-Series Graphics (Codename Alchemist) |
| 3rd Gen Intel® Xeon Scalable Ice Lake <br> (M50CYP Family)| Intel® Data Center GPU Flex Series |
