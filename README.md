# Molecule Proxmox LXC Driver

Ansible Molecule Driver plugin for managing LXC containers on Proxmox VE.

> **Note:** This is a fork of [molecule-proxmox](https://github.com/meffie/molecule-proxmox) by Michael Meffie, adapted to work with LXC containers instead of virtual machines.

## Features

- Create and destroy LXC containers on Proxmox VE
- Clone from LXC templates with full clone support
- Configure networking, SSH keys, and container settings
- Support for both privileged and unprivileged containers
- Container features support (nesting, keyctl, etc.)

## Requirements

- Access to a [Proxmox VE](https://www.proxmox.com/en/proxmox-ve) cluster
- One or more LXC container templates
- Python package [proxmoxer](https://pypi.org/project/proxmoxer/)
- Ansible collection [community.proxmox](https://docs.ansible.com/ansible/latest/collections/community/proxmox/proxmox_module.html)

The required Python packages are automatically installed when `molecule-proxmox-lxc` is installed with pip.

## Installation

```bash
pip install molecule_proxmox_lxc
```

Or install from source:

```bash
git clone https://github.com/filatof/molecule-proxmox-lxc.git
cd molecule_proxmox_lxc
pip install .
```

## LXC Template Requirements

LXC templates should have:
- SSH server installed and enabled
- Python installed for Ansible
- User account configured (root or dedicated user)
- SSH public key in authorized_keys
- For unprivileged containers: proper ID mapping configured in Proxmox

## Configuration Examples

### Basic Configuration

```yaml
driver:
  name: molecule_proxmox_lxc
  options:
    api_host: pve01.example.com
    api_user: root@pam
    api_password: "********"
    node: pve01
    ssh_user: root
    ssh_identity_file: ~/.ssh/id_rsa
    storage: local

platforms:
  - name: test01
    template_vmid: 100
    newid: 3001
    ip_address: 192.168.1.100
```

### Configuration with API Token

```yaml
driver:
  name: molecule_proxmox_lxc
  options:
    api_host: pve01.example.com
    api_user: root@pam
    api_token_id: "********"
    api_token_secret: "*******************************"
    node: pve01
    ssh_user: root
    ssh_identity_file: ~/.ssh/id_rsa
    storage: local-lvm

platforms:
  - name: container01
    template_vmid: 5510
    newid: 3015
    ip_address: 192.168.1.40
```

### Advanced Configuration

```yaml
driver:
  name: molecule_proxmox_lxc
  options:
    proxmox_secrets: /path/to/proxmox_secrets.yml
    node: pve01
    ssh_user: ansible
    ssh_identity_file: ~/.ssh/id_rsa
    storage: local-lvm
    timeout: 120

platforms:
  - name: container01
    template_vmid: 5510
    newid: 3015
    ip_address: 192.168.1.40
    netmask: 24
    gateway: 192.168.1.1
    bridge: vmbr0
    nameservers:
      - 192.168.1.1
      - 8.8.8.8
    searchdomains:
      - local
      - example.com
    unprivileged: true
    features:
      - nesting=1
      - keyctl=1
```

## Driver Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `api_host` | Proxmox API hostname | Yes* | - |
| `api_user` | Proxmox API user | Yes* | - |
| `api_password` | Proxmox API password | Yes* | - |
| `api_token_id` | Proxmox API token ID | No | - |
| `api_token_secret` | Proxmox API token secret | No | - |
| `api_port` | Proxmox API port | No | 8006 |
| `node` | Proxmox node name | Yes | - |
| `ssh_user` | SSH user for containers | Yes | `root` |
| `ssh_identity_file` | SSH private key path | Yes | - |
| `ssh_port` | SSH port | No | 22 |
| `storage` | Default storage for containers | Yes | - |
| `timeout` | Operation timeout in seconds | No | 30 |
| `proxmox_secrets` | Path to secrets file/script | No | - |

*Required unless using `proxmox_secrets`

## Platform Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `name` | Container hostname | Yes | - |
| `template_vmid` | VMID of LXC template to clone | Yes | - |
| `newid` | VMID for new container | No | Auto-assigned |
| `ip_address` | IP address for container | Yes | - |
| `netmask` | Network mask (CIDR bits) | No | `24` |
| `gateway` | Default gateway | No | `192.168.1.1` |
| `bridge` | Network bridge | No | `vmbr0` |
| `nameservers` | List of DNS servers | No | - |
| `searchdomains` | List of search domains | No | - |
| `unprivileged` | Use unprivileged container | No | `true` |
| `features` | List of container features | No | - |
| `storage` | Storage for this container | No | driver default |

## Using External Secrets

Store Proxmox credentials in an external file:

```yaml
# proxmox_secrets.yml
---
api_host: pve01.example.com
api_user: root@pam
api_password: your-secret-password
```

Reference in molecule.yml:

```yaml
driver:
  name: molecule_proxmox_lxc
  options:
    proxmox_secrets: /path/to/proxmox_secrets.yml
    node: pve01
    ssh_user: root
    ssh_identity_file: ~/.ssh/id_rsa
    storage: local
```

Or use an executable script:

```bash
#!/bin/sh
# proxmox_secrets.sh
pass proxmox/pve01
```

```yaml
driver:
  name: molecule_proxmox_lxc
  options:
    proxmox_secrets: /usr/local/bin/proxmox_secrets.sh
    node: pve01
    # ... other options
```

## Container Features

Common container features you can enable:

```yaml
features:
  - nesting=1      # Enable nested virtualization
  - keyctl=1       # Enable keyctl() syscall
  - fuse=1         # Enable FUSE filesystems
  - mount=nfs      # Allow NFS mounts
```

See [Proxmox LXC documentation](https://pve.proxmox.com/wiki/Linux_Container) for all available features.

## Differences from molecule-proxmox

This driver differs from the original molecule-proxmox:

- Uses `community.proxmox.proxmox` module instead of `community.general.proxmox_kvm`
- Creates LXC containers instead of KVM virtual machines
- Different network configuration format (netif vs ipconfig)
- No qemu-guest-agent dependency
- Always uses full clone (not linked clones)
- Simplified cloud-init handling
- Direct IP address configuration

## Development

Clone the repository:

```bash
git clone https://github.com/filatof/molecule-proxmox-lxc.git
cd molecule_proxmox_lxc
```

Install in development mode:

```bash
pip install -e .
```

Run tests:

```bash
tox -e latest
```

## Troubleshooting

### "Linked clone feature is not available"

This error occurs when trying to create linked clones on storage that doesn't support them. This driver always uses full clones (`clone_type: full`).

### Container doesn't get IP address

Make sure your LXC template has networking properly configured. The driver updates the network configuration after cloning.

### SSH connection fails

- Verify SSH server is running in the template
- Check that the SSH public key is properly configured
- Ensure the firewall allows SSH connections
- Verify the IP address is correct and reachable

## Credits

This project is based on [molecule-proxmox](https://github.com/meffie/molecule-proxmox) by Michael Meffie.

Original KVM driver: Copyright (c) Michael Meffie  
LXC adaptation: Copyright (c) 2025 Ivan Filatof

## License

[MIT License](LICENSE) - See LICENSE file for details