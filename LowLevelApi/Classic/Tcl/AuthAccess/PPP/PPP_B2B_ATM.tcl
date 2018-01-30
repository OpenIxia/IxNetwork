#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to configure a PPPoAv4 test and run it for 60 seconds 
#
#
#------------------------------------------------------------------------------



# Define the chassis, card and ports.
set hostname xm12-automation														
set card 7																			
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

# add ATM layer
set atm1 [ixNet add $vport1/protocolStack atm]							
set atm2 [ixNet add $vport2/protocolStack atm]							
ixNet commit																		
set atm1 [ixNet remapIds $atm1]											
set atm2 [ixNet remapIds $atm2]

# add PPPoX endpoint
set pppoxEndpoint1 [ixNet add $atm1 pppoxEndpoint]									
set pppoxEndpoint2 [ixNet add $atm2 pppoxEndpoint]									
ixNet commit																		
set pppoxEndpoint1 [ixNet remapIds $pppoxEndpoint1]										
set pppoxEndpoint2 [ixNet remapIds $pppoxEndpoint2]

# add range parameters
set range1 [ixNet add $pppoxEndpoint1 range]	
ixNet setAttribute $range1/atmRange -encapsulation {2}
ixNet setAttribute $range1/atmRange -mac {aa:bb:cc:00:00:00}
ixNet setAttribute $range1/atmRange -count 10
ixNet setAttribute $range1/pvcRange -vpiFirstId 11
ixNet setAttribute $range1/pvcRange -vciFirstId 15
ixNet setAttribute $range1/pppoxRange -authType {pap}
ixNet setAttribute $range1/pppoxRange -papUser {username}
ixNet setAttribute $range1/pppoxRange -papPassword {password}

set range2 [ixNet add $pppoxEndpoint2 range]	
ixNet setAttribute $range2/atmRange -encapsulation {2}
ixNet setAttribute $range2/atmRange -mac {ba:bb:cc:00:00:00}
ixNet setAttribute $range2/atmRange -count 10
ixNet setAttribute $range2/pvcRange -vpiFirstId 11
ixNet setAttribute $range2/pvcRange -vciFirstId 15
ixNet setAttribute $range2/pppoxRange -clientBaseIp {5.5.5.5}
ixNet setAttribute $range2/pppoxRange -serverBaseIp {7.7.7.7}
ixNet setAttribute $range2/pppoxRange -authType {pap}
ixNet setAttribute $range2/pppoxRange -papUser {username}
ixNet setAttribute $range2/pppoxRange -papPassword {password}

ixNet commit			
set range1 [ixNet remapIds $range1]													
set range2 [ixNet remapIds $range2]

# configuring PPPoX options
set pppoxOptions1 [ixNet add $vport1/protocolStack pppoxOptions]	
set pppoxOptions2 [ixNet add $vport2/protocolStack pppoxOptions]
ixNet setAttribute $pppoxOptions1 -role {client}						
ixNet setAttribute $pppoxOptions1 -associates [list $vport2/protocolStack]	
ixNet setAttribute $pppoxOptions2 -role {server}
ixNet commit
set pppoxOptions1 [ixNet remapIds $pppoxOptions1]
set pppoxOptions2 [ixNet remapIds $pppoxOptions2]

# run the test for one minute
ixNet exec startAllProtocols														
after 60000																			
ixNet exec stopAllProtocols															