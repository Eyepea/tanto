# -*- coding: utf-8 -*-
'''
WS Shinken handling
'''
from __future__ import absolute_import

import logging
import csv
import os
import time
import requests

from monitoring_agent import configurator

LOG = logging.getLogger(__name__)

class WsShinkenException(RuntimeError):
    """Generic exception when a problem occurs."""

class CacheFileException(WsShinkenException):
    """When a cache file has a problem, this exception is raised."""
    def __init__(self, cache_file):
        super(CacheFileException, self).__init__()
        self.cache_file = cache_file

    def __str__(self):
        return "The cache file '%s' has a problem." % str(self.cache_file)

class CacheDialect(csv.Dialect):
    delimiter = '|'
    quotechar = '"'
#     escapechar = None
#    doublequote = None
    lineterminator = "\n"
    quoting = csv.QUOTE_MINIMAL
#    skipinitialspace = False

CACHE_DIALECT_FIELDS = ['time_stamp',
                        'host_name',
                        'service_description',
                        'return_code',
                        'output']

class WsShinken(object):
    '''
    classdocs
    '''


    def __init__(self, config_file):
        '''
        Constructor
        '''
        self.http_headers = {'content-type': 'application/json', 'accept': 'application/json'}
        # Setup servers dict
        self.servers = configurator.read(config_file,
                                         configspec='outputs/configspecs/ws_shinken.cfg',
                                         server_mode=True)
        for server in self.servers:
            if self.servers[server]['cache'] == True:
                try:
                    cache_file = os.path.join(self.servers[server]['cache_working_directory'],
                                              '%s.csv' % (server, ))
                    self.servers[server]['file'] = open(cache_file, 'r+')
                except IOError:
                    raise CacheFileException(cache_file)

                cache_file = csv.DictReader(self.servers[server]['file'],
                                            dialect=CacheDialect,
                                            fieldnames=CACHE_DIALECT_FIELDS)

                self.servers[server]['csv'] = csv.DictWriter(self.servers[server]['file'],
                                                             dialect=CacheDialect,
                                                             fieldnames=CACHE_DIALECT_FIELDS)

                for cache_item in cache_file:
                    self.send_result(cache_item['return_code'],
                                     cache_item['output'],
                                     cache_item['service_description'],
                                     cache_item['time_stamp'],
                                     [server])



    def send_result(self, return_code, output, service_description='', time_stamp=0, specific_servers=None):
        '''
        Send result to the Skinken WS
        '''
        if time_stamp == 0:
            time_stamp = int(time.time())

        if specific_servers == None:
            specific_servers = self.servers
        else:
            specific_servers = set(self.servers).intersection(specific_servers)

        for server in specific_servers:
            post_data = {}
            post_data['time_stamp'] = time_stamp
            post_data['host_name'] = self.servers[server]['custom_fqdn']
            post_data['service_description'] = service_description
            post_data['return_code'] = return_code
            post_data['output'] = output

            if self.servers[server]['availability']:
                url = '%s://%s:%s%s' % (self.servers[server]['protocol'],
                                         self.servers[server]['host'],
                                         self.servers[server]['port'],
                                         self.servers[server]['uri'])

                auth = (self.servers[server]['username'],
                        self.servers[server]['password'])

                try:
                    response = requests.post(url,
                                             auth=auth,
                                             headers=self.http_headers,
                                             verify=self.servers[server]['verify'],
                                             timeout=self.servers[server]['timeout'],
                                             data=post_data)
                    if response.status_code == 400:
                        LOG.error("[ws_shinken][%s]: HTTP status: %s - The content of the WebService call is incorrect",
                                      server,
                                      response.status_code)
                    elif response.status_code == 401:
                        LOG.error("[ws_shinken][%s]: HTTP status: %s - You must provide an username and password",
                                      server,
                                      response.status_code)
                    elif response.status_code == 403:
                        LOG.error("[ws_shinken][%s]: HTTP status: %s - The username or password is wrong",
                                      server,
                                      response.status_code)
                    elif response.status_code != 200:
                        LOG.error("[ws_shinken][%s]: HTTP status: %s", server, response.status_code)
                except (requests.ConnectionError, requests.Timeout), error:
                    self.servers[server]['availability'] = False
                    LOG.error(error)
            else:
                LOG.error("[ws_shinken][%s]: Data not sent, server is unavailable", server)

            if self.servers[server]['availability'] == False and self.servers[server]['cache'] == True:
                self.servers[server]['csv'].writerow(post_data)
                LOG.info("[ws_shinken][%s]: Data cached", server)


    def close_cache(self):
        '''
        Close cache of WS Shinken
        '''
        # Close all WS_Shinken cache files
        for server in self.servers:
            if self.servers[server]['cache'] == True:
                self.servers[server]['file'].close()