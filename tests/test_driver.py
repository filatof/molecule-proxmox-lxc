"""Tests for ProxmoxLXC driver."""

import pytest
from molecule_proxmox_lxc.driver import ProxmoxLXC


class TestProxmoxLXC:
    """Test ProxmoxLXC driver class."""

    def test_driver_name(self):
        """Test driver name property."""
        driver = ProxmoxLXC()
        assert driver.name == "molecule-proxmox-lxc"

    def test_driver_name_setter(self):
        """Test driver name setter."""
        driver = ProxmoxLXC()
        driver.name = "custom-name"
        assert driver.name == "custom-name"

    def test_login_cmd_template(self):
        """Test login command template."""
        driver = ProxmoxLXC()
        template = driver.login_cmd_template
        assert "ssh" in template
        assert "{address}" in template
        assert "{user}" in template
        assert "{port}" in template
        assert "{identity_file}" in template

    def test_default_ssh_connection_options(self):
        """Test default SSH connection options."""
        driver = ProxmoxLXC()
        options = driver.default_ssh_connection_options
        assert isinstance(options, list)
        assert "UserKnownHostsFile=/dev/null" in " ".join(options)
        assert "StrictHostKeyChecking=no" in " ".join(options)
        assert "IdentitiesOnly=yes" in " ".join(options)

    def test_required_collections(self):
        """Test required Ansible collections."""
        driver = ProxmoxLXC()
        collections = driver.required_collections
        assert "community.proxmox" in collections
        assert "ansible.posix" in collections

    def test_sanity_checks(self):
        """Test sanity checks don't raise exceptions."""
        driver = ProxmoxLXC()
        # Should not raise any exception
        driver.sanity_checks()


class TestProxmoxLXCIntegration:
    """Integration tests for ProxmoxLXC driver."""

    @pytest.fixture
    def mock_config(self, mocker):
        """Create mock config."""
        config = mocker.MagicMock()
        config.driver.get_instance_config.return_value = []
        return config

    def test_ansible_connection_options_no_config(self, mock_config):
        """Test ansible connection options when no config exists."""
        driver = ProxmoxLXC(config=mock_config)
        options = driver.ansible_connection_options("test-instance")
        assert options == {}

    def test_template_dir(self):
        """Test template directory path."""
        driver = ProxmoxLXC()
        template_dir = driver.template_dir()
        assert "playbooks" in template_dir
