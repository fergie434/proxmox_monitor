#!/usr/bin/env python3

from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os

load_dotenv()
proxmox_server = os.getenv('proxmox_server')
realm = os.getenv('realm')
username = f"{os.getenv('username')}@{os.getenv('realm')}"
password = os.getenv('password')
proxmox = ProxmoxAPI(proxmox_server, user=username, password=password, verify_ssl=False)

def main():
    nodes = proxmox.nodes.get()
    for node in nodes:
        node_obj = proxmox.nodes(node['node'])
        lxc_list = node_obj.lxc.get()
        for lxc in lxc_list:
            lxc_config = node_obj.lxc(lxc['vmid']).config.get()
            ...


    ...

if __name__ == '__main__':
    main()