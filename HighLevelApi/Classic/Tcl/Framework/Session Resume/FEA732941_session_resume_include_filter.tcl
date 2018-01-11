package req Ixia

set res [ixia::connect \
    -config_file {FEA732941_session_resume_include_filter.ixncfg} \
    -ixnetwork_tcl_server localhost \
    -tcl_server localhost \
    -session_resume_include_filter {emulation_bgp_route_config.bgp_sites connect} \
]

proc keylprint {var_ref} {
    upvar 1 $var_ref var
    set level [expr [info level] - 1]
    foreach key [keylkeys var] {
        set indent [string repeat "    " $level]
        puts -nonewline $indent 
        if {[catch {keylkeys var $key}]} {
            puts "$key: [keylget var $key]"
            continue
        } else {
            puts $key
            puts "$indent[string repeat "-" [string length $key]]"
        }
        set rec_key [keylget var $key]
        keylprint rec_key
    }
}

puts stderr "Available keys:"
keylprint res