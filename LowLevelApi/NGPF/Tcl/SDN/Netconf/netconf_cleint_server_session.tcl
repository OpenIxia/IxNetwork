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
# Description :                                                                #
#   1. This scripts shows how we should configure Netconf Client & Netconf 	   #
#      Server. Different capoabilities configuration.						   #
#   2. Assign ports.                                                           #
#   3. Start all protocols.                                                    #
#   4. Send Command Snippet of Netconf executing Right Click Action	   		   #
#   5. Retrieve Netconf Client Sessions Per Port statistics.                   #
#   6. Retrieve Netconf Server Per port statistics.                            #
#   7. Stop all protocols.                                                     #
################################################################################
puts "Load ixNetwork Tcl API package"
package req IxTclNetwork
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ports       {{10.39.50.227 1 5} {10.39.50.227 1 6}}
    set ixTclServer 10.39.50.102
    set ixTclPort   8785
}

################################################################################
# Connect to IxNet client
################################################################################
ixNet connect $ixia::ixTclServer -port  $ixia::ixTclPort -version "8.50"

################################################################################
# Cleaning up IxNetwork
################################################################################
puts "Cleaning up IxNetwork..."
ixNet execute newConfig
puts "Get IxNetwork root object"
set root [ixNet getRoot]
################################################################################
# Adding virtual ports
################################################################################
puts "Adding virtual port 1"
set vport1 [ixNet add $root vport]
ixNet commit
set vport1 [lindex [ixNet remapIds $vport1] 0]
ixNet setAttribute $vport1 -name "10GE LAN - 001"
ixNet commit
puts "Adding virtual port 2"
set vport2 [ixNet add $root vport]
ixNet commit
set vport2 [lindex [ixNet remapIds $vport2] 0]
ixNet setAttribute $vport2 -name "10GE LAN - 002"
ixNet commit
################################################################################
# Adding topology
################################################################################
puts "Adding topology 1"
set topology1 [ixNet add $root "topology"]
ixNet commit
set topology1 [lindex [ixNet remapIds $topology1] 0]
ixNet setAttribute $topology1 -name "Topology 1"
ixNet setAttribute $topology1 -vports $vport1
ixNet commit
################################################################################
# Adding device group
################################################################################
puts "Adding device group 1"
set device1 [ixNet add $topology1 "deviceGroup"]
ixNet commit
set device1 [lindex [ixNet remapIds $device1] 0]
ixNet setAttribute $device1 -name "Device Group 1"
ixNet setAttribute $device1 -multiplier "1"
ixNet commit
################################################################################
# Adding ethernet layer
################################################################################
puts "Adding ethernet 1"
set ethernet1 [ixNet add $device1 "ethernet"]
ixNet commit
set ethernet1 [lindex [ixNet remapIds $ethernet1] 0]
set macMv [ixNet getAttribute $ethernet1 -mac]
ixNet add $macMv "counter"
ixNet setMultiAttribute $macMv/counter\
             -direction "increment"\
             -start     "00:11:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
################################################################################
# Adding IPv4 layer
################################################################################
puts "Adding ipv4 1"
set ipv4Addr1  [ixNet add $ethernet1 "ipv4"]
ixNet commit
set ipv4Addr1 [lindex [ixNet remapIds $ipv4Addr1] 0]
set addressMv [ixNet getAttribute $ipv4Addr1 -address]
ixNet add $addressMv "singleValue"
ixNet setMultiAttribute $addressMv/singleValue\
            -value "1.1.1.1"
set gatewayIpMv [ixNet getAttribute $ipv4Addr1 -gatewayIp]
ixNet add $gatewayIpMv "singleValue"
ixNet setMultiAttribute $gatewayIpMv/singleValue\
            -value "1.1.1.2"
################################################################################
# Adding Netconf Server layer
################################################################################
puts "Adding Netconf Server 1"
set netconfServer1 [ixNet add $ipv4Addr1 "netconfServer"]
ixNet commit
set netconfServer1  [lindex [ixNet remapIds $netconfServer1] 0]
ixNet commit
################################################################################
# Adding Netconf Server Parameters
# Configured parameters :
#    -clientIpv4Address
#    -multiplier
################################################################################
puts "Adding Adding Netconf Server Parameters"
set clientIpv4AddressMv [ixNet getAttribute $netconfServer1 -clientIpv4Address]
ixNet add $clientIpv4AddressMv "singleValue"
ixNet setMultiAttribute $clientIpv4AddressMv/singleValue\
            -value "1.1.1.2"
ixNet commit
ixNet setAttribute $netconfServer1 -multiplier "1"
ixNet commit

