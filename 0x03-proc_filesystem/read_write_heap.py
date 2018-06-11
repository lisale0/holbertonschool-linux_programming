#! /usr/bin/env python
import re
import sys

def print_memory_of_pid(pid, only_writable=True):

    maps_file = open("/proc/{}/maps".format(sys.argv[1]), 'r')
    mem_file = open("/proc/{}/mem".format(sys.argv[1]), 'rb+', 0)
    memory_permissions = 'rw' if only_writable else 'r-'

    """ for each mapped region"""
    for line in maps_file.readlines():
        spl = line.split(" ")
        addr = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])', line)
        if addr.group(3) == memory_permissions and "heap" in line:
            """ Change to Base-16 """
            start_addr = int(addr.group(1), 16)
            end_addr = int(addr.group(2), 16)

            print("Start: {}, End: {}".format(start_addr,end_addr))

            """ Jump to the start position of the offset """
            mem_file.seek(start_addr)
            """ The chunk to look at"""
            chunk = mem_file.read(end_addr - start_addr)

            """ Find the string in the chunk """
            find = chunk.find("Holberton".encode())
                    
            print(chunk)
            print("-------->>>{}".format(line))
            print("-------->>> start address: {}, end address: {}".format(start_addr, end_addr))
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
