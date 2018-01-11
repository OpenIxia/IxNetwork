#################################################################################
# Version 1    $Revision: 1 $
# $Author: RCsutak $
#
#    Copyright © 1997 - 2014 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    08-18-2014 RCsutak - created sample
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#   This sample connects to an IxNetwork client and loads an ixncfg containing #
#   traffic items. Using the retrieved information, it sets the global traffic #
#   option called "Frame Ordering" to the new option "Peak Loading".           #
# Module:                                                                      #
#   The sample was tested on a LSM XMVDC16NG module.                           #
#                                                                              #
################################################################################


from pprint import pprint
import os, sys
import time
import pdb


# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python')
# sys.path.append('/path/to/ixnetwork/api/python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError


ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

dirname, filename = os.path.split(os.path.abspath(__file__))
print dirname
print filename
logname = dirname + '\\log.log'
ixiahlt.ixiatcl.set_py('::ixia::debug', 3)
ixiahlt.ixiatcl.set_py('::ixia::debug_file_name', logname)


chassis_ip = "ixro-hlt-xm2-01"
tcl_server = "ixro-hlt-xm2-01"
ixnetwork_tcl_server = 'localhost'
port_list_str = "1/1 1/2 1/3 1/4"
port_list = port_list_str.split()
cfgErrors = 0
config_file = os.path.join(dirname, 'peak_loading_ipv4_vlan_traffic.ixncfg')



print "Printing connection variables ... "
print "test_name = %s" % filename
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list
print "config_file = %s" % config_file



###################################
##  CONNECT WITH SESSION RESUME  ##
###################################


print " Connecting to localhost ..."
connect_result = ixiangpf.connect(
		port_list	         	=  port_list,
		device				 	=  chassis_ip,
		ixnetwork_tcl_server 	=  ixnetwork_tcl_server,
		tcl_server				=  tcl_server,
        config_file             =  config_file,
        break_locks             =  1,
)

if connect_result['status'] != '1':
    print "FAIL:"
    print connect_result['log']
    quit()

print " Printing connection result"
pprint(connect_result)

ixNet = ixiangpf.ixnet

root = ixNet.getRoot()

aux = connect_result['traffic_config'].split('{')
aux2 = aux[1].split('}')
ti_name=aux2[0]

ti = connect_result[ti_name]['traffic_config']['traffic_item']

print "Starting protocols ...\n"

start = ixiangpf.test_control( action = 'start_all_protocols')
if start['status'] != '1':
    print "FAIL:"
    print start['log']
    quit()
time.sleep(5)

traffic = ixiangpf.traffic_config(
    mode                            = 'modify',
    global_dest_mac_retry_count     = '3',
    global_dest_mac_retry_delay     = '3',
    global_enable_dest_mac_retry    = '1',
    global_enable_mac_change_on_fly = '1',
    global_frame_ordering           = 'peak_loading',
    stream_id                       = ti,
    )

if traffic['status'] != '1':
    print "FAIL:"
    print traffic['log']
    quit()


ordering_mode = ixNet.getAttribute('/traffic','-frameOrderingMode')

print "Set ordering mode is : %s" % ordering_mode