# coding=utf-8
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################
################################################################################
# Description:                                                                 
#    This script intends to demonstrate how to use IEEE 802.1x API
#    It will do the  following :
#1.    Add topology and devicegroup 
#2.    Configure ethernet and dot1x Layer.
#3.    Change protocol type to PEAPV0
#4.    Change few global parameters
#5.    Start of Device group
#6.    Check for session info and stats
#7.    Stop of Device group
################################################################################

import os
import sys
import time

def assignPorts (ixNet, realPort1) :
    chassis1 = realPort1[0]
    card1 = realPort1[1]
    port1 = realPort1[2]
    root = ixNet.getRoot()
    vport1 = ixNet.add(root, 'vport')
    ixNet.commit()
    vport1 = ixNet.remapIds(vport1)[0]
    chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
    ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
    ixNet.commit()
    chassisObj1 = ixNet.remapIds(chassisObj1)[0]

    cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1, port1)
    ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
                                 '-rxMode', 'captureAndMeasure', '-name', 
                                 'Ethernet - 001')
    ixNet.commit()
# end def assignPorts

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.50-EA\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information  #
# below                                                                        #
################################################################################
ixTclServer = '10.39.65.1'
ixTclPort   = '8009'
ports       = [('10.39.65.187', '1', '4',)]


ixNet = IxNetwork.IxNet()
print("connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

print("cleaning up the old configfile, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0])
time.sleep(5)
root    = ixNet.getRoot()
vport1 = ixNet.getList(root, 'vport')[0]

##################### Creating topology and Device group ####################

print("Creating topology")
ixNet.add(root, 'topology', '-vports', vport1)
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]

print "Adding 1 device group"
ixNet.add(topo1, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
dot1x_dg = t1devices[0]
ixNet.setMultiAttribute(dot1x_dg,'-name','Dot1x DG')
ixNet.commit()

print("Changing the multiplier to 1")
ixNet.setAttribute(dot1x_dg, '-multiplier', '1')

############################# Creating Dot1x layer ##########################
print "Creating Dot1x layer"
ethernet = ixNet.add(dot1x_dg, 'ethernet')
ixNet.commit()
ixNet.setMultiAttribute(ethernet,'-name','Ethernet')
ixNet.commit()

dot1x = ixNet.add(ethernet, 'dotOneX')
ixNet.commit()
ixNet.setMultiAttribute(dot1x,'-name','Dot1x')
ixNet.commit()

################### Change protocol type to PEAPV0##########################
print "Change protocol type to PEAPV0"
dot1x_protocol = ixNet.getAttribute(dot1x, '-protocol')
ixNet.setAttribute(dot1x_protocol, '-pattern', 'singleValue')
ixNet.commit()
dot1x_protocol_single_val = ixNet.getList(dot1x_protocol, 'singleValue')[0]
ixNet.setAttribute(dot1x_protocol_single_val, '-value', 'eappeapv0')
ixNet.commit()

#################### Change few global parameters #########################
print ("Change few global parameters")
glob = ixNet.getList(root, 'globals')[0]
glob_topo = ixNet.getList(glob, 'topology')[0]
dot1x_glob = ixNet.getList(glob_topo, 'dotOneX')[0]

####### Enable Don't logoff global parameter ####
print ("Enable Don't logoff global parameter")
disable_logoff = ixNet.getAttribute(dot1x_glob, '-disableLogoff')
ixNet.setAttribute(disable_logoff, '-pattern', 'singleValue')
ixNet.commit()
disable_logoff_single_val = ixNet.getList(disable_logoff, 'singleValue')[0]
ixNet.setAttribute(disable_logoff_single_val, '-value', 'true')
ixNet.commit()

############### Change the DUT Test mode #######
print ("Change the DUT Test mode")
dut_mode = ixNet.getAttribute(dot1x_glob, '-dutTestMode')
ixNet.setAttribute(dut_mode, '-pattern', 'singleValue')
ixNet.commit()
dut_mode_single_val = ixNet.getList(dut_mode, 'singleValue')[0]
ixNet.setAttribute(dut_mode_single_val, '-value', 'singlehost')
ixNet.commit()

############# Change Wait before Run value ######
print ("Change Wait before Run value")
wait_before_run = ixNet.getAttribute(dot1x_glob, '-waitBeforeRun')
ixNet.setAttribute(wait_before_run, '-pattern', 'singleValue')
ixNet.commit()
wait_before_run_single_val = ixNet.getList(wait_before_run, 'singleValue')[0]
ixNet.setAttribute(wait_before_run_single_val, '-value', 10)
ixNet.commit()

############# Change EAPOL version ######
print ("Change EAPOL Version")
eapol_version = ixNet.getAttribute(dot1x, '-eapolVersion')
ixNet.setAttribute(eapol_version, '-pattern', 'singleValue')
ixNet.commit()
eapol_version_single_val = ixNet.getList(eapol_version, 'singleValue')[0]
ixNet.setAttribute(eapol_version_single_val, '-value', 'eapolver2020')
ixNet.commit()

############# Enable Ignore Authenticator EAPOL Version ######
print ("Enable Ignore Authenticator EAPOL Version")
ignore_auth_eapol_ver = ixNet.getAttribute(dot1x, '-ignoreAuthEapolVer')
ixNet.setAttribute(ignore_auth_eapol_ver, '-pattern', 'singleValue')
ixNet.commit()
ignore_auth_eapol_ver_single_val = ixNet.getList(ignore_auth_eapol_ver, 'singleValue')[0]
ixNet.setAttribute(ignore_auth_eapol_ver_single_val, '-value', 'true')
ixNet.commit()

######### Start Dot1x DG, Fetch Session info  and Display Statistics ######
print (" Start Dot1x DG, Fetch Session info  and Display Statistics")
ixNet.execute("start", dot1x_dg)
time.sleep(30)

print (" Fetch Session info")
sessionInfo = ixNet.getAttribute(dot1x, '-sessionInfo')
print ("sessionInfo", sessionInfo)

print ("Fetching  Protocol Summary Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
print("***************************************************")

print ("Fetching 802.1x  Protocol per port stats Stats\n")
viewPage = '::ixNet::OBJ-/statistics/view:"IEEE 802.1X Per Port"/page'
statcap = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues'):
    for statVal in statValList:
        print("***************************************************")
        index = 0
        for satIndv in statVal:
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
print("***************************************************")

######################## Stop Dot1x DG ####################################
print ("Stop Dot1x DG")
ixNet.execute("stop", dot1x_dg)
time.sleep(30)

print "For more info please refer to the user manual or the built-in help"
print  "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1"
print  "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/dotOneX:1"

print  "*****************END************************"