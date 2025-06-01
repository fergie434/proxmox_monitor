#!/usr/bin/env python3

from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()
proxmox_server = os.getenv('proxmox_server')
realm = os.getenv('realm')
username = f"{os.getenv('username')}@{os.getenv('realm')}"
password = os.getenv('password')
proxmox = ProxmoxAPI(proxmox_server, user=username, password=password, verify_ssl=False)
log_filename = 'logs/proxmox_monitor.log'
log_maxbytes = 4000000
log_filecount = 5

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
    )
    rotating_handler = RotatingFileHandler(filename=log_filename, maxBytes=log_maxbytes, backupCount=log_filecount)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)

    return logger

def main(logger):
    for node in proxmox.nodes.get():
        node_obj = proxmox.nodes(node['node'])
        lxc_list = node_obj.lxc.get()

        # Check all lxc containers are running
        for lxc in lxc_list:
            lxc_config = node_obj.lxc(lxc['vmid']).config.get()
            if lxc_config['onboot'] == 1and lxc['status'] == 'stopped':
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
    logger = setup_logging()
    logger.info('Script Starting')
    main(logger)
    logger.info('Script Completed')