################################################################################
# Adding topology
################################################################################
puts "Adding topology 2"
set topology2 [ixNet add $root "topology"]
ixNet commit
set topology2 [lindex [ixNet remapIds $topology2] 0]
ixNet setAttribute $topology2 -name "Topology 2"
ixNet setAttribute $topology2 -vports $vport2
ixNet commit
################################################################################
# Adding device group
################################################################################
puts "Adding device group 2"
set device2 [ixNet add $topology2 "deviceGroup"]
ixNet commit
set device2 [lindex [ixNet remapIds $device2] 0]
ixNet setAttribute $device2 -name "Device Group 2"
ixNet setAttribute $device2 -multiplier "1"
ixNet commit
################################################################################
# Adding ethernet layer
################################################################################
puts "Adding ethernet 2"
set ethernet2 [ixNet add $device2 "ethernet"]
ixNet commit
set ethernet2 [lindex [ixNet remapIds $ethernet2] 0]
set macMv [ixNet getAttribute $ethernet2 -mac]
ixNet add $macMv "counter"
ixNet setMultiAttribute $macMv/counter\
             -direction "increment"\
             -start     "00:12:01:00:00:01"\
             -step      "00:00:00:00:00:01"

ixNet commit
################################################################################
# Adding IPv4 layer
################################################################################
puts "Adding ipv4 2"
set ipv4Addr2  [ixNet add $ethernet2 "ipv4"]
ixNet commit
set ipv4Addr2 [lindex [ixNet remapIds $ipv4Addr2] 0]
set addressMv [ixNet getAttribute $ipv4Addr2 -address]
ixNet add $addressMv "singleValue"
ixNet setMultiAttribute $addressMv/singleValue\
            -value "1.1.1.2"
set gatewayIpMv [ixNet getAttribute $ipv4Addr2 -gatewayIp]
ixNet add $gatewayIpMv "singleValue"
ixNet setMultiAttribute $gatewayIpMv/singleValue\
            -value "1.1.1.1"
ixNet commit

################################################################################
# Adding Netconf Client layer
# Configured parameters :
#    -serverIpv4Adress
#    commandSnippetsData
################################################################################
puts "Adding Netconf Client 2"
set netconfClient2 [ixNet add $ipv4Addr2 "netconfClient"]
ixNet commit
set netconfClient2 [lindex [ixNet remapIds $netconfClient2] 0]
ixNet commit
set serverIPAdd [ixNet getAttribute $netconfClient2 -serverIpv4Address]
ixNet commit
set serverIPAdd [lindex [ixNet remapIds $serverIPAdd] 0]
ixNet add $serverIPAdd "singleValue"
ixNet setMultiAttribute $serverIPAdd/singleValue\
            -value "1.1.1.1"
ixNet commit

puts "Adding Netconf Client 2 Command Snippet Data"
set commandSnippetsData1 [ixNet getList $netconfClient2 commandSnippetsData]
ixNet commit
set commandSnippetsData1 [lindex [ixNet remapIds $commandSnippetsData1] 0]
ixNet commit
after 2000

puts "Setting Command Snippet Directory \n"
set commandSnippetDirectory1 [ixNet getA $commandSnippetsData1 -commandSnippetDirectory]
ixNet commit
set commandSnippetDirectory1 [lindex [ixNet remapIds $commandSnippetDirectory1] 0]
ixNet commit

ixNet setA $commandSnippetDirectory1/singleValue -value "C:\\Program Files (x86)\\Ixia\\IxNetwork\\8.50-EA\\SampleScripts\\IxNetwork\\NGPF\\Tcl\\SDN\\Netconf"
ixNet commit

puts "Setting Command Snippet File Name \n"
set commandSnippetFile1 [ixNet getA $commandSnippetsData1 -commandSnippetFile]

ixNet setA $commandSnippetFile1/singleValue -value "Get-config.xml"
ixNet commit

puts "Setting Command Snippet Active \n"
set commandSnippetDataActive1 [ixNet getA $commandSnippetsData1 -active]
ixNet commit
set commandSnippetDataActive1 [lindex [ixNet remapIds $commandSnippetDataActive1] 0]
ixNet commit
ixNet setAttr $commandSnippetDataActive1/singleValue -value true
ixNet commit

puts "Setting Command Snippet Transmission Behaviour \n"
set transmissionBehaviour1 [ixNet getA $commandSnippetsData1 -transmissionBehaviour]
set transmissionBehaviourOv [ixNet add $transmissionBehaviour1 overlay]

ixNet setA $transmissionBehaviourOv -count 1 -index 1 -value "once"
ixNet commit
ixNet setA $transmissionBehaviourOv -count 1 -index 2 -value "periodiccontinuous"
ixNet commit
################################################################################
# 2. Assign ports
################################################################################
puts "Assigning the ports"
set vPorts [ixNet getList $root "vport"]
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Starting all protocols"
################################################################################
# 3. Start all protocols
################################################################################
ixNet execute "startAllProtocols"
puts "Wait for 1 minute"
after 60000

################################################################################
# 4. Sending Command Snippet by executing Right Click Action 				   #
################################################################################
puts "Sending Command Snippet by executing Right Click Action"
ixNet exec executeCommand $commandSnippetsData1 {1 2}
after 15000

################################################################################
# 5. Retrieve protocol statistics. (Netconf Client Sessions Per Port)          #
################################################################################
puts "Fetching all Netconf Client Sessions Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Netconf Client Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -40 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"

################################################################################
# 6. Retrieve protocol statistics. (Netconf Server Per Port)                   #
################################################################################
puts "Fetching all Netconf Server Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Netconf Server Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -40 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "***************************************************"
after 5000

################################################################################
# 7. Stop all protocols                                                        #
################################################################################
ixNet execute "stopAllProtocols"
