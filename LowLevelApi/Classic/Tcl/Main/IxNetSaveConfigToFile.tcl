#!/opt/ActiveTcl-8.5/bin/tclsh

set ixNetworkTclServer 10.205.4.160
set ixNetworkVersion 7.22
set ixNetPort 8009
set ixNetworkCfgFile mySavedConfig.ixncfg

package req Ixia

puts "Connecting to $ixNetworkTclServer"
catch {ixNet connect $ixNetworkTclServer -port $ixNetPort -version $ixNetworkVersion} errMsg
if {$errMsg != "::ixNet::OK"} {
    puts "\nError: Connecting to IxNet Tcl server $ixNetworkTclServer failed: $errMsg"
    exit
} else {
    puts "Connected to IxNet Tcl Server"
}

# To save a config in Windows
#ixNet exec saveConfig [ixNet writeTo "c:/temp/blah.ixncfg" -ixNetRelative -overwrite]

# To save a config in Linux
ixNet exec saveConfig [ixNet writeTo $ixNetworkCfgFile -overwrite]
