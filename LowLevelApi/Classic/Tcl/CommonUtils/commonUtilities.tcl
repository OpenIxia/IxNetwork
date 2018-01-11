#-----------------------------------------------------------------------------#
# global variable to recognize a test case by name                            #
#-----------------------------------------------------------------------------#
if {![info exists testId]} {
    global testId
}

#-----------------------------------------------------------------------------#
# PROCEDURE    : removePortList                                               #
# PURPOSR      : To clean up all the virtual ports from the IxNetwork GUI     #
# INPUT        : The list of virtual ports to be removed                      #
# OUTPUT       : Removes all the virtual ports from the IxNetwork GUI         #
# RETURN VALUE : void                                                         #
#-----------------------------------------------------------------------------#
proc removePortList {portList} {
    set len [llength $portList]
    set i 0
    while { $i < $len } {
        set port [lindex $portList $i]
        ixNet remove $port
        ixNet commit
        incr i
    }
}

#-----------------------------------------------------------------------------#
# PROCEDURE    : ixNetCleanUp                                                 #
# PURPOSR      : Cleaning up, stop all protocols if running, close alnalyzer  #
#                tabs if open, stop test configuration etc.                   #
# INPUT        : void                                                         #
# OUTPUT       : Cleans up all configurations from IxNetwork GUI              #
# RETURN VALUE : void                                                         #
# ASSUMPTION   : we are in the "connected" with the IxNetwork GUI             #
#-----------------------------------------------------------------------------#
proc ixNetCleanUp {} {

    # if protocols are not stopped handle it from here
    catch {ixNet exec stopAllProtocols}

    # Clean all tabs
    catch {ixNet exec closeAllTabs}

    # Stop integrated if running
    catch {
         #stop test configuration if it is running
         catch {ixNet exec stopTestConfiguration}

         while { [regexp [ixNet getAtt [ixNet getRoot]/testConfiguration \
               -testRunning] true ] } {
               after 20000
          }
    };  # stopp !!!!

    # Remove port
    ixTclNet::UnassignPorts [ixNet getList [::ixNet getRoot] vport]
    removePortList [ixNet getList [::ixNet getRoot] vport]

    # clean
    catch {ixNet execute newConfig}
}

