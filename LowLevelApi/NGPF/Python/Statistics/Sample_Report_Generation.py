################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mario Dicu $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
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
#    This sample configures 10 IPv4 sessions on each of the two ports,         # 
#    adds a traffic Item that uses IPv4 endpoints, sends traffic and           #
#    generate a pdf report                                                     #
#                                                                              #
################################################################################

if 'py' not in dir():
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports = [('10.205.15.62', 3, 5), ('10.205.15.62', 3, 6)]
    py.ixTclServer = '10.205.15.224'
    py.ixTclPort = 8009

################################################################################
# Import the IxNet library
################################################################################
from IxNetwork import IxNet
import time, os
ixNet = IxNet()

################################################################################
# Connect to IxNet client
################################################################################

ixNet.connect(py.ixTclServer, '-port', py.ixTclPort, '-version', '7.40')

################################################################################
# Cleaning up IxNetwork
################################################################################
print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')

################################################################################
# Adding ports to configuration
################################################################################
print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()
vPorts = ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]

################################################################################
# Configure IPv4 endpoints
################################################################################
print "Add topologies"
ixNet.add(root, 'topology')
ixNet.add(root, 'topology')
ixNet.commit()

topo1 = ixNet.getList(root, 'topology')[0]
topo2 = ixNet.getList(root, 'topology')[1]

print "Add ports to topologies"
ixNet.setAttribute(topo1, '-vports', vport1)
ixNet.setAttribute(topo2, '-vports', vport2)
ixNet.commit()

print "Add device groups to topologies"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

dg1 = ixNet.getList(topo1, 'deviceGroup')[0]
dg2 = ixNet.getList(topo2, 'deviceGroup')[0]

print "Add Ethernet stacks to device groups"
ixNet.add(dg1, 'ethernet')
ixNet.add(dg2, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(dg1, 'ethernet')[0]
mac2 = ixNet.getList(dg2, 'ethernet')[0]

print "Add ipv4 stacks to Ethernets"
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ipv4_1 = ixNet.getList(mac1, 'ipv4')[0]
ipv4_2 = ixNet.getList(mac2, 'ipv4')[0]

print "Setting multi values for ipv4 addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-address') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-gatewayIp') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-address') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-gatewayIp') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

################################################################################
# Create Traffic for IPv4
################################################################################
print ''
print "Creating Traffic for IPv4"

ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.commit()
ti1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[0]
ixNet.setMultiAttribute( ti1,
        '-name'                 ,'Traffic IPv4',
        '-trafficType'          ,'ipv4',
        '-allowSelfDestined'    ,False,
        '-trafficItemType'      ,'l2L3',
        '-mergeDestinations'    ,True,
        '-egressEnabled'        ,False,
        '-srcDestMesh'          ,'manyToMany',
        '-enabled'              ,True,
        '-routeMesh'            ,'fullMesh',
        '-transmitMode'         ,'interleaved',
        '-biDirectional'        ,True,
        '-hostsPerNetwork'      ,1)
ixNet.commit()
ixNet.setAttribute(ti1, '-trafficType', 'ipv4')
ixNet.commit()
ixNet.add(ti1, 'endpointSet',
        '-sources',             ipv4_1,
        '-destinations',        ipv4_2,
        '-name',                'ep-set1',
        '-sourceFilter',        '',
        '-destinationFilter',   '')
ixNet.commit()
ixNet.setMultiAttribute(ti1 + "/configElement:1/frameSize",
        '-type',        'fixed',
        '-fixedSize',   128)
ixNet.setMultiAttribute(ti1 + "/configElement:1/frameRate",
        '-type',        'percentLineRate',
        '-rate',        10)
ixNet.setMultiAttribute(ti1 + "/configElement:1/transmissionControl",
        '-duration'               ,1,
        '-iterationCount'         ,1,
        '-startDelayUnits'        ,'bytes',
        '-minGapBytes'            ,12,
        '-frameCount'             ,10000,
        '-type'                   ,'fixedFrameCount',
        '-interBurstGapUnits'     ,'nanoseconds',
        '-interBurstGap'          , 0,
        '-enableInterBurstGap'    ,False,
        '-interStreamGap'         ,0,
        '-repeatBurst'            ,1,
        '-enableInterStreamGap'   ,False,
        '-startDelay'             ,0,
        '-burstPacketCount'       ,1,)
ixNet.setMultiAttribute(ti1 + "/tracking", '-trackBy', ['ipv4SourceIp0'])
ixNet.commit()

################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts = ixNet.execute('assignPorts', py.ports, [], ixNet.getList("/","vport"), True)
if assignPorts != vports:
    raise TestFailedError("FAILED assigning ports. Got %s" %assignPorts)
else:
    print("PASSED assigning ports. Got %s" %assignPorts)

################################################################################
# Start All Protocols
################################################################################
print "Starting All Protocols"
ixNet.execute('startAllProtocols')
print "Sleep 30sec for protocols to start"
time.sleep(30)

################################################################################
# Generate, apply, start traffic
################################################################################
ixNet.execute('generate', ti1)
ixNet.execute('apply', '/traffic')
ixNet.execute('start', '/traffic')
print "Sleep 30sec to send all traffic"
time.sleep(30)

print "#########################"
print "## Reporter Samples ##"
print "#########################"
print ""

################################################################################
# Define the Generate PDF report using the Master Template function
################################################################################
def generateReport(ixNet, reportName="MasterTemplate", templateName=None, outputPath=r"c:\\Regression\\reporter", outputFormat="pdf", saveResults="saveDetailedResults"):
    print ('- generate report')
    if templateName:
        defaultTemplateDir = r"C:\Program Files (x86)\Ixia\IxReporter-IxN\data\Templates"
        templateFile = os.path.join(defaultTemplateDir,templateName)
        ixNet.setAttribute('/reporter/generate', '-templatePath', templateFile)
    ixNet.setMultiAttribute('/reporter/generate',
                '-outputFormat', outputFormat,
                '-outputPath', os.path.join(outputPath, reportName + "." + outputFormat))
    ixNet.commit()

    ixNet.execute(saveResults, '/reporter/saveResults')
    timeOut=360
    stTime = time.time()
    while ixNet.getAttribute('/reporter/saveResults', '-state') != "done":
        time.sleep(10)
        if (time.time()-stTime)>timeOut:
            raise Exception('Report save Result is taking more than specified timeout time (%d secs.)' % (timeOut))
        print '\t -- saving detailed results, wait 10 more seconds'

    timeOut=360
    ixNet.execute('generateReport', '/reporter/generate')
    stTime = time.time()
    print "- start Report Generate"
    while ixNet.getAttribute('/reporter/generate', '-state') == "inProgress":
        time.sleep(10)
        if (time.time()-stTime)>timeOut:
            break
        print "\t -- generating report, wait 10 more seconds"

    repGenState = ixNet.getAttribute('/reporter/generate', '-state')
    if repGenState=="inProgress":
        raise Exception("Detailed report generation did not complete within %d seconds" %(timeOut,))
    elif repGenState == "done":
        print "- report generation complete"
    elif repGenState == "failed":
        raise Exception("Detailed report generation failed")

################################################################################
# Generate the pdf report
################################################################################
print "Generate Master Template pdf report"
generateReport(ixNet)
