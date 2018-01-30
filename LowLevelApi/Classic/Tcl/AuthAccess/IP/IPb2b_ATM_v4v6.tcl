#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to configure 2 ranges, 1 with ipv4 and another one with ipv6.
#
#
#------------------------------------------------------------------------------


# Define the chassis, card and ports.
set hostname xm12-automation														;# set the chassis name/ip														
set card 7																			;# set card number
set port1 1																			;# set port number (first port)
set port2 2																			;# set port number (second port)

# load the IxNetwork TCL files
package require IxTclNetwork														;# access TCL Package

# connect to the IxNetwork TCL Server running on a Windows PC
ixNet connect localhost																;# connect to IxNetwork

# create a new configuration file
ixNet rollback																		;# abandon all changes since last commit command				
ixNet exec newConfig																;# load a new (empty) IxNetwork configuration

# create the root object and add the chassis to it
set root [ixNet getRoot] 															;# create root object
set chassisObject [ixNet add $root/availableHardware chassis] 						;# create a chassis object 
ixNet setAttribute $chassisObject -hostname $hostname 								;# assign the name of the physical chassis
ixNet commit																		;# save the config and map them to local IDs
set chassisObject [ixNet remapIds $chassisObject]									;# replace local references with permanent IxNetwork server-based object references

# add virtual ports and map to real ports
set vport1 [ixNet add $root vport]													;# create first virtual port
set vport2 [ixNet add $root vport]													;# create second virtual port
ixNet setAttribute $vport1 -connectedTo $chassisObject/card:${card}/port:${port1}	;# first physical port used in test
ixNet setAttribute $vport2 -connectedTo $chassisObject/card:${card}/port:${port2}	;# second physical port used in test
ixNet commit																		;# save the config and map them to local IDs						
set vport1 [ixNet remapIds $vport1]													;# replace local references with permanent IxNetwork server-based object references
set vport2 [ixNet remapIds $vport2]													

# add ATM layer
set atm1 [ixNet add $vport1/protocolStack atm]										;# create atm layer for the first port
set atm2 [ixNet add $vport2/protocolStack atm]										;# create atm layer for the second port
ixNet commit																		;# save the config and map them to local IDs
set atm1 [ixNet remapIds $atm1]														;# replace local references with permanent IxNetwork server-based object references
set atm2 [ixNet remapIds $atm2]

# add IP endpoint
set ipEndpoint1 [ixNet add $atm1 ipEndpoint]										;# create IP endpoint for the first port
set ipEndpoint2 [ixNet add $atm2 ipEndpoint]										;# create IP endpoint for the second port
ixNet commit																		;# save the config and map them to local IDs
set ipEndpoint1 [ixNet remapIds $ipEndpoint1]										;# replace local references with permanent IxNetwork server-based object references
set ipEndpoint2 [ixNet remapIds $ipEndpoint2]

# add range parameters
set range11 [ixNet add $ipEndpoint1 range]											;# create the first range on the first port
ixNet setAttribute $range11/atmRange -encapsulation {6}								;# set the encapsulation type to LLC ROUTED AAL5 SNAP
ixNet setAttribute $range11/atmRange -mac {aa:bb:cc:00:00:00}						;# configure MAC address
ixNet setAttribute $range11/atmRange -count 10										;# configure number of interfaces
ixNet setAttribute $range11/pvcRange -vpiFirstId 17									;# configure VPI 
ixNet setAttribute $range11/pvcRange -vciFirstId 30									;# configure VCI
ixNet setAttribute $range11/ipRange -enabled True									;# enable IP range
ixNet setAttribute $range11/ipRange -ipAddress {10.0.0.1}							;# configure IP address
ixNet setAttribute $range11/ipRange -prefix 16										;# configure netmask
ixNet setAttribute $range11/ipRange -incrementBy {0.0.0.2}							;# configure IP increment
ixNet setAttribute $range11/ipRange -count 10										;# configure number of IP interfaces
ixNet setAttribute $range11/ipRange -gatewayAddress {10.0.0.2}						;# configure gateway address
ixNet setAttribute $range11/ipRange -gatewayIncrement {0.0.0.2}						;# configure gateway increment

