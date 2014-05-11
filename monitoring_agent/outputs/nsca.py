# -*- coding: utf-8 -*-
'''
NSCA handling
'''
from __future__ import absolute_import

import logging
import pynsca
import socket

from monitoring_agent import configurator

LOG = logging.getLogger(__name__)

class Nsca(object):
    '''
    Manage NSCA requests
    '''


    def __init__(self, config_file):
        '''
        Read the config file and start NSCA connexions
        '''
        # Setup servers dict from config file
        self.servers = configurator.read(config_file,
                                         configspec='outputs/configspecs/nsca.cfg',
                                         server_mode=True)
        # start NSCA connexions
        for server in self.servers:
            self.servers[server]['notifier'] = pynsca.NSCANotifier(self.servers[server]['host'],
                                                                   monitoring_port=int(self.servers[server]['port']),
                                                                   encryption_mode=int(self.servers[server]['encryption_mode']),
                                                                   password=self.servers[server]['password'])


    def send_result(self, return_code, output, service_description='', specific_servers=None):
        '''
        Send results
        '''
        if specific_servers == None:
            specific_servers = self.servers
        else:
            specific_servers = set(self.servers).intersection(specific_servers)

        for server in specific_servers:
            if self.servers[server]['availability']:
                try:
                    self.servers[server]['notifier'].svc_result(self.servers[server]['custom_fqdn'],
                                                                service_description,
                                                                int(return_code),
                                                                str(output))
                    LOG.info("[nsca][%s][%s]: Data sent", service_description, self.servers[server]['host'])
                except (socket.gaierror, socket.error), error:
                    self.servers[server]['availability'] = False
                    LOG.error("[nsca][%s][%s]: %s", service_description, self.servers[server]['host'], error[1])
            else:
                LOG.error("[nsca][%s][%s]: Data not sent, server is unavailable", service_description, self.servers[server]['host'])