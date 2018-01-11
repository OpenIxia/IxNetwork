#!/usr/local/python2.7.6/bin/python2.7
import sys, os
import time, re

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixia_tcl = IxiaTcl()
ixia_hlt = IxiaHlt(ixia_tcl)
ixia_ngpf = IxiaNgpf(ixia_hlt)
ixNet = ixia_ngpf.ixnet ;# For low level Python API commands

#import IxN_Api

chassis_ip = '10.219.117.101'
ixnetwork_tcl_server = '10.219.117.103'
tcl_server = chassis_ip
user_name = 'hgee'
#port_list = '1/1 1/2'
#port_1 = '1/1/1'
#port_2 = '1/1/2'

def GetStatsNgpfHlPy(type_of_stats='flow'):
    print '\nGetStatsNgpfHlPy:', type_of_stats
    status = ixia_ngpf.traffic_stats(mode = type_of_stats)    
    if status['status'] != '1':
        print '\nGetStatsNgpfHlPy failed: ', status['log']
        sys.exit()

    PrintDict(status)
    return status


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

def StartTrafficNgpfHlPy():
    print '\nStartTrafficNgpfHlPy'
    status = ixia_ngpf.traffic_control(action = 'run')    
    if status == 1:
        print '\nStartTrafficNgpfHlPy failed: ', status['log']
        return 1

    return status


# To Resume
connect_result = ixia_ngpf.connect ( 
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    username = user_name,
    break_locks = '1'
    ) 

PrintDict(connect_result)

StartTrafficNgpfHlPy()

stats = GetStatsNgpfHlPy('aggregate')

PrintDict(stats)

