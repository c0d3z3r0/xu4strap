#!/usr/bin/env python3

# xu4strap
# Copyright (C) 2016  Michael Niewöhner <foss@mniewoehner.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


__author__ = 'Michael Niewöhner <c0d3z3r0>'
__email__ = 'mniewoeh@stud.hs-offenburg.de'

import argparse
import sys
import os
import random


# TODO: move argparse to armdebootstrap
def parseargs():
    parser = argparse.ArgumentParser(description='XU4strap')
    parser.add_argument('sdcard', nargs=1,
                        help='SD card to install debian on e.g. /dev/sdc')
    parser.add_argument('--debug', "-d", action="store_true",
                        help='Enable debug output')
    parser.add_argument('--boot-size', "-b", type=int, default=100,
                        help='Boot partition size in MB')
    parser.add_argument('--packages', "-p",
                        help='Comma separated list of additional packages')
    return parser.parse_args()


def main():

    args = parseargs()
    name = 'xu4strap'
    hostname = 'odroidxu4'
    rootdevice = 'mmcblk1'
    partitions = [
        {'start': '4096', 'end': '+%sM' % str(args.boot_size), 'type': 'e',
         'fs': 'msdos', 'mount': '/boot'},
        {'start': str(4096+args.boot_size*2048), 'end': '',
         'type': '83', 'fs': 'ext4', 'mount': '/'}
    ]
    packages = ['curl']
    if args.packages:
        packages += args.packages.split(',')

    # Download latest armdebootstrap
    if not os.path.isfile("armdebootstrap.py"):
        os.system('curl -so armdebootstrap.py --connect-timeout 5 '
                  'https://raw.githubusercontent.com/c0d3z3r0/armdebootstrap/'
                  'master/armdebootstrap.py')

    # Initialize ArmDebootstrap and start the installation process
    from armdebootstrap import ArmDeboostrap
    adb = ArmDeboostrap(name, hostname, args.sdcard[0], partitions,
                        packages, rootdevice, debug=args.debug)
    adb.init()
    adb.install()

    # ################### Odroid-XU4 specific stuff ####################

    # Generate random locally administered mac address
    mac = ':'.join(map(lambda x: "%02X" % x,
                       [random.randint(0x00, 0xFF) & 0xFC | 0x02] +
                       [random.randint(0x00, 0xFF) for _ in range(0, 5)]))

    adb.writeFile('/etc/network/interfaces.d/eth0',
                  '  hwaddress ether %s' % mac,
                  append=True)

    # Install xu4-update
    adb.lprint("Install xu4-update.")
    adb.run('curl -Lso %s/usr/bin/xu4-update '
            'https://raw.githubusercontent.com/c0d3z3r0/xu4-update/master/'
            'xu4-update' % adb.tmp)
    adb.run('chmod +x %s/usr/bin/xu4-update' % adb.tmp)

    # Install kernel and modules
    adb.lprint("Install kernel, modules and bootloader.")
    if not os.path.isdir("%s/lib/modules" % adb.tmp):
        os.mkdir("%s/lib/modules" % adb.tmp, 755)
    adb.run("mount --rbind /dev %s/dev" % adb.tmp)
    adb.run("SKIP_WARNING=1 SD_DEV=%s chroot %s /usr/bin/xu4-update" %
            (adb.sdcard, adb.tmp))
    adb.run("umount -R %s/dev" % adb.tmp)

    # ################# end Odroid-XU4 specific stuff ##################

    adb.cleanup()
    sys.exit(0)


if __name__ == '__main__':
    main()
