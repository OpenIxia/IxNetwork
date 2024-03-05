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
#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to configure a PPPoE test with 2 ranges, 1 ipv4 and 1 ipv6. The test will have QinQ configured and will run for 60 seconds
#
#
#------------------------------------------------------------------------------



# Define the chassis, card and ports.
set hostname xm12-automation														
set card 1																			
set port1 1																			
set port2 2																			

# load the IxNetwork TCL files
package require IxTclNetwork														

# connect to the IxNetwork TCL Server running on a Windows PC
ixNet connect localhost																

# create a new configuration file
ixNet rollback																						
ixNet exec newConfig

# create the root object and add the chassis to it
set root [ixNet getRoot] 															
set chassisObject [ixNet add $root/availableHardware chassis] 						
ixNet setAttribute $chassisObject -hostname $hostname 								
ixNet commit																		
set chassisObject [ixNet remapIds $chassisObject]									

# add virtual ports and map to real ports
set vport1 [ixNet add $root vport]													
set vport2 [ixNet add $root vport]													
ixNet setAttribute $vport1 -connectedTo $chassisObject/card:${card}/port:${port1}	
ixNet setAttribute $vport2 -connectedTo $chassisObject/card:${card}/port:${port2}	
ixNet commit																								
set vport1 [ixNet remapIds $vport1]													
set vport2 [ixNet remapIds $vport2]													

# add ethernet layer
set ethernet1 [ixNet add $vport1/protocolStack ethernet]							
set ethernet2 [ixNet add $vport2/protocolStack ethernet]							
ixNet commit																		
set ethernet1 [ixNet remapIds $ethernet1]											
set ethernet2 [ixNet remapIds $ethernet2]

# add PPPoX endpoint
set pppoxEndpoint1 [ixNet add $ethernet1 pppoxEndpoint]									
set pppoxEndpoint2 [ixNet add $ethernet2 pppoxEndpoint]									
ixNet commit																		
set pppoxEndpoint1 [ixNet remapIds $pppoxEndpoint1]										
set pppoxEndpoint2 [ixNet remapIds $pppoxEndpoint2]

# add range parameters
set range11 [ixNet add $pppoxEndpoint1 range]	
ixNet setAttribute $range11/macRange -mac {aa:bb:cc:00:00:00}
ixNet setAttribute $range11/macRange -count 10
ixNet setAttribute $range11/vlanRange -enabled True
ixNet setAttribute $range11/vlanRange -firstId 1
ixNet setAttribute $range11/pppoxRange -clientBaseIp {3.3.3.3}
ixNet setAttribute $range11/pppoxRange -serverBaseIp {4.4.4.4}
ixNet setAttribute $range11/pppoxRange -authType {pap}
ixNet setAttribute $range11/pppoxRange -papUser {pap_user}
ixNet setAttribute $range11/pppoxRange -papPassword {pap_passwd}
ixNet setAttribute $range11/pppoxRange -numSessions 10

set range12 [ixNet add $pppoxEndpoint1 range]	
ixNet setAttribute $range12/macRange -mac {ba:bb:cc:00:00:00}
ixNet setAttribute $range12/macRange -count 100
ixNet setAttribute $range12/vlanRange -enabled True
ixNet setAttribute $range12/vlanRange -firstId 11
ixNet setAttribute $range12/vlanRange -innerEnable True
ixNet setAttribute $range12/vlanRange -innerFirstId 50
ixNet setAttribute $range12/pppoxRange -ncpType {IPv6}
#ixNet setAttribute $range12/pppoxRange -clientBaseIid {1::1}
ixNet setAttribute $range12/pppoxRange -clientIidIncr 10
ixNet setAttribute $range12/pppoxRange -authType {chap}
ixNet setAttribute $range12/pppoxRange -chapName {chap_user}
ixNet setAttribute $range12/pppoxRange -chapSecret {chap_passwd}
ixNet setAttribute $range12/pppoxRange -numSessions 100

set range21 [ixNet add $pppoxEndpoint2 range]	
ixNet setAttribute $range21/macRange -mac {ca:bb:cc:00:00:00}
ixNet setAttribute $range21/macRange -count 10
ixNet setAttribute $range21/vlanRange -enabled True
ixNet setAttribute $range21/vlanRange -firstId 1
ixNet setAttribute $range21/pppoxRange -authType {pap}
ixNet setAttribute $range21/pppoxRange -papUser {pap_user}
ixNet setAttribute $range21/pppoxRange -papPassword {pap_passwd}
ixNet setAttribute $range21/pppoxRange -numSessions 10

set range22 [ixNet add $pppoxEndpoint2 range]	
ixNet setAttribute $range22/macRange -mac {da:bb:cc:00:00:00}
ixNet setAttribute $range22/macRange -count 100
ixNet setAttribute $range22/vlanRange -enabled True
ixNet setAttribute $range22/vlanRange -firstId 11
ixNet setAttribute $range22/vlanRange -innerEnable True
ixNet setAttribute $range22/vlanRange -innerFirstId 50
ixNet setAttribute $range22/pppoxRange -ncpType {IPv6}
ixNet setAttribute $range22/pppoxRange -authType {chap}
ixNet setAttribute $range22/pppoxRange -chapName {chap_user}
ixNet setAttribute $range22/pppoxRange -chapSecret {chap_passwd}
ixNet setAttribute $range22/pppoxRange -numSessions 100

ixNet commit			
set range11 [ixNet remapIds $range11]	
set range12 [ixNet remapIds $range12]	
set range21 [ixNet remapIds $range21]											
set range22 [ixNet remapIds $range22]

# configuring PPPoX options
set pppoxOptions1 [ixNet add $vport1/protocolStack pppoxOptions]	
set pppoxOptions2 [ixNet add $vport2/protocolStack pppoxOptions]
ixNet setAttribute $pppoxOptions1 -role {server}						
ixNet setAttribute $pppoxOptions2 -role {client}
ixNet setAttribute $pppoxOptions2 -associates [list $vport1/protocolStack]	
ixNet commit
set pppoxOptions1 [ixNet remapIds $pppoxOptions1]
set pppoxOptions2 [ixNet remapIds $pppoxOptions2]

# run the test for one minute
ixNet exec startAllProtocols														
after 60000																			
ixNet exec stopAllProtocols															