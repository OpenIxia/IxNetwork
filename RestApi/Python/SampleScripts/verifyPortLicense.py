from __future__ import absolute_import, print_function
import sys, os, re, time, subprocess
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, tostringlist
from xml.dom import minidom
import xml.etree.ElementTree as ET
import paramiko

try:
    # Python2.7
    import StringIO
except:
    # Python3
    import io

"""
Description
    Verify port license availability.
    Supports retrieving license check on chassis and Windows.
    
Usage:
    import verifyPortLicense
    licenseObj = verifyPortLicense.Connect(platform='chassis', licenseServerIp=ip, username='admin', password='admin', licenseModel='VM-IXN-TIER3')
    licenseObj = verifyPortLicense.Connect(platform='windows', licenseServerIp=ip, username='user1', password='password', licenseModel='VM-IXN-TIER3')
    availablePortLiceneses = licenseObj.areThereEnoughLicenses(2)

"""

def _xmlprettyprint(stringlist):
    indent = ''
    in_tag = False
    for token in stringlist:
        if token.startswith('</'):
            indent = indent[:-3]
            yield indent + token + '\n'
            in_tag = True
        elif token.startswith('<'):
            yield indent + token
            indent += '   '
            in_tag = True
        elif token == '>':
            yield '>' + '\n'
            in_tag = False
        elif in_tag:
            yield token
        else:
            yield indent + token + '\n'
 
 
