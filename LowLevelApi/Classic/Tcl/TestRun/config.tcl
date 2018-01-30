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
