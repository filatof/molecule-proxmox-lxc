# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2025-11-09

### Added
- Initial release of molecule-proxmox-lxc driver
- Support for creating LXC containers on Proxmox VE by cloning templates
- Support for destroying LXC containers with proper cleanup
- Full clone support for LXC container templates
- Network configuration with support for:
  - Static IP address assignment
  - Custom gateway configuration
  - Network bridge selection
  - Custom netmask (CIDR notation)
- SSH key configuration via public key injection
- Container features support:
  - nesting (nested virtualization)
  - keyctl (kernel keyring)
  - fuse (FUSE filesystems)
  - custom mount options
- Unprivileged container support (enabled by default)
- Privileged container support (when needed)
- External secrets management:
  - File-based secrets (YAML format)
  - Script-based secrets (executable with stdout output)
- DNS configuration:
  - Custom nameservers
  - Search domains
- Storage selection per platform or globally
- Configurable timeouts for Proxmox API operations
- Wait for container SSH availability after creation
- Proper instance config management for Molecule

### Changed
- Forked from [molecule-proxmox](https://github.com/meffie/molecule-proxmox) by Michael Meffie
- Replaced `community.general.proxmox_kvm` module with `community.proxmox.proxmox`
- Changed target from KVM virtual machines to LXC containers
- Updated network configuration format:
  - Changed from `ipconfig` parameter to `netif` dictionary
  - Simplified IP configuration with separate `ip_address`, `gateway`, `netmask` parameters
- Removed qemu-guest-agent dependency (not needed for LXC)
- Simplified cloud-init handling specific to LXC containers
- Updated driver name from `proxmox` to `proxmox-lxc`
- Changed Python package name from `molecule-proxmox` to `molecule-proxmox-lxc`

### Fixed
- Proper handling of full clones on storage types that don't support linked clones
- Container network configuration now properly updates after cloning
- SSH key injection works correctly with LXC containers
- Container startup sequence ensures proper initialization

### Security
- SSH connections use strict options by default:
  - `UserKnownHostsFile=/dev/null`
  - `StrictHostKeyChecking=no`
  - `IdentitiesOnly=yes`

### Notes
- This is an **alpha release** - use with caution in production environments
- Based on [molecule-proxmox](https://github.com/meffie/molecule-proxmox) version as of January 2025
- Requires `community.proxmox` collection version >= 1.0.0
- Python 3.8+ required
- Ansible Core 2.12+ required
- Molecule 6.0.0+ required

### Migration from molecule-proxmox

If you're migrating from molecule-proxmox (KVM driver), note these changes:

**molecule.yml changes:**
```yaml
# OLD (molecule-proxmox):
driver:
  name: molecule-proxmox
platforms:
  - name: test01
    template_name: debian11
    ipconfig:
      ipconfig0: 'ip=192.168.1.10/24,gw=192.168.1.1'

# NEW (molecule-proxmox-lxc):
driver:
  name: molecule-proxmox-lxc
platforms:
  - name: test01
    template_vmid: 100  # Must use VMID, not name
    ip_address: 192.168.1.10
    gateway: 192.168.1.1
    netmask: 24
```

**Key differences:**
- Use `template_vmid` instead of `template_name`
- Network config is split into separate parameters
- No cloud-init drive required in template
- Containers start much faster than VMs
- Lower resource overhead

### Known Issues
- Storage must support LXC containers (not all Proxmox storage types do)
- Linked clones are not supported (always uses full clones)
- Some advanced cloud-init features are not available with LXC

### Credits
- Original molecule-proxmox driver: [Michael Meffie](https://github.com/meffie)
- LXC adaptation: Ivan Filatof

### License
MIT License - See [LICENSE](LICENSE) file for details

---

## Version History

- **0.0.1** (2025-11-09) - Initial alpha release

## Semantic Versioning Guide

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version (X.0.0) - Incompatible API changes
- **MINOR** version (0.X.0) - New functionality (backwards compatible)
- **PATCH** version (0.0.X) - Bug fixes (backwards compatible)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

[Unreleased]: https://github.com/filatof/molecule-proxmox-lxc/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/filatof/molecule-proxmox-lxc/releases/tag/v0.0.1