def pretty_xml(element):
    return ''.join(_xmlprettyprint(tostringlist(element)))


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    from xml.etree import ElementTree

    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class Connect():
    def __init__(self, platform='chassis', licenseServerIp=None, sshPort=22, username='admin', password='admin', licenseModel='VM-IXN-TIER3'):
        """
        Description
           # For IxVM ports.  Not for physical hardware.

           Class PortLicenses()
           Get available port licenses from the vChassis.
           Only supported on chassis's running LinuxOS.  Not for Windows.

        Parameters
           platform: chassis|windows
           licenseServerIp: The license server IP address.
           username: The chassis login username. Default = admin
           password: The chassis login password. Default = admin
           licenseModel: The license name to look under: For example:
                         VM-IXN-TIER3  VM-IXL-TIER4-10G

        Usage
            import verifyPortLicense
            licenseObj = verifyPortLicense.Connect(platform='chassis', licenseServerIp=ip, username='admin', password='admin', licenseModel='VM-IXN-TIER3')
            licenseObj.areThereEnoughLicenses(2)

        Raises Exception
        """
        self.platform = platform
        self.licenseServerIp = licenseServerIp
        self.username = username
        self.password = password
        self.licenseNameToGet = licenseModel
        self.availablePortLicenses = 0
        self.sshPort = sshPort
        self.sshTimeout = 10
        self.sshPkey = None
        self.sshKeyFilename = None
        if self.platform == 'chassis':
            self.command = 'show licenses --floatingstats'
        if self.platform == 'windows':
            self.command = 'LSPlusCLI.exe -floatingstats -server localhost'

        self.getLicenseDetails()

    def sshConnect(self):
        try:
            print('\nverifyPortLicense.sshConnect:', self.platform, self.licenseServerIp)
            self.ssh.connect(hostname=self.licenseServerIp, port=self.sshPort, username=self.username, password=self.password,
                             pkey=self.sshPkey, key_filename=self.sshKeyFilename, timeout=self.sshTimeout)
        except paramiko.SSHException:
            raise Exception('\nSSH Failed to connect:', self.licenseServerIp)

        print('verifyPortLicense.sshConnect: Connected')

    def send(self, command, displayOutput=True, convertBufferToLines=True):
        bufferBytes=9999
        eof = False
        #convertBufferToLines = False
        expect = '(#|>)'
        timeout = 10
        expectTimeout = 60
        #time.sleep(1)        
        channelData = str()
        sys.stdout.flush()

        noDataFlag = 0
        print('\nSending:', command)
        self.channel.sendall(command+'\n')

        time.sleep(1) ;# Must wait a second to allow time for Linux to respond
        breakWhileFlag = 0

        while True:
            # Keep checking for any output datas to be read up to 
            # timeout seconds.
            #print('ready:', self.channel.recv_ready())
            if self.channel.recv_ready():
               # The shell console may take some time to show the output
                # such as errors and failures. Wait up to 10 seconds.
                for timer in range(0,51):
                    channelData +=  self.channel.recv(bufferBytes).decode('utf-8').strip()
                    if timer < 50 and len(channelData) == 0 and eof == False:
                        time.sleep(.1)
                        continue
                    elif timer < 50 and len(channelData) == 0 and eof == True:
                        if displayOutput:
                            print('\nRECEIVED:', channelData)
                            print('EOF')
                        return 1,''
                    elif timer < 50 and len(channelData) != 0 and eof == False:
                        if displayOutput:
                            print('\nRECEIVED:', channelData)
                        breakWhileFlag = 1
                        break
                    elif timer == 50 and len(channelData) == 0:
                        noDataFlag == 1
                        print('\nRECEIVED no output after sending the command.')
                        breakWhileFlag = 1
                        break
                    else:
                        noDataFlag == 1
                        break

                if noDataFlag == 1:
                    return 0,''

                if breakWhileFlag == 1:
                    break
            else:
                if timeout != 0:
                    time.sleep(.1)
                    timeout -= 1
                    continue
                if timeout == 0:
                    print('\nTIMEOUT. No data ready')
                    return 0, ''

        buffer = ''
        countDownCurrentTime = expectTimeout

        # Wait for expected prompt
        while True:
            if expect == None:
                # Ignore any output. Just return the buffer.
                return 2, channelData

            if displayOutput and channelData != '':
                print('\n--------------- Channel Data Output -----------------')
                print (channelData)
                print('-------------------------------------------------------\n')

            # Note: channelData is the screen output
            #buffer = channelData
            if expect != None:
                # Got the expected prompt and before timeout
                if countDownCurrentTime != 0 and (bool(re.search('.*%s' % expect, channelData))) == True:
                    print('Received the expected prompt')
                    if convertBufferToLines == True:
                        try:
                            # Python2.7
                            buffer = StringIO.StringIO(channelData)
                        except:
                            # Python3
                            buffer = io.StringIO(channelData)
                    else:
                        buffer = channelData

                    return buffer

                if countDownCurrentTime != 0 and (bool(re.search('.*%s' % expect , channelData))) == False:
                    print('Waiting for response and the expected prompt: %d/%d' % (countDownCurrentTime, expectTimeout))
                    countDownCurrentTime -= 1
                    time.sleep(1)
                    self.channel.sendall('\r')
                    channelData = self.channel.recv(bufferBytes).decode('utf-8')
                    continue

                # Did not get the expected prompt and timeout
                if countDownCurrentTime == 0 and (bool(re.search('.*%s' % expect, buffer))) == False:
                    print('\nThe user defined Expected pattern not found. Got:')
                    return 0, channelData

    def getLicenseDetails(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshConnect()
        transport = self.ssh.get_transport()
        transport.set_keepalive(1)
        self.channel = self.ssh.invoke_shell()

        if self.verifyLockFile() == True:
            for counter in range(1,11):
                print('\nareThereEnoughLicenses.verifyLockFile: Somebody is reserving ports. Waiting %d/%d seconds ...' % (counter, 10))
                time.sleep(1)
                
        self.lockFile(True)

        if self.platform == 'chassis':
            output = self.send('launch chassis')
            #output = self.send(self.command)
            stdout = self.send(self.command, convertBufferToLines=True)
            # stdout: <_io.StringIO object at 0x7f4c8ddc9048>
            for line in stdout.readlines():
                if line.strip() == '':
                    continue
                #print(line.strip())
                # version <  8.30: Located license name: VM-IXN-TIER3 | 18-dec-2017 | No | 8 | hgee | Windows2012  | 192.168.70.127 | 2 | No |  |
                # version >= 8.30: VM-IXN-TIER3       | 18-dec-2017      | No         | 10

                match = re.match('^%s.*([0-9]+-[a-zA-Z]+-[0-9]+)(.*?)\|(.*?)\| +([0-9]+)' % self.licenseNameToGet, line, re.I)
                #match = re.match('^%s.*([0-9]+-[a-zA-Z]+-[0-9]+).*\|.*\| +([0-9]+)' % expect, line, re.I)
                if match:
                    self.availablePortLicenses = match.group(4)

        if self.platform == 'windows':
            output = self.send('cd C:\Program Files (x86)', displayOutput=False)
            output = self.send('cd Ixia\LicenseServerPlus', displayOutput=False)
            output = self.send(self.command, displayOutput=False, convertBufferToLines=False)
            match = re.match('%s.*\n(.*)' % self.command, output)
            if match:
                xmlBuffer = match.group(1)
                root = ET.fromstring(xmlBuffer)

                print(prettify(root))
                #['FeatureUsage']['FloatingStats']['Feature']['name']['VM-IXN-TIER3']['available'])

                for child in root.iter():
                    for attrib in child.findall('FloatingStats/Feature'):
                        name = attrib.find('name')
                        available = attrib.find('available')
                        if name.text == 'VM-IXN-TIER3':
                            self.availablePortLicenses = available.text
                            print('%s: Available:%s' % (name.text, available.text))
                            break
                    else:
                        continue
                    break
            else:
                print('\nNo match found')

        self.releaseLockFile()
                    
    def lockFile(self, enabled=True):
        result = subprocess.Popen('touch verifyPortLicense.lock'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = result.communicate()

    def verifyLockFile(self):
        if os.path.isfile('verifyPortLicense.lock') == True:
            return True
        else:
            return False

    def releaseLockFile(self):
        if self.verifyLockFile:
            result = subprocess.Popen('rm verifyPortLicense.lock'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout,stderr = result.communicate()

    def areThereEnoughLicenses(self, required):
        """
        Description
            Verify trhe license server if there are enough port licenses for usage.
            This is only supported for chassis running Linux OS.

        Parameter
            requred: The requred amount of port licenses needed.

        Usage
              portLicenseObj = PortLicenses(platform='windows', licenseServerIp=ip, username='admin', password='admin', licenseModel='VM-IXN-TIER3')
              portLicenseObj = PortLicenses(platform='chassis', licenseServerIp=ip, username='admin', password='admin', licenseModel='VM-IXN-TIER3')
              portLicenseObj.areThereEnoughLicenses(required=2)
        """

        self.requiredNumberOfLicenses = required
        msg = '\nPort license check:'
        msg = msg+'\n\tAvailablePortLicenses: {0}\n\tRequiredLicenses: {1}\n'.format(self.availablePortLicenses, self.requiredNumberOfLicenses)
        if int(self.requiredNumberOfLicenses) <= int(self.availablePortLicenses):
            print(msg)

        else:
            raise Exception('Not enough port licenses:'+msg)
