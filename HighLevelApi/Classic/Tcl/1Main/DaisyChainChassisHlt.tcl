#!/opt/ActiveTcl-8.5/bin/tclsh

# Connecting to multiple Ixia chassis's.

# About daisy chaining Ixia chassis's:
# 
# There's nothing that needs to be done. IxNetwork and IxExplorer 
# will recognize which are the Master and Slave (and actually, they don't care).
# Turn on the Master chassis first, and bring up IxServer. Once IxServer says it's 
# master, you can turn up the Slave chassis and bring up IxServer on that chassis. 
# Make sure IxServer on that chassis recognizes it's a slave.

# Add the chassis and  ports to the IxNetwork config (slave or master doesn't matter). 
# In IxExplorer, just connect to both the chassis. Again master or slave doesn't matter.

# Whenever connecting from a Linux machine, always include -tcl_server, and
# the tcl server could be from either master or slave.  It doesn't matter.

set chassisIpList "10.219.117.101 10.219.117.102"
set tclServer 10.219.117.102
set ixNetTclServer 10.219.117.103
set userName hgee

set portList [list [list 1/1 1/2 1/3] [list 1/9 1/10 1/11]]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect  \
			-config_file vport_order.ixncfg \
			-device      $chassisIpList \
			-tcl_server  $tclServer \
			-port_list   $portList \
			-ixnetwork_tcl_server $ixNetTclServer \
			-username  $userName \
		       ]
if {[keylget connect_status status] != $::SUCCESS} {
    puts "\nError: [keylget connect_status log]"
}
