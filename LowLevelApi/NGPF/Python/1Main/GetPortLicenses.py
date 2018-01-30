# Description
#   Get the available port license remaining count.
#   SSH into the IxVM chassis and enter "show licenses --floatingstats".
#   Get the available port licenses for IxNetwork VE and IxLoad VE.
#
#   Supports Python2 and Python3
#
# Requirements
#     Since there are many type of licenses, you must set the variable 
#     "licenseNameToGet" with a value of your license.
#
# Usage:
#   python GetPortLicenses.py <IxVM Chassis IP> ixnetwork 
#   python GetPortLicenses.py <IxVM Chassis IP> ixload
#
# By: Hubert Gee

from __future__ import absolute_import, print_function
import paramiko
import sys
import re
import traceback
import time

#------ User settings -------
username = 'admin'
password = 'admin'

if sys.argv[2] not in ['ixnetwork', 'ixload']:
    sys.exit('\nNo such platform: %s\nMust be either ixnetwork or ixload\n\n' % sys.argv[1])

# Set the license name
if sys.argv[2] == 'ixnetwork':
    licenseNameToGet = 'VM-IXN-TIER3'

if sys.argv[2] == 'ixload':
    licenseNameToGet = 'VM-IXL-TIER4-10G'

#------ User settings end -------

class PortLicenses():
    def __init__(self, chassisIp, username, password, licenseToGet):
        """
        Description
           Class PortLicenses()
           Get available port licenses from the chassis.
           Only supported on chassis's running LinuxOS.  Not for Windows.
        
        Parameters
           host: The chassis IP address
           username: The chassis login username. Default = admin
           password: The chassis login password. Default = admin
           licenseToGet: The license name to look under: For example: 
                         VM-IxN-TIER3  VM-IXL-TIER4-10G 
        """
        self.chassisIp = chassisIp
        self.username = username
        self.password = password
        self.licenseNameToGet = licenseToGet
        self.command = 'show licenses --floatingstats'
        self.availablePortLicenses = 0
        self.sshPort = 22
        self.sshTimeout = 10
        self.sshPkey = None
        self.sshKeyFilename = None
        self.getLicenseDetails()

    def sshConnect(self):
        try:
            self.ssh.connect(hostname=self.chassisIp, port=self.sshPort, username=self.username, password=self.password,
                             pkey=self.sshPkey, key_filename=self.sshKeyFilename, timeout=self.sshTimeout)
        except paramiko.SSHException:
            raise Exception('\nSSH Failed to connect:', self.chassisIp)

    def send(self, command=None, expect=None):
        print('\nChecking port licenses on:', self.chassisIp)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        for line in stdout.readlines():
            if line.strip() == '':
                continue
            print(line.strip())
            match = re.match('^%s.*([0-9]+-[a-zA-Z]+-[0-9]+)(.*?)\|(.*?)\| +([0-9]+)' % expect, line)
            if match:
                # Located license name: VM-IXN-TIER3 | 18-dec-2017 | No | 8 | hgee | Windows2012  | 192.168.70.127 | 2 | No |  |
                self.availablePortLicenses = match.group(4)
            
    def getLicenseDetails(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshConnect()
        transport = self.ssh.get_transport()
        transport.set_keepalive(1)
        self.channel = self.ssh.invoke_shell()
        self.send(command=self.command, expect=self.licenseNameToGet)
        
    def areThereEnoughLicenses(self, required):
        self.requiredNumberOfLicenses = required
        msg = '\nPort license check:'
        msg = msg+'\n\tAvailablePortLicenses: {0}\n\tRequiredLicenses: {1}\n'.format(self.availablePortLicenses, self.requiredNumberOfLicenses)
        if int(self.requiredNumberOfLicenses) <= int(self.availablePortLicenses):
            print(msg)
        else:
            raise IxNetRestApiException('Not enough port licenses:'+msg)
        
try:
    portLicenseObj = PortLicenses(chassisIp=sys.argv[1],
                                  username=username,
                                  password=password,
                                  licenseToGet=licenseNameToGet)

    portLicenseObj.areThereEnoughLicenses(required=2)

    print('\nAvailable port licenses:', portLicenseObj.availablePortLicenses)

except Exception as errMsg:
    #print(traceback.format_exc())
    print('\nException Error:', errMsg)
