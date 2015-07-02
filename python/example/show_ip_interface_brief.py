#!/usr/bin/env python2.7

# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
Demonstrate how to obtain a brief description of the network interfaces of one network device.

1. Select a configured device from the inventory.
2. Execute the command and print the output.
3. Print the command syntax and output field descriptions.
"""
from __future__ import print_function
from inspect import cleandoc
from logging import log, WARN
from nxapi.http import cli_show, connect, disconnect, print_command_reference, session_device_url
from nxapi.context import sys_exit, EX_OK, EX_TEMPFAIL
from nxapi.render import print_table
from example import inventory_config
from itertools import chain

command = 'sh ip int br'

def demonstrate(session):
    """ Execute a command, print the output, return 'true' if successful. """
    response = cli_show(session, command)
    for c in response:
        print('Output for command:', c)
        output = response[c]
        
        table_intf =output['TABLE_intf']
        rows = [row.values() for row in table_intf]
        rows=list(chain(*rows))
        print_table(rows)
        print()

        table_vrf =output['TABLE_vrf']
        rows = [row.values() for row in table_vrf]
        rows=list(chain(*rows))
        print_table(rows)
        print()
    return True

def main():
    """ Oversee the sequence of tasks as per the documentation of this script. """
    print(cleandoc(__doc__))
    print()
    
    print('Select an appropriate device from those available.')
    print_table(inventory_config)
    print()
    for device_config in inventory_config:
        try:
            http_session = connect(**device_config)
            try:
                print('Connected to', session_device_url(http_session))
                print()
                demonstrate(http_session)
                return EX_OK if print_command_reference(http_session, command) else EX_TEMPFAIL        
            finally:
                disconnect(http_session)
        except IOError:
            log(WARN, 'Unable to connect to Nexus device %s', str(device_config))
            continue
    
    print("There are no suitable network devices. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
        
