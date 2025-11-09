"""Molecule Proxmox LXC Driver.

Based on molecule-proxmox by Michael Meffie.
Adapted for LXC containers support.
"""

__version__ = "0.0.1"
__author__ = "Ivan Filatof"
__credits__ = ["Michael Meffie"]

from .driver import ProxmoxLXC

__all__ = ["ProxmoxLXC"]