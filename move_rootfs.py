import re
import os

def permissions_to_mode(permissions):
    # Define the permission-to-mode mapping
    permission_map = {
        'r': 4,
        'w': 2,
        'x': 1,
        '-': 0
    }
    # Iterate over the permissions string in sets of three (owner, group, others)
    type = permissions[0]
    owner_mode = str(sum(permission_map[char] for char in permissions[1:4]))
    group_mode = str(sum(permission_map[char] for char in permissions[4:7]))
    others_mode = str(sum(permission_map[char] for char in permissions[7:10]))
    mode = owner_mode+group_mode+others_mode
    return type,mode

"""
# Input file:
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/arpd/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/chrony/
drwxr-xr-x 999/999           0 2018-03-09 14:34 ./var/lib/dbus/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/misc/
drwxr-xr-x 28/28             0 2018-03-09 14:34 ./var/lib/postgresql/
-rw-r--r-- 28/28            90 2018-03-09 14:34 ./var/lib/postgresql/.profile

"""
def parse_file_for_mode_uid_gid(line, source_dir_parent):
    cmd = None
    line = re.sub(r'[ \t]+', ' ', line)
    pattern = r"([a-zA-Z\-]+) (\d+)\/(\d+) \d+ \d{4}\-\d{2}\-\d{2} \d{2}:\d{2} (.+)"
    # Search for the pattern
    print(line.strip())  # Use strip() to remove leading/trailing whitespace
    match = re.search(pattern, line)
    if match:
        # Extracted information
        file_permissions = match.group(1)
        type, mode = permissions_to_mode(file_permissions)
        print(f"Type:{type}")
        uid = match.group(2)
        gid = match.group(3)
        file_name = match.group(4)
        # Output results
        print(f"Mode: {mode}")
        print(f"UID: {uid}")
        print(f"GID: {gid}")
        print(f"File Name: {file_name}")
        if type=='d':
            # This is a directory
            dst_file_name = re.sub("^./", "/", file_name)
            cmd = f"e2mkdir -v -P {mode} -O {uid} -G {gid} ./img.ext4:{dst_file_name}\n"
        else:
            # This is a file
            src_file_name = re.sub("^"+source_dir_parent, ".", file_name)
            dst_file_name = re.sub("^./", "/", file_name)
            cmd = f"e2cp -v -P {mode} -O {uid} -G {gid} {src_file_name} -d ./img.ext4:{dst_file_name}\n"
    else:
        print("No match found.")
    return cmd




# Example usage
permissions = "drwxr-xr-x"
mode = permissions_to_mode(permissions)
print(f"Mode: {mode}")

"""
Create a list of files

tar --strip-components=2 -tvf ./rootfs.tar.gz ./var/lib | tee rootfs_files.txt
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/arpd/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/chrony/
drwxr-xr-x 999/999           0 2018-03-09 14:34 ./var/lib/dbus/
drwxr-xr-x 0/0               0 2018-03-09 14:34 ./var/lib/misc/
drwxr-xr-x 28/28             0 2018-03-09 14:34 ./var/lib/postgresql/
-rw-r--r-- 28/28            90 2018-03-09 14:34 ./var/lib/postgresql/.profile

Extract files:
tar --strip-components=2 -xzvf ./rootfs.tar.gz ./var/lib


"""

# Open the text file and parse it line by line
source_dir="./var/lib"
# Get the last directory by using os.path.basename



# Get the directory part before the last component
source_dir_parent = os.path.dirname(source_dir)


print("Parent directory:", source_dir_parent)  # Output: ./var


script_file_path = 'e2cp_to_ext4.sh'
rootfs_file_path = 'rootfs_files.txt'  # Replace with your file path
list_of_lines = ["#!/bin/sh\n",
                "rm -rf ./img.ext4\n",
                "dd if=/dev/zero of=./img.ext4 bs=1M count=100\n",
                "mkfs.ext4 ./img.ext4\n"
                ]

with open(rootfs_file_path, 'r') as file:
    for line in file:
        # Process each line here
        cmd = parse_file_for_mode_uid_gid(line, source_dir_parent)
        if cmd:
            list_of_lines.append(cmd)
with open(script_file_path, 'w') as file:
    file.writelines(list_of_lines)


