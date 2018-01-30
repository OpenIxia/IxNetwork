#!/usr/local/python2.7.6/bin/python2.7

import sys

# Ixia Python modules
from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

ixNetworkTclServer = '10.219.117.103'
tclServer = '10.219.117.101'
chassisIp = '10.219.117.101'
userName = 'hgee'
portList = '1/5 1/6'

def ConnectAndResumeReassignPortsNgpfHlPy(ixNetworkTclServer, tclServer,
                             userName, portList, chassisIp
                             ):
    '''
    Connect to an existing configuration.
    portList format: 1/3. Not 1/1/3.
    This will return all session configuration handles.
    '''

    connectStatus = ixia_ngpf.connect ( 
        ixnetwork_tcl_server = ixNetworkTclServer,
        tcl_server = tclServer,
        username = userName,
        port_list = portList,
        device = chassisIp,
        session_resume_keys = '1',
        break_locks = '1',
        ) 
    if connectStatus['status'] != '1':
        return 1
    else:
        return connectStatus


def PrintDict(obj, nested_level=0, output=sys.stdout):
    """
    Print each dict key with indentions for readability.
    """

    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)

        print >> output, '%s' % (nested_level * spacing)

    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                PrintDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)

    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


connectStatus = ConnectAndResumeReassignPortsNgpfHlPy(ixNetworkTclServer, tclServer,
                                         userName, portList, chassisIp)


PrintDict(connectStatus)
