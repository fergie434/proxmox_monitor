#!/usr/bin/env python3

from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os
import log_helper

load_dotenv()
proxmox_server = os.getenv('proxmox_server')
realm = os.getenv('realm')
username = f"{os.getenv('username')}@{os.getenv('realm')}"
password = os.getenv('password')
proxmox = ProxmoxAPI(proxmox_server, user=username, password=password, verify_ssl=False)

def main(logger):
    for node in proxmox.nodes.get():
        node_obj = proxmox.nodes(node['node'])
        lxc_list = node_obj.lxc.get()

        # Don't run at first boot
        if node['uptime'] < 700:
            return

        # Check all lxc containers are running
        for lxc in lxc_list:
            lxc_config = node_obj.lxc(lxc['vmid']).config.get()
            if 'onboot' not in lxc_config.keys():
                continue
            if lxc_config['onboot'] == 1 and lxc['status'] == 'stopped':
                node_obj.lxc(lxc['vmid']).status.start.post()
                logger.info(f"Started {lxc['name']}")

        # Check all qemu VM's are running
        for vm in node_obj.qemu.get():
            vm_config = node_obj.qemu(vm['vmid']).config.get()
            if not 'onboot' in vm_config.keys():
                vm_config['onboot'] = 0
            if vm_config['onboot'] == 1 and vm['status'] == 'stopped':
                node_obj.qemu(vm['vmid']).status.start.post()
                logger.info(f"Started {vm['name']}")


if __name__ == '__main__':
    logger = log_helper.setup_logging(log_filename='proxmox_monitor.log')
    logger.info('Script Starting')
    main(logger)
    logger.info('Script Completed')
