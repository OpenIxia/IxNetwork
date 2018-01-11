
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
#   1. This scripts shows how we should configure PCC/RSVP to synchronize      #
#      RSVP-TE LSPs by PCC. RSVP-TE and PCC will be running on same device and #
#      LSPs that are brought up by the RSVP-TE will be synchronized by the     #
#      PCC to the PCE.                                                         #
#   2. Assign ports.                                                           #
#   3. Start all protocols.                                                    #
#   4. Retrieve PCE Sessions Per Port statistics.                              #
#   5. Retrieve PCC Per port statistics.                                       #
#   6. Stop all protocols.                                                     #
################################################################################
puts "Load ixNetwork Tcl API package"
package req IxTclNetwork
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ports       {{10.216.108.96 4 3} {10.216.108.96 4 4}}
    set ixTclServer 10.216.108.113
    set ixTclPort   8074
}

################################################################################
# Connect to IxNet client
################################################################################
ixNet connect $ixia::ixTclServer -port  $ixia::ixTclPort -version "8.10"

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
# Adding PCE layer
################################################################################
puts "Adding PCE 1"
set pce1 [ixNet add $ipv4Addr1 "pce"]
ixNet commit
set pce1  [lindex [ixNet remapIds $pce1] 0]
################################################################################
# Adding PCC Group
# Configured parameters :
#    -pccIpv4Address
#    -multiplier
#    -pceInitiatedLspsPerPcc
################################################################################
puts "Adding PCC Group1"
set pccGroup1 [ixNet add $pce1 "pccGroup"]
ixNet commit
set pccGroup1 [lindex [ixNet remapIds $pccGroup1] 0]
set pccIpv4AddressMv [ixNet getAttribute $pccGroup1 -pccIpv4Address]
ixNet add $pccIpv4AddressMv "singleValue"
ixNet setMultiAttribute $pccIpv4AddressMv/singleValue\
            -value "1.1.1.2"
ixNet commit
ixNet setAttribute $pccGroup1 -multiplier "1"
ixNet commit
ixNet setAttribute $pccGroup1 -pceInitiatedLspsPerPcc "0"
ixNet commit

################################################################################
# Adding RSVP layer
# Configured parameters :
#    -dutIp
################################################################################
puts "Adding rsvp 1"
set rsvpIf1  [ixNet add $ipv4Addr1 "rsvpteIf"]
ixNet commit
set rsvpIf1 [lindex [ixNet remapIds $rsvpIf1] 0]
set dutIpMv [ixNet getAttribute $rsvpIf1 -dutIp]
ixNet add $dutIpMv "singleValue"
ixNet setMultiAttribute $dutIpMv/singleValue\
            -value "1.1.1.2"
ixNet commit

################################################################################
# Adding RSVP LSP
# Configured parameters :
#    -ingressP2PLsps
################################################################################
puts "Adding rsvp 1"
set rsvpteLsps1 [ixNet add $ipv4Addr1 "rsvpteLsps"]
ixNet commit
set rsvpteLsps1 [lindex [ixNet remapIds $rsvpteLsps1] 0]
ixNet setAttribute $rsvpteLsps1 -ingressP2PLsps "0"
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
# Adding PCC layer
# Configured parameters :
#    -pceIpv4Address
#    -expectedInitiatedLspsForTraffic
#    -preEstablishedSrLspsPerPcc
#    -requestedLspsPerPcc
################################################################################
puts "Adding PCC 2"
set pcc2 [ixNet add $ipv4Addr2 "pcc"]
ixNet commit
set pcc2 [lindex [ixNet remapIds $pcc2] 0]
set pceIpv4AddressMv [ixNet getAttribute $pcc2 -pceIpv4Address]
ixNet add $pceIpv4AddressMv "singleValue"
ixNet setMultiAttribute $pceIpv4AddressMv/singleValue\
            -value "1.1.1.1"
ixNet commit
ixNet setAttribute $pcc2 -expectedInitiatedLspsForTraffic "0"
ixNet commit
ixNet setAttribute $pcc2 -preEstablishedSrLspsPerPcc "0"
ixNet commit
ixNet setAttribute $pcc2 -requestedLspsPerPcc "0"
ixNet commit

################################################################################
# Adding RSVP layer
# Configured parameters :
#    -dutIp
################################################################################
puts "Adding rsvp 2"
set rsvpIf2  [ixNet add $ipv4Addr2 "rsvpteIf"]
ixNet commit
set rsvpIf2 [lindex [ixNet remapIds $rsvpIf2] 0]
set dutIpMv [ixNet getAttribute $rsvpIf2 -dutIp]
ixNet add $dutIpMv "singleValue"
ixNet setMultiAttribute $dutIpMv/singleValue\
            -value "1.1.1.1"
ixNet commit

################################################################################
# Adding RSVP LSP
# Configured parameters :
#    -ingressP2PLsps
################################################################################
puts "Adding rsvp 2"
set rsvpteLsps2 [ixNet add $ipv4Addr2 "rsvpteLsps"]
ixNet commit
set rsvpteLsps2 [lindex [ixNet remapIds $rsvpteLsps2] 0]
ixNet setAttribute $rsvpteLsps2 -ingressP2PLsps "10"
ixNet commit
################################################################################
# Adding RSVP P2P tunnel
# Configured parameters :
#    -tunnelId
#    -remoteIp
################################################################################
set rsvpp2p2 $rsvpteLsps2/rsvpP2PIngressLsps
set tunnelIdMv [ixNet getAttribute $rsvpp2p2 -tunnelId]
ixNet add $tunnelIdMv "counter"
ixNet setMultiAttribute $tunnelIdMv/counter\
             -direction "increment"\
             -start     "1"\
             -step      "1"

ixNet commit
set remoteIpMv [ixNet getAttribute $rsvpp2p2 -remoteIp]
ixNet add $remoteIpMv "singleValue"
ixNet setMultiAttribute $remoteIpMv/singleValue\
            -value "1.1.1.1"
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
# 4. Retrieve protocol statistics. (PCE Sessions Per Port)                     #
################################################################################
puts "Fetching all PCE Sessions Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"PCE Sessions Per Port"/page}
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
# 5. Retrieve protocol statistics. (PCC Per Port)                              #
################################################################################
puts "Fetching all PCC Per Port Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"PCC Per Port"/page}
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
# 6. Stop all protocols                                                        #
################################################################################
ixNet execute "stopAllProtocols"
