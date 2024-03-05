################################################################################


################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF BFDv6 API              #
#    It will create 2 BFDv6 topologyes, it will start the emulation and        #
#    than it will retrieve and display few statistics                          #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    IxOS      8.00 EA                                                         #
#    IxNetwork 8.00 EA                                                         #
#                                                                              #
################################################################################
if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports        = [('10.200.113.7', '8', '7'), ('10.200.113.7', '8', '8')]
    py.ixTclServer  =  "10.200.225.53"
    py.ixRestPort    =  '11020'
    py.ixTclPort     =  8020
# END HARNESS VARS ************************************************************

################################################################################
# Import the IxNet library
################################################################################
import sys,time,copy,pprint,os,ast
from restAPIV import *
import restAPI as rest

################################################################################
# Connect to IxNet client
################################################################################

ixNet = IxNet(py.ixTclServer, int(py.ixTclPort)+3000)
ixNet.connect()
root = ixNet.getRoot()

################################################################################
# Cleaning up IxNetwork
################################################################################

print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')

print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()

root    = ixNet.getRoot()
vportTx = ixNet.getList(root, 'vport')[0]
vportRx = ixNet.getList(root, 'vport')[1]

print("adding topologies")
print "Add topologies"
ixNet.add(root, 'topology')
ixNet.add(root, 'topology')
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]

print "Add ports to topologies"
ixNet.setAttribute(topo1, '-vports', [vportTx])
ixNet.setAttribute(topo2, '-vports', [vportRx])
ixNet.commit()




print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '18:03:73:C7:6C:B1',
    '-step',      '00:00:00:00:00:01')

ixNet.setAttribute(ixNet.getAttribute(mac2, '-mac') + '/singleValue',
    '-value', '18:03:73:C7:6C:01')
ixNet.commit()


print("Add ipv4")
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ip1 = ixNet.getList(mac1, 'ipv4')[0]
ip2 = ixNet.getList(mac2, 'ipv4')[0]

mvAdd1 = ixNet.getAttribute(ip1, '-address')
mvAdd2 = ixNet.getAttribute(ip2, '-address')
mvGw1  = ixNet.getAttribute(ip1, '-gatewayIp')
mvGw2  = ixNet.getAttribute(ip2, '-gatewayIp')

print("configuring ipv4 addresses")
ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '20.20.20.2')
ixNet.setAttribute(mvAdd2 + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '20.20.20.1')
ixNet.setAttribute(mvGw2  + '/singleValue', '-value', '20.20.20.2')

ixNet.setAttribute(ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
ixNet.setAttribute(ixNet.getAttribute(ip2, '-prefix') + '/singleValue', '-value', '24')

ixNet.setMultiAttribute(ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ip2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()


###########################################################################
#Add and Configure BFDv4 Interface 
###########################################################################
print("Adding BFDv4 and Configuring")
ixNet.add(ip1, 'bfdv4Interface')
ixNet.add(ip2, 'bfdv4Interface')
ixNet.commit()

bfdv41 = ixNet.getList(ip1, 'bfdv4Interface')[0]
bfdv42 = ixNet.getList(ip2, 'bfdv4Interface')[0]

txInterval1 = ixNet.getAttribute(bfdv41, '-txInterval')
txInterval2 = ixNet.getAttribute(bfdv42, '-txInterval')
minRxInterval1 = ixNet.getAttribute(bfdv41, '-minRxInterval')
minRxInterval2 = ixNet.getAttribute(bfdv42, '-minRxInterval')

ixNet.setAttribute(txInterval1 + '/singleValue', '-value', '2000')
ixNet.setAttribute(txInterval2 + '/singleValue', '-value', '2000')
ixNet.setAttribute(minRxInterval1 + '/singleValue', '-value', '2000')
ixNet.setAttribute(minRxInterval2 + '/singleValue', '-value', '2000')
ixNet.commit()


############################################################################
#Add and Configure OSPFv2
############################################################################
print("Adding OSPF and Configuring")
ixNet.add(ip1, 'ospfv2')
ixNet.add(ip2, 'ospfv2')
ixNet.commit()

ospfv21 = ixNet.getList(ip1, 'ospfv2')[0]
ospfv22 = ixNet.getList(ip2, 'ospfv2')[0]

enableBFD1 = ixNet.getAttribute(ospfv21, '-enableBfdRegistration')
enableBFD2 = ixNet.getAttribute(ospfv22, '-enableBfdRegistration')
networkType1 = ixNet.getAttribute(ospfv21, '-networkType')
networkType2 = ixNet.getAttribute(ospfv22, '-networkType')

ixNet.setAttribute(enableBFD1 +'/singleValue', '-value', 'true')
ixNet.setAttribute(enableBFD2 +'/singleValue', '-value', 'true')
ixNet.setAttribute(networkType1 +'/singleValue', '-value', 'pointtopoint')
ixNet.setAttribute(networkType2 +'/singleValue', '-value', 'pointtopoint')
ixNet.commit()

################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts=ixNet.execute('assignPorts',py.ports,[],vports,True )
time.sleep(10)

################################################################################
# Start BFD protocol and wait for 45 seconds                                   #
################################################################################
print("Starting protocols and waiting for 45 seconds for protocols to come up")
ixNet.execute('startAllProtocols')
time.sleep(45)

################################################################################
# Retrieve protocol statistics                                              #
################################################################################
print ("Fetching all Protocol Summary Stats\n")
viewName  = 'Protocols Summary'
views = ixNet.getList(ixNet.getRoot()+'/statistics', 'view')
for view in views:
    if viewName == ixNet.getAttribute(view,"caption"):
        viewObj = view
        break
viewPage=viewObj+'/page'			
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    print '**************1',statValList
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for

############################################################################
##On The Fly Section
############################################################################
print("Deactivating and Activating BFDv4 Interface On the fly")
activation = ixNet.getAttribute(bfdv41, '-active')

ixNet.setAttribute(activation +'/singleValue', '-value', 'false')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")

time.sleep(10)
ixNet.setAttribute(activation +'/singleValue', '-value', 'true')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
try :
    ixNet.execute('applyOnTheFly', topology)
except :
    print("error in applying on the fly change")
# end try/expect
time.sleep(10)

###############################################################################
# Retrieve protocol learned info                                              # 
###############################################################################
print("Fetching BFD learned info")
data ={'arg1':['/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/bfdv4Interface/1'],'arg2':['1']}
rest.ixNetExec(bfdv41,"getLearnedInfo",data)
time.sleep(5)
linfo  = ixNet.getList(bfdv41, 'learnedInfo')[0]
values = ixNet.getAttribute(linfo, '-values')

print("***************************************************")
for v in values :
    print(v)
# end for
print("***************************************************")

################################################################################
# Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
