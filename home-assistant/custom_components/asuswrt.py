"""
Support for ASUSWRT routers.
"""
import logging
import re
import socket
import threading
from collections import namedtuple
from datetime import timedelta

import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pexpect==4.0.1']
DOMAIN = 'asuswrt'
ASUSWRT = None

CONF_PROTOCOL = 'protocol'
CONF_MODE = 'mode'
CONF_SSH_KEY = 'ssh_key'
CONF_PUB_KEY = 'pub_key'
SECRET_GROUP = 'Password or SSH Key'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PROTOCOL, default='ssh'):
            vol.In(['ssh', 'telnet']),
        vol.Optional(CONF_MODE, default='router'):
            vol.In(['router', 'ap']),
        vol.Exclusive(CONF_PASSWORD, SECRET_GROUP): cv.string,
        vol.Exclusive(CONF_SSH_KEY, SECRET_GROUP): cv.isfile,
        vol.Exclusive(CONF_PUB_KEY, SECRET_GROUP): cv.isfile
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up ASUS WRT device"""
    global ASUSWRT

    conf = config[DOMAIN]
    ASUSWRT = AsusWrt(conf)

    return ASUSWRT.success_init

class AsusWrt(object):
    """This class queries a router running ASUSWRT firmware."""

    # pylint: disable=too-many-instance-attributes, too-many-branches
    # Eighth attribute needed for mode (AP mode vs router mode)

    def __init__(self, config):
        """Initialize the scanner."""
        self.host = config[CONF_HOST]
        self.username = config[CONF_USERNAME]
        self.password = config.get(CONF_PASSWORD, '')
        self.ssh_key = config.get('ssh_key', config.get('pub_key', ''))
        self.protocol = config[CONF_PROTOCOL]
        self.connection = None

        if self.protocol == 'ssh':
            if self.ssh_key:
                self.ssh_secret = {'ssh_key': self.ssh_key}
            elif self.password:
                self.ssh_secret = {'password': self.password}
            else:
                _LOGGER.error('No password or private key specified')
                self.success_init = False
                return
        else:
            if not self.password:
                _LOGGER.error('No password specified')
                self.success_init = False
                return

        self.lock = threading.Lock()

        # Test the router is accessible.
        self.success_init = self.get_connection() is not None

    def get_connection(self):
        """Retrieve data from ASUSWRT and return parsed result."""
        if not self.connection:
            if self.protocol == 'ssh':
                connection = AsusWrtSshConnection(self.host, self.username, self.ssh_secret)
            elif self.protocol == 'telnet':
                connection = AsusWrtTelnetConnection(self.host, self.username, self.password)
            else:
                # autodetect protocol
                connection = AsusWrtSshConnection(self.host, self.username, self.ssh_secret)
                if connection and connection.success_init:
                    self.protocol = 'ssh'
                else:
                    connection = AsusWrtTelnetConnection(self.host, self.username, self.password)
                    if connection and connection.success_init:
                        self.protocol = 'telnet'
            self.connection = connection
        return self.connection

    def send_command(self, command):
        if not self.success_init:
            return None

        return self.connection.send_command(command)


class AsusWrtConnection(object):
    def __init__(self):
        # Test the router is accessible.
        self.success_init = self.__get_connection(self) is not None

    def __get_connection(self):
        return None

    def send_command(self, command):
        raise NotImplementedError()



class AsusWrtSshConnection(AsusWrtConnection):
    """This class communicates with the ASUS router via the ssh protocol."""

    def __init__(self, host, username, ssh_secret):
        """Initialize the connection"""
        self.host = host
        self.username = username
        self.ssh_secret = ssh_secret

        super().__init__()

    def __get_connection(self):
        """Create the connection"""
        from pexpect import pxssh, exceptions

        ssh = pxssh.pxssh()
        try:
            ssh.login(self.host, self.username, **self.ssh_secret)
        except exceptions.EOF as err:
            _LOGGER.error('Connection refused. Is SSH enabled?')
            return None
        except pxssh.ExceptionPxssh as err:
            _LOGGER.error('Unable to connect via SSH: %s', str(err))
            return None
        return ssh

    def send_command(self, command):
        """Execute a command on the router and return the output"""
        try:
            ssh = __get_connection()
            ssh.sendline(command)
            ssh.prompt()
            response = ssh.before
            ssh.logout()
            response = b'\n'.join(response.split(b'\n')[1:-1])
            return response.decode('utf-8')
        except pxssh.ExceptionPxssh as exc:
            _LOGGER.error('Unexpected response from router: %s', exc)
            return None

class AsusWrtTelnetConnection(object):
    """This class communicates with the ASUS router via the telnet protocol."""

    def __init__(self, host, username, password):
        """Initialize the connection"""
        self.host = host
        self.username = username
        self.password = password

        super().__init__()


    def __get_connection(self):
        """Create the connection"""
        import telnetlib

        try:
            telnet = telnetlib.Telnet(self.host)
            telnet.read_until(b'login: ')
            telnet.write((self.username + '\n').encode('ascii'))
            telnet.read_until(b'Password: ')
            telnet.write((self.password + '\n').encode('ascii'))
            self.prompt_string = telnet.read_until(b'#').split(b'\n')[-1]
            return telnet
        except EOFError:
            _LOGGER.error('Unexpected response from router')
            return None
        except ConnectionRefusedError:
            _LOGGER.error('Connection refused by router, is telnet enabled?')
            return None
        except socket.gaierror as exc:
            _LOGGER.error('Socket exception: %s', exc)
            return None
        except OSError as exc:
            _LOGGER.error('OSError: %s', exc)
            return None

    def send_command(self, command):
        """Execute a command on the router and return the output"""
        try:
            telnet = self.__get_connection()
            telnet.write('{}\n'.format(command).encode('ascii'))
            response = telnet.read_until(self.prompt_string)
            telnet.write('exit\n'.encode('ascii'))
            response = b'\n'.join(response.split(b'\r\n')[1:-1])
            return response.decode('utf-8')
        except EOFError:
            _LOGGER.error('Unexpected response from router')
            return None
        except socket.gaierror as exc:
            _LOGGER.error('Socket exception: %s', exc)
            return None