#-----------------------------------------------------------------------------#
# PROCEDURE    : getPortList                                                  #
# PURPOSR      : connecting to IxNetworl client                               #
# INPUT        : [list $chassis1 $card1 $port1 $client1 $tcpPort1] and        #
#                [list $chassis2 $card2 $port2 $client2 $tcpPort2]            #
# OUTPUT       : Connects to IxNetwork Tcl server and chassis                 #
# RETURN VALUE : list of virtual ports                                        #
#-----------------------------------------------------------------------------#
proc getPortList {portData1 portData2} {

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set hostName1  [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set hostName2  [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    set portList [list [list $chassisIp1 $card1 $port1] \
                       [list $chassisIp2 $card2 $port2] ]

    if {[catch {ixNet connect $hostName1 -port $tcpPort1} result]} {
        puts "error in connect: $result"
        set iter 1
        while {$iter <= 3} {
            after 1000
            if {[catch {ixNet connect $hostName1 -port $tcpPort1} \
                result]} {
                puts "error on connect retry $iter: $result"
            } else {
                puts "successful connect on retry $iter"
                break
            }
            incr iter
        }
    }

    # after connecting cleaning up the network
    ixNetCleanUp

    ixTclNet::AssignPorts $portList
    set vPortList [ixNet getList [::ixNet getRoot] vport]
    return $vPortList
}

#-----------------------------------------------------------------------------#
# PROCEDURE : connectToClient                                                 #
# PURPOSE   : connecting to IxNetwork client (but not assigning the port)     #
# INPUT     : portData1 portData2 and IxNetwork version                       #
# OUTPUT    : get connected to IxNetwork client                               #
#-----------------------------------------------------------------------------#
proc connectToClient {portData1 portData2 {ver 0.0}} {

    set chassisIP [getChassisIp  $portData1]

    set card1 [getCardNumber $portData1]
    set port1 [getPortNumber $portData1]

    set card2 [getCardNumber $portData2]
    set port2 [getPortNumber $portData2]

    set hostName1 [getHostName $portData1]
    set hostName2 [getHostName $portData2]

    set tclPortNumber1 [getTcpPort $portData1]
    set tclPortNumber2 [getTcpPort $portData2]

    set portList [list [list $chassisIP $card1 $port1] \
                       [list $chassisIP $card2 $port2]]

    if {[catch {ixNet_connect $hostName1 $tclPortNumber1 $ver} result]} {
        log "error in connect: $result"
        set iter 1
        while {$iter <= 3} {
            after 1000
            if {[catch {ixNet_connect $hostName1 $tclPortNumber1 $ver} \
                        result]} {
                log "error on connect retry $iter: $result"
            } else {
                log "successful connect on retry $iter"
                break
            }
            incr iter
        }
    }

    ixNet exec newConfig
    return $result
}


#-----------------------------------------------------------------------------#
# PROCEDURE : ixNet_connect                                                   #
# PURPOSE   : connecting to IxNetwork client (but not assigning the port)     #
#             being called form connectToClient                               #
# INPUT     : portData1 portData2 and IxNetwork version                       #
# OUTPUT    : get connected to IxNetwork client                               #
# ASSUMPTION: connectToClient is a wrapper of this proc. So that is basic     #
#             IxNet API changes it does not impacts coded scripts.            #
#-----------------------------------------------------------------------------#
proc ixNet_connect {hostName1 {port 8009} {version 0.0}} {

    set connectionResult ""
    if {$version < 5.40} {
        set isError [catch {set connectionResult [ixNet connect \
            $hostName1 -port $port]} error]
    } else {
        set isError [catch {set connectionResult [ixNet connect \
            $hostName1 -port $port -version $version]} error]
    }

    if {$isError} {
        error "$error"
    }
    return $connectionResult
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getChassisIp                                                    #
# PURPOSE   : extract the chassis IP from the port data list                  #
# INPUT     : the portDataList structure                                      #
# OUTPUT    : Chassis IP                                                      #
#-----------------------------------------------------------------------------#
proc getChassisIp {portData1} {
    return [lindex $portData1 0]
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getCardNumber                                                   #
# PURPOSE   : extract the chassis IP from the port data list                  #
# INPUT     : the portDataList structure                                      #
# OUTPUT    : Chassis IP                                                      #
#-----------------------------------------------------------------------------#
proc getCardNumber {portData1} {
    return [lindex $portData1 1]
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getPortNumber                                                   #
# PURPOSE   : extract the chassis IP from the port data list                  #
# INPUT     : the portDataList structure                                      #
# OUTPUT    : Chassis IP                                                      #
#-----------------------------------------------------------------------------#
proc getPortNumber {portData1} {
    return [lindex $portData1 2]
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getHostName                                                     #
# PURPOSE   : extract the chassis IP from the port data list                  #
# INPUT     : the portDataList structure                                      #
# OUTPUT    : Chassis IP                                                      #
#-----------------------------------------------------------------------------#
proc getHostName {portData1} {
    return [lindex $portData1 3]
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getHostName                                                     #
# PURPOSE   : extract the chassis IP from the port data list                  #
# INPUT     : the portDataList structure                                      #
# OUTPUT    : Chassis IP                                                      #
#-----------------------------------------------------------------------------#
proc getTcpPort {portData1} {
    return [lindex $portData1 4]
}


#-----------------------------------------------------------------------------#
# PROCEDURE : getTestId                                                       #
# PURPOSE   : retriving the test case Id of a test case                       #
# INPUT     : none                                                            #
# OUTPUT    :the test cases id                                                #
#-----------------------------------------------------------------------------#
proc getTestId {} {
    global testId
    return $testId
}


#-----------------------------------------------------------------------------#
# PROCEDURE : setTestId                                                       #
# PURPOSE   : setting the test case Id of a test case                         #
# INPUT     : test cases id                                                   #
# OUTPUT    : none                                                            #
#-----------------------------------------------------------------------------#
proc setTestId {fileName} {
    global testId
    regexp {test.(.*).tcl} $fileName match testId
}


#-----------------------------------------------------------------------------#
# PROCEDURE : unsetTestId                                                     #
# PURPOSE   : un-setting the test case Id of a test case                      #
# INPUT     : none                                                            #
# OUTPUT    : none                                                            #
#-----------------------------------------------------------------------------#
proc unsetTestId {} {
    global testId
    set testId ""
}


#------------------------------------------------------------------------------#
# PROCEDURE  : getScriptGenFile                                                #
# PURPOSE    : Finds the Scriptgen file that is required for the current       #
#              test  cases                                                     #
# INPUT      : port index                                                      #
# OUTPUT     : scriptGen fileName                                              #
#------------------------------------------------------------------------------#
proc getScriptGenFile { {portIndex -1}} {

    set testId [getTestId]
    if {$portIndex == -1} {
        return "config.$testId.tcl"
    } else {
        return "config.$testId.$portIndex.tcl"
    }
}


#------------------------------------------------------------------------------#
# PROCEDURE  : scriptGenConfigPort                                             #
# PURPOSE    : Uses the Scriptgen file that was modified in ActionWrapper      #
#              and configures the port using it.                               #
# INPUT      : none                                                            #
# OUTPUT     : scriptGen file is being sourced                                 #
#              Return value is 0 if scriptgen is sourced successfully          #
#------------------------------------------------------------------------------#
proc scriptGenConfigPort {{portIndex -1}} {

    set retCode 0
    set scriptGen [getScriptGenFile $portIndex]
    source "$::pwd/$scriptGen"
    set addedPort [catch {ixNetScriptgenProc}]
    return $addedPort
}


#-----------------------------------------------------------------------------#
# PROCEDURE    : addVport                                                     #
# PURPOSE      : Adding two virtual ports                                     #
# PARAMETERS   : IxNetwork client info                                        #
# INPUT        : [list $chassis1 $card1 $port1 $client1 $tcpPort1] and        #
#                [list $chassis2 $card2 $port2 $client2 $tcpPort2]            #
# OUTPUT       : Connects to IxNetwork Tcl server (but not to chassis)        #
# ASSUMPTION   : We are adding two virtual ports only. We can assign real     #
#                ports to virtual ports latter.                               #
#-----------------------------------------------------------------------------#
proc addVport {portData1 portData2} {
    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set hostName1  [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set hostName2  [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    if {[catch {ixNet connect $hostName1 -port $tcpPort1} result]} {
        puts "error in connect: $result"
        set iter 1
        while {$iter <= 3} {
            after 1000
            if {[catch {ixNet connect $hostName1 -port $tcpPort1} \
                result]} {
                puts "error on connect retry $iter: $result"
            } else {
                puts "successful connect on retry $iter"
                break
            }
            incr iter
        }
    }

    # after connecting cleaning up the network
    ixNetCleanUp

    # Add two virtual ports
    set root      [ixNet getRoot]
    set vPort1    [ixNet add $root vport]
    set vPort2    [ixNet add $root vport]
    set vPortList [list $vPort1 $vPort2]

    return $vPortList
}

#--------------------------------------------------------------------------#
# PROCEDURE    : cleanupConfigurationFromPorts                             #
# PURPOSE      : Removing all the vitrual ports from the IxNetwork GUI     #
# RETURN VALUE : none                                                      #
#--------------------------------------------------------------------------#
proc cleanupConfigurationFromPorts {} {
    set portsList [ixNet getList [::ixNet getRoot] vport]
    ixTclNet::UnassignPorts $portsList
    foreach portId $portsList {
        ixNet remove $portId
    }
    ixNet commit
    ixNet exec newConfig
}


#--------------------------------------------------------------------------#
# PROCEDURE    : setPortPropertiesToFactoryDefaults                        #
# PURPOSE      : Setting a given port to factory defaults.                 #
# RETURN VALUE : none                                                      #
#--------------------------------------------------------------------------#
proc setPortPropertiesToFactoryDefaults {vport} {
    set err 0
    set setResult [ixNet execute setFactoryDefaults $vport]
    if {[string equal $setResult "::ixNet::OK"] != 1} {
        puts "set port to Factory defaults unsuccessfill for $vport"
        set err 1
        return $err
    }
    puts "set port to Factory defaults successfull for $vport"
    return $err
}



#-----------------------------------------------------------------------------#
# End of definations of all common utils                                      #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Put all other files util files to source in this directory                  #
#-----------------------------------------------------------------------------#
set srcDir "$env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl"
source $srcDir/CommonUtils/5.40TrafficCommonUtils.tcl
