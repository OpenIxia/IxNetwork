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