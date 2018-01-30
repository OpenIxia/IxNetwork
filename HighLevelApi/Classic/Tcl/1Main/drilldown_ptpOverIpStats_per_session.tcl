#!/opt/ActiveTcl-8.5/bin/tclsh

# Description:
#
#    ::ixia::ptp_over_ip_stats is only supported for NGPF.
#    This script is a workaround to get PTP stats using UDS.
# 
#    Load the ixncfg file /Temp/ptp_test1_jack.ixncfg.
#    Enable global Protocols.
#    Run the script to get the drill down per session stats for
#    PTP OverIP stats.
#    
#    NOTE: I used Theresa's Perl sample /Temp/script ptpoe_session_stats.pl.txt

package req Ixia

set ixiaChassisIp 10.219.117.101
set ixNetworkTclServerIp 10.219.16.219
set userName hgee

#source /home/hgee/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

puts "\nConnecting to $ixNetworkTclServerIp ..."

set status [::ixia::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
		-break_locks 1 \
	       ]

puts [KeylPrint status]

set trafficStats [::ixia::traffic_stats \
		      -mode user_defined_stats \
		      -uds_action get_available_protocol_stack_filters \
		      -uds_type l23_protocol_stack \
		     ]
		  
puts "\n--- trafficStatus: $trafficStats ----\n"
# trafficStatus: {status 1} {waiting_for_stats 1} {filters {{//PTP/Ethernet - 001/PTP-R1} {//PTP/Ethernet - 002/PTP-R2}}}

# Get the filter.  This variable "filters" contains the port name.
# In your case, you want the second port name since it  is the slave.
# Therefore, this sample code uses [lindex $filters 1] to get the second port
set filters [keylget trafficStats filters]
puts "\n---- filters: $filters : [lindex $filters 1] ----\n"

# filters: {//PTP/Ethernet - 001/PTP-R1} {//PTP/Ethernet - 002/PTP-R2}

set finalStats [::ixia::traffic_stats \
		-uds_l23ps_drilldown per_session \
		-mode user_defined_stats \
		-uds_type l23_protocol_stack \
		-uds_protocol_stack_filter [lindex $filters 1] \
		-uds_protocol_stack_filter_count 1 \
	       ]


puts "\nstats:\n\n[KeylPrint finalStats]\n\n"

set offset [keylget finalStats 1.Offset\ \[ns\]]
puts "\n==== offset: $offset ====\n"

stats:

status: 1
waiting_for_stats: 1
1:
 FM 0 Port Number: 1
CF PDelayReq [ns]: 0
Min Path Delay [ns]: 0
 Announce Messages Sent: 0
 Time t3 UTC: 09 March 2015 21:14:56.304069080
 Time Traceable: 0
 FM 2 Port Number: 0
CF PDelayRespFollowUp [ns]: 0
Max Path Delay [ns]: 0
Min Offset [ns]: -20
 FM 4 Port Number: 0
Path Delay [ns]: 0
CF FollowUp Min [ns]: 0
Max Offset [ns]: 20
IA FollowUp Min [ns]: 999169180
 Port Identity: 00:ee:ff:ff:fe:00:00:00
Offset [ns]: 0
 Steps Removed: 0
CF FollowUp [ns]: 0
CF PDelayResp [ns]: 0
 DelayResp Messages Sent: 0
 DelayResp Messages Received Rate: 0
CF DelayReq Min [ns]: 0
IA DelayReq Min [ns]: 0
IA Sync Max [ns]: 1001715480
 PdelayResp Messages Received: 0
IA DelayReq [ns]: 0
 FollowUp Messages Received Rate: 0
 FM 0 Identity: aa:bb:cc:ff:fe:00:00:00
 Stat Name: 10.219.117.101/Card1/Port2 - 1400000
IA Announce Min [ns]: 999191080
 DelayReq Messages Received: 0
CF DelayResp Min [ns]: 0
 Sync Messages Sent: 0
 FollowUp Messages Received: 4415
CF FollowUp Max [ns]: 0
IA FollowUp Max [ns]: 1001720560
IA Announce [ns]: 999983040
 FollowUp Messages Sent: 0
CF Sync Min [ns]: 0
 Master Clock Accuracy: The time is accurate to within 1 us
CF PDelayReq Min [ns]: 0
 Local Clock Class: 255
 FM 1 Identity: N/A
 Announce Messages Received: 6759
CF PDelayRespFollowUp Min [ns]: 0
CF DelayReq Max [ns]: 0
IA DelayReq Max [ns]: 0
IA DelayResp Min [ns]: 999864400
 Time t2 UTC: 09 March 2015 21:14:56.92055440
 PdelayReq Messages Sent: 0
 FM 1 Port Number: 0
 Time Slope: 1
 Time t4 UTC: 09 March 2015 21:14:56.304069020
Avg Path Delay [ns]: 0
IA DelayResp [ns]: 999966520
 Time t1: 1425935696092055440
 FM 3 Port Number: 0
 Time t2: 1425935696092055440
 Time t3: 1425935696304069080
Avg Offset [ns]: 0
 Time t4: 1425935696304069020
 FM 2 Identity: N/A
CF PDelayResp Min [ns]: 0
IA Announce Max [ns]: 1002036460
 PTP Status: SLAVE
 Range Identifier: 10
 DelayResp Messages Received: 112
 PdelayResp FollowUp Messages Received: 0
 Leap59: 0
CF DelayResp Max [ns]: 0
 Leap61: 0
 DelayReq Messages Received Rate: 0
IA FollowUp [ns]: 1000000840
 PdelayRespFollowUp Messages Sent: 0
 Signaling Messages Received: 0
 Interface Identifier: 1400000
CF Sync Max [ns]: 0
 Frequency Traceable: 0
 Signaling Messages Sent: 0
 Master Clock Class: 6
 Current UTC Offset: 0
CF PDelayReq Max [ns]: 0
 FM 3 Identity: N/A
CF PDelayRespFollowUp Max [ns]: 0
CF DelayReq [ns]: 0
IA DelayResp Max [ns]: 1213753600
 Local Clock Accuracy: The time is accurate to within 1 us
 Master Port Identity: aa:bb:cc:ff:fe:00:00:00
 PdelayResp Messages Sent: 0
 Status: Successful
 Sync Messages Received: 4415
 Port Name: Ethernet - 002
 Sync Messages Received Rate: 0
 FM 4 Identity: N/A
CF PDelayResp Max [ns]: 0
 DelayReq Messages Sent: 112
CF DelayResp [ns]: 0
IA Sync Min [ns]: 999166440
 PdelayReq Messages Received: 0
CF Sync [ns]: 0
IA Sync [ns]: 999999640
 Time t1 UTC: 09 March 2015 21:14:56.92055440
row_count: 1

