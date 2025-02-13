#!/bin/sh
rm -rf ./img.ext4
dd if=/dev/zero of=./img.ext4 bs=1M count=100
mkfs.ext4 ./img.ext4
e2mkdir -v -P 755 -O 0 -G 0 ./img.ext4:/var/lib/
e2mkdir -v -P 755 -O 0 -G 0 ./img.ext4:/var/lib/arpd/
e2mkdir -v -P 755 -O 0 -G 0 ./img.ext4:/var/lib/chrony/
e2mkdir -v -P 755 -O 999 -G 999 ./img.ext4:/var/lib/dbus/
e2mkdir -v -P 755 -O 0 -G 0 ./img.ext4:/var/lib/misc/
e2mkdir -v -P 755 -O 28 -G 28 ./img.ext4:/var/lib/postgresql/
e2cp -v -P 644 -O 28 -G 28 ./lib/postgresql/.profile -d ./img.ext4:/var/lib/postgresql/.profile
e2mkdir -v -P 700 -O 28 -G 28 ./img.ext4:/var/lib/postgresql/backups/
e2mkdir -v -P 700 -O 28 -G 28 ./img.ext4:/var/lib/postgresql/data/
e2mkdir -v -P 711 -O 0 -G 0 ./img.ext4:/var/lib/sudo/
e2mkdir -v -P 700 -O 0 -G 0 ./img.ext4:/var/lib/sudo/lectured/
e2mkdir -v -P 755 -O 0 -G 0 ./img.ext4:/var/lib/systemd/
