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

#-----------------------------------------------------------------------------#
# FILE NAME  : Configuration.tcl                                              #
#                                                                             #
# PURPOSE    : To specify a test bed on which sample scripts provided could   #
#              be executed                                                    #
#                                                                             #
# PARAMETERS : Following information is required for running the test case    #
#              (1) Chassis-Name/Chassis-IP 1, Chassis-Name/Chassis-IP 2.      #
#              (2) Card1, Card2.                                              #
#              (3) Port1, Port2.                                              #
#              (4) Client-Name/Client-IP whrere the ixNetwork GUI should run. #
#              (5) The TCP port of ixNetwork tcl server.                      #
#              (6) IXOS BUILD.                                                #
#              (7) IxNetwork build                                            #
#                                                                             #
# ASSUMPTIONS: (1) user will change these parameters according to their need  #
#                  to run the scripts provided                                #
#              (2) If IxOs/IxNetwork build variables are changed the scripts  #
#                  needs to be run on a new wish console                      #
#              (3) All scripts are back to back                               #
#-----------------------------------------------------------------------------#
set ::chassis     10.205.28.195
set ::card1       9
set ::card2       9
set ::port1       1
set ::port2       2
set ::client      "10.205.28.84"
set ::tcpPort     8099
set ::IXOS_BUILD  "6.90.0.208"
set ::IX_NETWORK  "7.50.0.135-EB"

#-----------------------------------------------------------------------------#
# PLEASE DO NOT MODIFY THE SCRIPT BELOW THIS LINE                             #
#-----------------------------------------------------------------------------#
set envFileLocation "IxNetwork/Classic/Tcl/TestRun/setupEnv.tcl"
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/$envFileLocation
set ::argv0 $argv0
