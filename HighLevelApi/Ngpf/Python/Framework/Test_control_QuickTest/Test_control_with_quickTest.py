################################################################################
# Version 1.0    $Revision: 1 $
# $Author: rcsutak
#
#    Copyright ? 1997 - 2008 by IXIA
#    All Rights Reserved.
#
#    Revision Log:
#    05-14-2014 Ruxandra Csutak
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
# This script is based on the following scenario:							   #
#         - load an ixncfg containing a QuickTest                              #
#         - retrieve and change the input parameters of the QT                 #
#         - start the QT, retrieve statistics, stop the QT                     # 
#                                                                              # 
# Module:                                                                      #
#    The sample was tested on a 1GE LSM XMVDC16NG module.                      #
#                                                                              #
################################################################################

from pprint import pprint
import os, sys
import time
from itertools import izip
import pdb
# Append paths to python APIs

# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python') 
# sys.path.append('/path/to/ixnetwork/api/python')


from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError


ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

try:
	ErrorHandler('', {})
except (NameError,):
	def ErrorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)


dirname, filename = os.path.split(os.path.abspath(__file__))
config_file = os.path.join(dirname, 'sample_test_control_with_quickTest.ixncfg')

chassis_ip = "ixro-hlt-xm2-09"
tcl_server = "ixro-hlt-xm2-09"
ixnetwork_tcl_server = 'localhost'
port_list = ['2/1','2/2']
errors = 0


print "Printing connection variables ... "
print "test_name = %s" % filename
print 'chassis_ip =  %s' % chassis_ip
print "tcl_server = %s " % tcl_server
print "ixnetwork_tcl_server = %s" % ixnetwork_tcl_server
print "port_list = %s " % port_list
print "config_file = %s" % config_file


#===============================> CONNECTION <==========================================
print "Connecting to localhost ..."
connect_result = ixiangpf.connect(
    ixnetwork_tcl_server = ixnetwork_tcl_server,
    tcl_server = tcl_server,
    device = chassis_ip,
    port_list = port_list,
    break_locks = 1,
    config_file = config_file,
)

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)

print "\nPrinting connection result\n"
pprint(connect_result)

ports = connect_result['vport_list'].split()


print "\nRetrieving all QuickTest handles present in the config ...\n"

test_control_status = ixiahlt.test_control(action = 'get_all_qt_handles')
    
if test_control_status['status'] != '1':
    ErrorHandler('test_control', test_control_status)

qt_handle = test_control_status['qt_handle']

print "\nHandle(s) retrieved: %s \n" % qt_handle


#===============================> RETRIEVE INPUT PARAMS <==========================================


print "\nRetrieving the input parameters of the QT(s)\n"

test_control_status = ixiangpf.test_control(
    action = 'qt_get_input_params',
    qt_handle = qt_handle,
)
    
if test_control_status['status'] != '1':
    ErrorHandler('test_control', test_control_status)

print "\nInput parameters retrieved for QT (%s):\n %s\n" % (qt_handle, test_control_status[qt_handle]['input_params'])

param_list =test_control_status[qt_handle]['input_params']
aux=param_list[2:-2]
aux2=aux.replace('} {',' ')
params=aux2.split()
i = iter(params)
modified_params = dict(izip(i,i))

print "\nModifying input parameters ...\n"
lava_trial=2
lava_init_load=15
lava_iterations=02         

modified_params['lava_trial']=lava_trial
modified_params['lava_init_load'] = lava_init_load
modified_params['lava_iterations']=lava_iterations


print "\nModified params = %s\n" % modified_params
#===============================> APPLY CONFIG - SYNC <==========================================

test_control_status = ixiangpf.test_control(
    action    = 'qt_apply_config',
    qt_handle = qt_handle,
)
    
if test_control_status['status'] != '1':
    ErrorHandler('test_control', test_control_status)

#===============================> START TEST - SYNC <==========================================

print "\nStarting QT with modified parameters ... \n"
test_control_status = ixiangpf.test_control(
    action            =    'qt_start',
    qt_handle         =     qt_handle,
)
#input_params      =     modified_params,
if test_control_status['status'] != '1':
    ErrorHandler('test_control', test_control_status)


#===============================> RETRIEVE STATS <==========================================


time.sleep(20)

print "\nRetrieving currently running QuickTest ... \n"
test_stats_status=ixiangpf.test_stats(
    mode = 'qt_currently_running',
)

if test_stats_status['status'] != '1':
    ErrorHandler('test_stats', test_stats_status)


new_qt_handle=test_stats_status['qt_handle']

print "\nGetting the status of the currently running QuickTest ...\n"
test_stats_status=ixiangpf.test_stats(
    mode = 'qt_running_status',
    qt_handle = new_qt_handle,
)

if test_stats_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_stats', test_stats_status)

running_qt=test_stats_status[new_qt_handle]['is_running']


while running_qt:

    qt_progress = ixiangpf.test_stats(
        mode = 'qt_progress',
        qt_handle = new_qt_handle,
    )
    
    if qt_progress['status'] != IxiaHlt.SUCCESS:
        ErrorHandler('test_stats', qt_progress)
     
    if qt_progress[new_qt_handle]['progress'] == '':
        break
    
    print " qt_progress : %s " % qt_progress
    
    time.sleep(10)
    
    test_stats_status=ixiangpf.test_stats(
        mode = 'qt_running_status',
        qt_handle = new_qt_handle,
    )
            
    if test_stats_status['status'] != IxiaHlt.SUCCESS:
        ErrorHandler('test_stats', test_stats_status)

    running_qt=test_stats_status[new_qt_handle]['is_running']

print "\nGetting and printing the run result of the QuickTest ...\n"
qt_result=ixiangpf.test_stats(
    mode = 'qt_result',
    qt_handle = new_qt_handle,
)
    
if qt_result['status'] != IxiaHlt.SUCCESS :
    ErrorHandler('test_stats', qt_result)

print "\nQT Result: %s\n" % qt_result[new_qt_handle]['result']

pprint(qt_result)

time.sleep(10)

print "\nRetrieving flow view stats ...\n"
test_stats_status = ixiangpf.test_stats(
    mode = 'qt_flow_view',
    qt_handle = new_qt_handle,
)

if test_stats_status['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_stats', test_stats_status)


pprint(test_stats_status)
flow_keys = test_stats_status.keys()
aux1=flow_keys[0]

if test_stats_status[aux1]['rx_frames'] != test_stats_status[aux1]['tx_frames'] or test_stats_status[aux1]['loss_percentage'] > '0.03':
    errors +=1
    print "FAIL - %s - rx and tx frame no doesn't match / loss_percentage is bigger than 0" % filename

    
print "\nSUCCESS!\n"
