#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to configure an ipv4 test and run it for 60 seconds
#
#
#------------------------------------------------------------------------------



# Define the chassis, card and ports.
set hostname xm12-automation														;# set the chassis name/ip
set card 1																			;# set card number
set port1 1																			;# set port number (first port)
set port2 2																			;# set port number (second port)

# load the IxNetwork TCL files
package require IxTclNetwork														;# access TCL Package

# connect to the IxNetwork TCL Server running on a Windows PC
ixNet connect localhost																;# connect ot IxNetwork

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

# add ethernet layer
set ethernet1 [ixNet add $vport1/protocolStack ethernet]							;# create ethernet layer for the first port
set ethernet2 [ixNet add $vport2/protocolStack ethernet]							;# create ethernet layer for the second port
ixNet commit																		;# save the config and map them to local IDs
set ethernet1 [ixNet remapIds $ethernet1]											;# replace local references with permanent IxNetwork server-based object references
set ethernet2 [ixNet remapIds $ethernet2]

# add IP endpoint
set ipEndpoint1 [ixNet add $ethernet1 ipEndpoint]									;# create IP endpoint for the first port
set ipEndpoint2 [ixNet add $ethernet2 ipEndpoint]									;# create IP endpoint for the second port
ixNet commit																		;# save the config and map them to local IDs
set ipEndpoint1 [ixNet remapIds $ipEndpoint1]										;# replace local references with permanent IxNetwork server-based object references
set ipEndpoint2 [ixNet remapIds $ipEndpoint2]

# add range parameters
set range1 [ixNet add $ipEndpoint1 range]											;# create the range for the first port
ixNet setAttribute $range1/macRange -mac {aa:bb:cc:22:22:22}						;# configure MAC address
ixNet setAttribute $range1/ipRange -ipAddress {9.0.0.1}								;# configure IP address
ixNet setAttribute $range1/ipRange -prefix 16										;# configure netmask
ixNet setAttribute $range1/ipRange -gatewayAddress {9.0.0.2}						;# configure gateway

set range2 [ixNet add $ipEndpoint2 range]											;# create the range for the second port
ixNet setAttribute $range2/macRange -mac {ba:bb:cc:33:33:33}						;# configure MAC address
ixNet setAttribute $range2/ipRange -ipAddress {9.0.0.2}								;# configure IP address
ixNet setAttribute $range2/ipRange -prefix 16										;# configure netmask
ixNet setAttribute $range2/ipRange -gatewayAddress {9.0.0.1}						;# configure gateway
ixNet commit																		;# save the config and map them to local IDs
set range1 [ixNet remapIds $range1]													;# replace local references with permanent IxNetwork server-based object references
set range2 [ixNet remapIds $range2]

# run the test for one minute
ixNet exec startAllProtocols														;# start the test
after 60000																			;# run for 60 seconds
ixNet exec stopAllProtocols															;# stop the test