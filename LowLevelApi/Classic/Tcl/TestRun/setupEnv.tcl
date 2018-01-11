#-----------------------------------------------------------------------------#
# IF this file is already sourced; it should not be sourced once more         #
#-----------------------------------------------------------------------------#
if {[info exists ::SETUP_ENV]} {
    # source only common utils path
    source $::COMMOM_UTILS_PATH/commonUtilities.tcl
    return
}

#-----------------------------------------------------------------------------#
# Find the Ixia Installation Directory                                        #
#-----------------------------------------------------------------------------#
set IXIA_INSTALL_DIR "C:/Program Files (x86)/Ixia/IxNetwork/$::IX_NETWORK"

#-----------------------------------------------------------------------------#
# Find the common utilities directory                                         #
#-----------------------------------------------------------------------------#
set ::COMMOM_UTILS_PATH  \
    "$IXIA_INSTALL_DIR/SampleScripts/IxNetwork/Classic/Tcl/CommonUtils"

#-----------------------------------------------------------------------------#
# Find the registry key path of IXOS                                          #
#-----------------------------------------------------------------------------#
set ixos $::IXOS_BUILD
set registryKeyPath \
"HKEY_LOCAL_MACHINE\\Software\\Ixia Communications\\IxOS\\$ixos\\InstallInfo"

#-----------------------------------------------------------------------------#
# Load IXOS package (IxTclHAL)                                                #
#-----------------------------------------------------------------------------#
if {$::tcl_platform(platform) == "windows"} {
    package require registry 1

    set ::_IXOS_INSTALL_ROOT [registry get $registryKeyPath HOMEDIR]
    set ::_IXOS_PKG_DIR $::_IXOS_INSTALL_ROOT

    lappend ::auto_path $::_IXOS_PKG_DIR
    source "$::_IXOS_PKG_DIR\\TclScripts\\bin\\IxiaWish.tcl"

    if {[catch {package req IxTclHal} errorMsg]} {
        puts "Unable to load IxTclHal ...."
        puts "Make sure that IXOS BUILD is specified/installed properly"
        error "$errorMsg"
    }
}

#-----------------------------------------------------------------------------#
# include the package IxTclNetwork                                            #
#-----------------------------------------------------------------------------#
if {[catch {package req IxTclNetwork} errMsg]} {
    puts "unable to load package IxTclNetwork"
    error $errMsg
}

#-----------------------------------------------------------------------------#
# include the package IxTclHal                                                #
#-----------------------------------------------------------------------------#
if {[catch {package req IxTclHal} errMsg]} {
    puts "unable to load package IxTclHal"
    error $errMsg
}

#-----------------------------------------------------------------------------#
# Withdraw the TK window                                                      #
#-----------------------------------------------------------------------------#
set isError [catch {wm withdraw .; update} errMsg]
if {$isError} {puts "$errMsg"}

#-----------------------------------------------------------------------------#
# Source some test-management utility procedures                              #
#-----------------------------------------------------------------------------#
source $IXIA_INSTALL_DIR/SampleScripts/IxNetwork/Classic/Tcl/TestRun/wrapper.tcl

#-----------------------------------------------------------------------------#
# source the common utility files                                             #
#-----------------------------------------------------------------------------#
source $::COMMOM_UTILS_PATH/commonUtilities.tcl

#-----------------------------------------------------------------------------#
# Rename old puts use new puts that will update puts statement immediately    #
# On the wish console                                                         #
#-----------------------------------------------------------------------------#
rename puts oldPuts
proc puts {args} {
    lappend cmdString oldPuts
    foreach argument $args {
        lappend cmdString $argument
    }
    eval $cmdString
    unset cmdString
    update
}

#-----------------------------------------------------------------------------#
# Define log functions (used extensively in test cases, same as puts)         #
#-----------------------------------------------------------------------------#
proc log {str} {puts $str}

#-----------------------------------------------------------------------------#
# All the environment variables are sourced. Scripts must be able to get the  #
# following environment variables                                             #
#                                                                             #
# 1)  $::IX_NETWORK        --> IxNetwork build number                         #
# 2)  $::IXOS_BUILD        --> IxOs build Number                              #
# 3)  $::COMMOM_UTILS_PATH --> Common utility file path                       #
# 4)  $::chassis           --> Chassis IP                                     #
# 5)  $::card1             --> Card 1                                         #
# 6)  $::card2             --> Card 2                                         #
# 7)  $::port1             --> Port 1                                         #
# 8)  $::port2             --> Port 2                                         #
# 9)  $::client            --> Client IP                                      #
# 10) $::tcpPort           --> TCP Port Number                                #
# 11) $::argv0             --> the parent script name                         #
#-----------------------------------------------------------------------------#
set ::SETUP_ENV 1
update