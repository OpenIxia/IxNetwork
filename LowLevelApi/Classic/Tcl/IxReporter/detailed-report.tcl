################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#                                                                              #
#    Copyright © 1997 - 2011 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    04/14 - Mircea Dan Gheorghe - created sample                              #
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
#     This script intends to demonstrate how IxNetwork-IxReporter API can be   #
#     used in order to generate a detailed pdf report using a custom template  #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    IxOS      6.10 EA (6.10.0.618)                                            #
#    IxNetwork 6.0  EA (6.0.0.265)                                             #
################################################################################

set IXN_TCL_SERVER 10.200.113.27
set CHASSIS_IP     10.200.113.61
set PORT_LIST      [list {1 11} {1 12}]

puts " load ixNetwork Tcl API package"
package req IxTclNetwork

puts " connect to ixNetwork Tcl server"
ixNet connect $IXN_TCL_SERVER -port 8009 -version 6.0

puts " load the binary config with 2 ports pre configured with traffic"
ixNet exec loadConfig [ixNet readFrom "ixReporter.ixncfg"]

puts " creating variables for the list of virtual ports and also for each virtual port"
set vport_list [ixNet getList [ixNet getRoot] vport]

set vport1 [lindex $vport_list 0]
set card1 [lindex [lindex $PORT_LIST 0] 0]
set port1 [lindex [lindex $PORT_LIST 0] 1]

set vport2 [lindex $vport_list 1]
set card2 [lindex [lindex $PORT_LIST 1] 0]
set port2 [lindex [lindex $PORT_LIST 1] 1]

puts " assign the virtual ports to real ports"
ixTclNet::AssignPorts [list [list $CHASSIS_IP $card1 $port1] [list $CHASSIS_IP $card2 $port2]] {} [list $vport1 $vport2] force

after 10000
puts " starting ospf"
ixNet exec startAllProtocols

after 10000

puts " configuring reporter settings"
ixNet setMultiAttrs [ixNet getRoot]/reporter/testParameters  \
    -testCategory     "Ixia Demo IxReporter API"             \
    -testDUTName      "No DUT just Ixia ports"               \
    -testerName       "Ixia tester"                          \
    -testHighlights   "Ixia test summary pdf report sample"  \
    -testName         "an Ixia sample"                       \
    -testObjectives   "to demo the IxReporter API"
ixNet commit

set template_path [ixNet getAttr [ixNet getRoot]/reporter/generate -templatePath]
set template_dir  [file dirname $template_path]
set template_name "OSPF-Detailed.repx"
set template_path [file join $template_dir $template_name]

puts " using $template_path template"
ixNet setMultiAttrs [ixNet getRoot]/reporter/generate      \
    -outputFormat    pdf                                   \
    -outputPath      {c:\detailedReport.pdf}               \
    -templatePath    $template_path
ixNet commit

puts " saving detailed results"
ixNet exec saveDetailedResults [ixNet getRoot]/reporter/saveResults


while  {[ixNet getAttribute [ixNet getRoot]/reporter/saveResults -state] != "done"} {
    after  1000
}
    
puts " generating report"    
ixNet exec generateReport [ixNet getRoot]/reporter/generate

while  {[ixNet getAttribute [ixNet getRoot]/reporter/generate -state] != "done"} {
    after  1000
}

puts "report c:\\detailedReport.pdf generation done"
puts "TEST END ."
puts " "
puts " "
puts " for more info on IxNetwork-IxReporter API please refer to the user manual or the build-in help"
puts " "
puts "ixNet help [ixNet getRoot]/reporter"
puts "[ixNet help [ixNet getRoot]/reporter]"
puts " "
puts "ixNet help [ixNet getRoot]/reporter/testParameters"
puts "[ixNet help [ixNet getRoot]/reporter/testParameters]"
puts " "
puts "ixNet help [ixNet getRoot]/reporter/generate"
puts "[ixNet help [ixNet getRoot]/reporter/generate]"
puts " "
puts "ixNet help [ixNet getRoot]/reporter/saveResults"
puts "[ixNet help [ixNet getRoot]/reporter/saveResults]"







