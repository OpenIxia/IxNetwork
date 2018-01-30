################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Daniel Iordache $
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
#                                                                             															  #
# Description:                                                                 													  #
#    This sample script configures a RFC2544 Throughput/Latency classic QT    						  #						  
#                                                                              														  #
# Steps:   1 -> Cleaning up IxNetwork                                          										  #
#	   			2 -> Add ports                                                      												  #
#	   			3 -> Creating QT                                                    											  #
#	   			4 -> Set source and destination                                     										  #
#	   			5 -> Create endpoint set                                            											  #	
#	   			6 -> Add o2o traffic map                                            											  #
#	   			7 -> Set Ipv4 protocol                                              											  #
#	   			8 -> Set Ipv4 addresses                                             											  #
#	   			9 -> Set parameters to QT                                           										  #
#	   			10 -> Assigning ports to virtual ports                              										  #
#	   			11 -> Apply QT                                                      											  #
#                                                                              														  #
################################################################################

namespace eval ::py {
    #client domain name or ip address
    set ixTclServer PC-name 
    #client Tcl port
    set ixTclPort   8009    
    #chassis ip address/domain name ; card number ; port number	
    set ports       {{192.168.1.1 1 1} {192.168.1.1 1 2}} 
}


################################################################################
# Source the IxNet library
################################################################################
package req IxTclNetwork

################################################################################
# Connect to IxNet client
################################################################################
ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 7.50

################################################################################
# Cleaning up IxNetwork
################################################################################
puts "Step 1 -> Cleaning up IxNetwork..."
ixNet exec newConfig

puts "Step 2 -> Add ports"

ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vport1 [lindex $vPorts 0]
set vport2 [lindex $vPorts 1]

################################################################################
# TEST BODY START
################################################################################
puts "Step 3 -> Creating QT"
set test [ixNet add /quickTest "rfc2544throughput"]
ixNet setAttribute $test -mode newMode
ixNet setAttribute $test/protocolSettings -protocolType classic
ixNet commit


puts "Step 4 -> Set source and destination"
set map [ixNet add $test/trafficMapping "lightMap"]
set source [ixNet add $map "source"]
set destination [ixNet add $map "destination"]
ixNet commit

puts "Step 5 -> Create endpoint set"
ixNet setAttribute $map -mapName EndpointSet1
ixNet commit


puts "Step 6 -> Add o2o traffic map"
ixNet setMultiAttribute $source \-portName Port1 \-portId $vport1
ixNet setMultiAttribute $destination \-portName Por2 \-portId $vport2
ixNet setAttribute $test/trafficMapping -usesLightMaps True
ixNet commit


puts "Step 7 -> Set Ipv4 protocol"
ixNet setAttribute $test/frameData -trafficType ipv4
ixNet commit

puts "Step 8 -> Set Ipv4 addresses"
ixNet setMultiAttribute $test/frameData/automaticIp/ip \-firstSrcIpAddr 192.168.1.1 \-firstGwIpAddr 192.168.1.1 \-addrIncrementAcrossInterface 0.0.0.0 \-addrIncrement 0.0.0.0
ixNet commit

puts "Step 9 -> Set parameters to QT"
ixNet setMultiAttribute $test/testConfig \-frameSizeMode custom \-framesizeList [list 128] \-initialBinaryLoadRate 50 \-binaryResolution 25 \-duration 10
ixNet commit

################################################################################
# Assign ports 
################################################################################
set vPorts [ixNet getList [ixNet getRoot] vport]
puts "Step 10 -> Assigning ports to $vPorts"
::ixTclNet::AssignPorts $py::ports {} $vPorts force
puts "Done"
after 2000

################################################################################
# Apply QT
################################################################################
puts "Step 11 -> Apply QT"
ixNet execute apply $test
    
################################################################################
# TEST END
################################################################################