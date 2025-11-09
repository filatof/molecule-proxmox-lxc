"""Molecule Proxmox LXC Driver Module.

Based on molecule-proxmox by Michael Meffie.
Adapted for LXC containers support.
"""

import os
import yaml
from molecule import logger
from molecule.api import Driver

LOG = logger.get_logger(__name__)


class ProxmoxLXC(Driver):
    """Proxmox LXC Driver Class.

    This driver manages LXC containers on Proxmox VE for Molecule testing.
    It is based on the original molecule-proxmox driver but adapted for
    LXC containers instead of virtual machines.

    The driver uses the community.proxmox.proxmox Ansible module to interact
    with the Proxmox API.
    """

    def __init__(self, config=None):
        """Initialize Proxmox LXC driver."""
        super(ProxmoxLXC, self).__init__(config)
        self._name = "molecule-proxmox-lxc"

    @property
    def name(self):
        """Return driver name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set driver name."""
        self._name = value

    @property
    def login_cmd_template(self):
        """Return login command template."""
        return (
            "ssh {address} "
            "-l {user} "
            "-p {port} "
            "-i {identity_file} "
            "-o UserKnownHostsFile=/dev/null "
            "-o StrictHostKeyChecking=no "
            "-o IdentitiesOnly=yes"
        )

    @property
    def default_ssh_connection_options(self):
        """Return default SSH connection options."""
        return [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
            "-o IdentitiesOnly=yes",
        ]

    @property
    def default_safe_files(self):
        """Return default safe files."""
        return [self.instance_config]

    def login_options(self, instance_name):
        """Return login options for instance."""
        d = {"instance": instance_name}

        return dict(
            self._get_instance_config(instance_name),
            **d,
        )

    def ansible_connection_options(self, instance_name):
        """Return Ansible connection options for instance."""
        try:
            d = self._get_instance_config(instance_name)

            return {
                "ansible_user": d["user"],
                "ansible_host": d["address"],
                "ansible_port": d["port"],
                "ansible_ssh_private_key_file": d["identity_file"],
                "ansible_connection": "ssh",
                "ansible_ssh_common_args": " ".join(
                    self.default_ssh_connection_options
                ),
            }
        except StopIteration:
            return {}
        except IOError:
            # Instance has yet to be provisioned, therefore the
            # instance config file does not yet exist.
            return {}

    def _get_instance_config(self, instance_name):
        """Get instance configuration."""
        instance_config_dict = self._get_instance_config_dict()
        return next(
            item for item in instance_config_dict if item["instance"] == instance_name
        )

    def _get_instance_config_dict(self):
        """Get instance configuration dictionary."""
        instance_config_dict = []

        if os.path.exists(self.instance_config):
            try:
                with open(self.instance_config, "r", encoding="utf-8") as f:
                    instance_config_dict = yaml.safe_load(f) or []
            except Exception as e:
                LOG.warning(f"Failed to load instance config: {e}")
                instance_config_dict = []

        return instance_config_dict

    def sanity_checks(self):
        """Perform sanity checks."""
        # Note: Template validation moved to playbooks for better error handling
        pass  # pylint: disable=unnecessary-pass

    def template_dir(self):
        """Return template directory."""
        return os.path.join(
            os.path.dirname(__file__),
            "playbooks",
        )

    @property
    def required_collections(self):
        """Return required Ansible collections."""
        return {
            "community.proxmox": "1.0.0",
            "ansible.posix": "1.0.0",
        }