set range12 [ixNet add $ipEndpoint1 range]											;# create the second range on the first port
ixNet setAttribute $range12/atmRange -encapsulation {6}								;# set the encapsulation type to LLC ROUTED AAL5 SNAP
ixNet setAttribute $range12/atmRange -mac {ba:bb:cc:00:00:00}						;# configure MAC address
ixNet setAttribute $range12/atmRange -count 100										;# configure number of interfaces
ixNet setAttribute $range12/pvcRange -vpiFirstId 50									;# configure VPI
ixNet setAttribute $range12/pvcRange -vciFirstId 70									;# configure VCI
ixNet setAttribute $range12/ipRange -enabled True									;# enable IP range
ixNet setAttribute $range12/ipRange -ipType {IPv6}									;# set NCP type to IPv6
ixNet setAttribute $range12/ipRange -ipAddress {17::1}								;# configure IPv6 address
ixNet setAttribute $range12/ipRange -prefix 48										;# configure IPv6 prefix 
ixNet setAttribute $range12/ipRange -incrementBy {::2}								;# configure IPv6 increment
ixNet setAttribute $range12/ipRange -count 100										;# configure number of IPv6 interfaces
ixNet setAttribute $range12/ipRange -gatewayAddress {17::2}							;# configure IPv6 gateway address
ixNet setAttribute $range12/ipRange -gatewayIncrement {::2}							;# configure IPv6 gateway increment

set range21 [ixNet add $ipEndpoint2 range]											;# create the first range on the second port
ixNet setAttribute $range21/atmRange -encapsulation {6}								;# set the encapsulation type to LLC ROUTED AAL5 SNAP
ixNet setAttribute $range21/atmRange -mac {ca:bb:cc:00:00:00}						;# configure MAC address				
ixNet setAttribute $range21/atmRange -count 10										;# configure number of interfaces
ixNet setAttribute $range21/pvcRange -vpiFirstId 17									;# configure VPI
ixNet setAttribute $range21/pvcRange -vciFirstId 30									;# configure VCI
ixNet setAttribute $range21/ipRange -enabled True									;# enable IP range
ixNet setAttribute $range21/ipRange -ipAddress {10.0.0.2}							;# configure IP address
ixNet setAttribute $range21/ipRange -prefix 16										;# configure netmask
ixNet setAttribute $range21/ipRange -incrementBy {0.0.0.2}							;# configure IP increment
ixNet setAttribute $range21/ipRange -count 10										;# configure number of IP interfaces
ixNet setAttribute $range21/ipRange -gatewayAddress {10.0.0.1}						;# configure gateway address
ixNet setAttribute $range21/ipRange -gatewayIncrement {0.0.0.2}						;# configure gateway increment

set range22 [ixNet add $ipEndpoint2 range]											;# create the second range on the second port
ixNet setAttribute $range22/atmRange -encapsulation {6}								;# set the encapsulation type to LLC ROUTED AAL5 SNAP
ixNet setAttribute $range22/atmRange -mac {da:bb:cc:00:00:00}						;# configure MAC addresss
ixNet setAttribute $range22/atmRange -count 100										;# configure number of interfaces
ixNet setAttribute $range22/pvcRange -vpiFirstId 50									;# configure VPI
ixNet setAttribute $range22/pvcRange -vciFirstId 70									;# configure VCI
ixNet setAttribute $range22/ipRange -enabled True									;# enable IP range
ixNet setAttribute $range22/ipRange -ipType {IPv6}									;# set NCP type to IPv6
ixNet setAttribute $range22/ipRange -ipAddress {17::2}								;# configure IPv6 address
ixNet setAttribute $range22/ipRange -prefix 48										;# configure IPv6 prefix
ixNet setAttribute $range22/ipRange -incrementBy {::2}								;# configure IPv6 increment
ixNet setAttribute $range22/ipRange -count 100										;# configure number of IPv6 interfaces
ixNet setAttribute $range22/ipRange -gatewayAddress {17::1}							;# configure IPv6 gateway address
ixNet setAttribute $range22/ipRange -gatewayIncrement {::2}							;# configure IPv6 gateway increment
ixNet commit																		;# save the config and map them to local IDs
set range11 [ixNet remapIds $range11]												;# replace local references with permanent IxNetwork server-based object references
set range12 [ixNet remapIds $range12]												
set range21 [ixNet remapIds $range21]	
set range22 [ixNet remapIds $range22]

# run the test for one minute
ixNet exec startAllProtocols														;# start the test													
after 60000																			;# run for 60 seconds
ixNet exec stopAllProtocols															;# stop the test
