#! /usr/bin/env python
import re
import sys

def print_memory_of_pid(pid, only_writable=True):

    maps_file = open("/proc/{}/maps".format(sys.argv[1]), 'r')
    mem_file = open("/proc/{}/mem".format(sys.argv[1]), 'rb', 0)

    memory_permissions = 'rw' if only_writable else 'r-'
    for line in maps_file.readlines():  # for each mapped region
        spl = line.split(" ")
        addr = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])', line)
        if addr.group(3) == memory_permissions:
            start_addr = int(addr.group(1), 16) #change to hex
            end_addr = int(addr.group(2), 16)
            print("Start: {}, End: {}".format(start_addr,end_addr))
            mem_file.seek(start_addr)
            chunk = mem_file.read(end_addr - start_addr) # read region contents
            find = chunk.find("Holberton".encode())
            
            print("----find: {}".format(find))
            
            print("[*] maps: /proc/{}/maps".format(sys.argv[1]) + "\n"
                  "[*] mem: /proc/{}/mem".format(sys.argv[1]) + "\n"
                  "Found [heap]:" + "\n"
                  "    pathname = [heap]" + "\n"
                  "    addresses = {}".format(spl[0]) + "\n"
                  "    permissions = {}".format(spl[1]) + "\n"
                  "    offset = {}".format(spl[2]) + "\n"
                  "    inode = {}".format(spl[4]) + "\n"
            )

print_memory_of_pid(sys.argv[1], only_writable=True)
