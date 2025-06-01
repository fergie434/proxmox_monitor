# Proxmox Monitor

Proxmox monitoring script which uses the proxmox ve API to check all lxc containers and qemu VM's are running.

Only VM's/containers with 'Start at boot' set to 'enabled' will be started, all others will be ignored.

## Usage

### Initial Setup

Create a new .env file, then open it in nano and populate with values for 'proxmox_server', 'username' and 'password'
```bash
cp .env.example .env
nano .env
```

### Install dependencies
```bash
pip3 install -r requirements.txt
```
### Run the script manually

```bash
cd /path/to/script/proxmox_monitor
python3 main.py
```

### Or set up a cron job to execute every 10 minutes

```
*/10 * * * * python3 /path/to/script/proxmox_monitor/main.py
```