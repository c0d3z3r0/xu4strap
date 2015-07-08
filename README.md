# rockstrap for Radxa Rock

## What is it?
rockstrap is a script for installing Debian GNU/Linux Jessie 8.0 armhf to a sd card for Radxa Rock.

## Why?
Why not? :-) I *hate* downloading big sd card images and dd'ing them onto my sd cards resulting in an overblown Debian installation with software I am never going to use. You'll simply get a basic Debian installation like from the netinstaller with some more basic packages (see below).

## What you will need and how to I use it
There is some software you have to install before using my installer:

* python3
* python3-colorama
* sed
* psmisc
* fdisk
* curl
* dosfstools
* cdebootstrap
* qemu-user-static.

If there is no package python3-colorama you can also install it with `pip3 install colorama` after installing `python3-pip` via aptitude / apt-get.

*You'll be warned if something is missing.*

## Usage
Just look at the help: ./rockstrap.py -h

## Packages already included
- debian standard packages
- keyboard-configuration, console-data, console-setup
- ntp, tzdata, locales, openssh-server, ca-certificates, openssl
- cpufrequtils, cpufreqd
- vim, aptitude, apt-transport-https, psmisc

## I want wheezy instead of jessie
Open the script with vim and type `:%s/jessie/wheezy`. Then close vim with `:wq`. That's it.

## Warnings

The installer enables SSH root login and password authentication so you can easily ssh to your new Debian installation. For security reasons you shouldn't use that in a production environment. Switch to pubkey authentication instead.

There have been error reports that this script doesn't work on Ubuntu so you need to use a Debian host.

## Am I allowed to modify and share it?
Yes, of course but please keep the author name where it is :-)

## Problems?
Open an issue on GitHub, please.

## Questions?
Contact me on IRC via c0d3z3r0 @ freenode.net

# License

Copyright (C) 2015 Michael Niewöhner

This is open source software, licensed under GPLv2. See the file LICENSE for details.
