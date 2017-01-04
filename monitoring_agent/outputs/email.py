# -*- coding: utf-8 -*-
'''
Email handling
'''
from __future__ import absolute_import

import logging
import smtplib
from email.mime.text import MIMEText

from monitoring_agent import configurator
from monitoring_agent.inputs.nagios_plugins import STATUSES

LOG = logging.getLogger(__name__)

class Email(object):
    '''
    Send emails
    '''


    def __init__(self, config_file):
        '''
        Read the config file
        '''
        # Setup servers dict from config file
        self.servers = configurator.read(config_file,
                                         configspec='outputs/configspecs/email.cfg',
                                         server_mode=True,
                                         list_values=True)
        for server in self.servers:
            self.servers[server]['results'] = []


    def aggregate_result(self, return_code, output, service_description='', specific_servers=None):
        '''
        aggregate result
        '''
        if specific_servers == None:
            specific_servers = self.servers
        else:
            specific_servers = set(self.servers).intersection(specific_servers)

        for server in specific_servers:
            if not self.servers[server]['send_errors_only'] or return_code > 0:
                self.servers[server]['results'].append({'return_code': return_code,
                           'output': output,
                           'service_description': service_description,
                           'return_status': STATUSES[return_code][0],
                           'custom_fqdn': self.servers[server]['custom_fqdn']})
                LOG.info("[email][%s][%s]: Aggregate result: %r", service_description, server, self.servers[server]['results'][-1])

    def send_results(self):
        '''
        send results
        '''

        for server in self.servers:
            if self.servers[server]['results']:
                if len(self.servers[server]['results']) == 1:
                    msg = MIMEText('')
                    msg['Subject'] = '[%(custom_fqdn)s] [%(service_description)s] %(return_status)s: %(output)s' % self.servers[server]['results'][0]
                else:
                    txt = ''
                    summary = [0, 0, 0, 0]
                    for results in self.servers[server]['results']:
                        txt += '[%(service_description)s] %(return_status)s: %(output)s\n' % results
                        summary[results['return_code']] += 1
                    msg = MIMEText(txt)
                    subject = '[%(custom_fqdn)s]' % self.servers[server]['results'][0]
                    for i, status in enumerate(STATUSES):
                        subject += ' %s:%s' % (status[0], summary[i])
                    msg['Subject'] = subject

                msg['From'] = self.servers[server]['from']
                msg['To'] = ', '.join(self.servers[server]['to'])
                if self.servers[server]['tls']:
                    smtp_server = smtplib.SMTP_SSL(self.servers[server]['host'], self.servers[server]['port'])
                else:
                    smtp_server = smtplib.SMTP(self.servers[server]['host'], self.servers[server]['port'])

                if self.servers[server]['login'] and len(self.servers[server]['login']) > 0:
                    smtp_server.login(self.servers[server]['login'], self.servers[server]['password'])
                smtp_server.sendmail(self.servers[server]['from'], self.servers[server]['to'], msg.as_string())
                smtp_server.quit()
                LOG.info("[email][%s]: e-mail sent from: %s to: %s", server, self.servers[server]['from'], self.servers[server]['to'])