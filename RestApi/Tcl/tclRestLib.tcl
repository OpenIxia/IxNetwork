proc get {url} {
    # Description
    #    A HTTP GET function to send REST APIs.
    #	
    #Parameters
    #    url: (str): The REST API URL.
    #	
    #Syntax
    #	/api/v1/sessions/1/ixnetwork/operations
    #
    puts "\nGET: $url"
    set header [list Content-type application/json]
    set config [list method get format json headers $header result json]
    set response [::rest::simple $url {} $config]
    #set currentState [dict get $response state]
    return $response
}
    
proc post {url jsonData} {
    #Description
    #	A HTTP POST function to create and start operations.
    #	
    #Parameters
    #	restApi: (str): The REST API URL.
    #	jsonData: (dict): The data payload for the URL.
    #
    #Syntax
    #
    puts "POST: $url"
    puts "DATA: $jsonData"
    set header [list Content-type application/json]
    set config [list method post format json headers $header result json]
    set response [::rest::simple $url {} $config $jsonData]
    #puts "STATUS: [dict get $response state]"
    return $response
}
    
proc patch {url jsonData} {
    #Description
    #	A HTTP PATCH function to modify configurations.
    #	
    #Parameters
    #	url: (str): The REST API URL.
    #	jsonData: (dict): The data payload for the URL.
    #    
    #Syntax
    #
    puts "PATCH: $url"
    puts "DATA: $jsonData"
    set header [list Content-type application/json]
    set config [list method patch format json headers $header]
    set response [::rest::simple $url {} $config $jsonData]
    return $response
}
    
proc startAllProtocols {args} {
    #Description
    #    Start all protocols in NGPF and verify all Device Groups are started.
    #
    #Parameter
    #    sessionUrl: session Url
    #
    #Syntax
    #    POST: /api/v1/sessions/{id}/ixnetwork/operations/startallprotocols
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set argIndex 0
    while {$argIndex < [llength $args]} {
        set currentArg [lindex $args $argIndex]
        switch -exact -- $currentArg {
            -sessionUrl {
                set sessionUrl [lindex $args [expr $argIndex + 1]]
                incr argIndex 2
            }
            default {
                error "$procName: No such parameter: $currentArg"
                # return 1
            }
        }
    }
    set url $sessionUrl/operations/startallprotocols
    set response [post $url {}]
    set id [dict get $response id]
    set url [concat $url/${id}]
    waitForComplete -response $response -url $url
}

proc stopAllProtocols {args} {
    #Description
    #    Stop all protocols in NGPF
    #
    #Parameter
    #    sessionUrl: session Url
    #
    #Syntax
    #    POST: /api/v1/sessions/{id}/ixnetwork/operations/stopallprotocols
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set argIndex 0
    while {$argIndex < [llength $args]} {
        set currentArg [lindex $args $argIndex]
        switch -exact -- $currentArg {
            -sessionUrl {
                set sessionUrl [lindex $args [expr $argIndex + 1]]
                incr argIndex 2
            }
            default {
                error "$procName: No such parameter: $currentArg"
                # return 1
            }
        }
    }
    set url $sessionUrl/operations/stopallprotocols
    set response [post $url {{"arg1":"sync"}}]
    set id [dict get $response id]
    set url [concat $url/${id}]
    waitForComplete -response $response -url $url
}		

proc regenerateTrafficItems {args} {
    #Description
    #    Performs regenerate on Traffic Items.
    #
    #Parameter
    #    trafficItemList: 'all' will automatically regenerate from all Traffic Items.
    #                     Or provide a list of Traffic Items.
    #                     ['/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1', ...]
    #    sessionUrl: session Url
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set trafficItemList "all"
	
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -trafficItemList {
		set trafficItemList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		# return 1
	    }
	}
    }
	
    set url $sessionUrl/traffic/trafficItem
    if {$trafficItemList == "all"} {
	set response [get $url]
	foreach trafficItem $response {
	    set links [dict get $trafficItem links]
	    set links [string range $links 1 end-1]
	    set href [dict get $links href]
	    append trafficItemLists " " \"$href\",
	}
    } else {
	#if {type(trafficItemList) != list} {
        #    trafficItemList = trafficItemList.split(' ')
        #}
    }

    set url $sessionUrl/traffic/trafficItem/operations/generate
    set lst "\"arg1\": \[[string trimright $trafficItemLists ","]\]"
    set body [list $lst]
    puts "Regenerating traffic items: $trafficItemLists"
    set response [post $url $body]
    set id [dict get $response id]
    set url [concat $url/${id}]
    waitForComplete -response $response -url $url
}		

proc applyTraffic {args} {
    #Description
    #    Apply the configured traffic.
    #
    #Parameter
    #    sessionUrl: session Url
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
        set currentArg [lindex $args $argIndex]
        switch -exact -- $currentArg {
            -sessionUrl {
                set sessionUrl [lindex $args [expr $argIndex + 1]]
                incr argIndex 2
            }
            default {
                error "$procName: No such parameter: $currentArg"
                # return 1
            }
        }
    }
    set url $sessionUrl/traffic/operations/apply
    regexp {(.*)api(.*)} $url match ip header
    set restApiHeader [concat '/api' $header]	
    set response [post $url {{"arg1":"/api/v1/sessions/1/ixnetwork/traffic"}}]
    set id [dict get $response id]
    set url [concat $url/${id}]
    waitForComplete -response $response -url $url
}	

proc startTraffic {args} {
    #Description
    #    Start traffic and verify traffic is started.
    #    This function will also give you the option to regenerate and apply traffic.
    #Parameter
    #    regenerateTraffic: <bool>
    #                   
    #    applyTraffic: <bool> 
    #                 In a situation like packet capturing, you cannot apply traffic after
    #                  starting packet capture because this will stop packet capturing. 
    #                  You need to set applyTraffic to False in this case.
    #    blocking: <bool> If True, API server doesn't return until it has
    #                         started traffic and ready for stats.  Unblocking is the opposite.
    #    sessionUrl: session Url
    #
    #Syntax
    #    For blocking state:
    #       POST:  /api/v1/sessions/{id}/ixnetwork/traffic/operations/startstatelesstrafficblocking'
    #       DATA:  {arg1: ['/api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}' ...]}
    #    For non blocking state:
    #       POST: /api/v1/sessions/1/ixnetwork/traffic/operations/start
    #       DATA: {arg1: '/api/v1/sessions/{id}/ixnetwork/traffic'}
    #Requirements:
    #    For non blocking state only:
    #       # You need to check the traffic state before getting stats.
    #       # Note: Use the configElementObj returned by configTrafficItem()
    #        if trafficObj.getTransmissionType(configElementObj) == "fixedFrameCount":
    #           trafficObj.checkTrafficState(expectedState=['stopped', 'stoppedWaitingForStats'], timeout=45)
    #       if trafficObj.getTransmissionType(configElementObj) == "continuous":
    #           trafficObj.checkTrafficState(expectedState=['started', 'startedWaitingForStats'], timeout=45)
    #
    set procName [lindex [info level [info level]] 0]
    set regenerateTraffic "True"
    set applyTraffic "True"
    set blocking "False"
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -regenerateTraffic {
		set regenerateTraffic [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -applyTraffic {
		set applyTraffic [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -blocking {
		set blocking [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		return 1
	    }
	}
    }
    if {$regenerateTraffic == "True"} {
        regenerateTrafficItems -sessionUrl $sessionUrl
    } 
    if {$applyTraffic == "True"} {
        applyTraffic -sessionUrl $sessionUrl
    } 
    
    if {$blocking == "False"} {
	set url $sessionUrl/traffic/operations/start
	set response [post $url {{"arg1":"/api/v1/sessions/1/ixnetwork/traffic"}}]
	set id [dict get $response id]
	set url [concat $url/${id}]
	waitForComplete -response $response -url $url -timeout 120
	
	# Server will go into blocking state until it is ready to accept the next api command.
    }
    if {$blocking == "True"} {
        set enabledTrafficItemList [getAllTrafficItemObjects -getEnabledTrafficItemsOnly "True"]
        set lst "\"arg1\": \[[string trimright $enabledTrafficItemList ","]\]"
	set body [list $lst]
	set url $sessionUrl/traffic/operations/startstatelesstrafficblocking
	set response [post $url {{$lst}}]
	set id [dict get $response id]
	set url [concat $url/${id}]
	waitForComplete -response $response -url $url -timeout 120
    }
}	

proc getAllTrafficItemObjects {args} {
    #Description
    #    Get all the Traffic Item objects.
    #
    #Parameter
    #    getEnabledTrafficItemOnly: <bool>
    #    sessionUrl: session Url
    #
    #Return
    #    A list of Traffic Items
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set getEnabledTrafficItemsOnly "False"
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -getEnabledTrafficItemsOnly {
		set getEnabledTrafficItemsOnly [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		return 1
	    }
	}
    }
	
    set url $sessionUrl/traffic/trafficItem
    set response [get $url]
    foreach trafficItem $response {
	if {$getEnabledTrafficItemsOnly == "True"} {
	    set a [dict get $trafficItem enabled]
	    if {$a == [string tolower "True"]} { 
		set links [dict get $trafficItem links]
		set links [string range $links 1 end-1]
		set href [dict get $links href]
		append trafficItemObjList " " \"$href\",
	    }	
	} else {
	    set links [dict get $trafficItem links]
	    set links [string range $links 1 end-1]
	    set href [dict get $links href]
	    append trafficItemObjList " " \"$href\",
	}
    }
    puts "TrafficItemObjList : $trafficItemObjList"
    return $trafficItemObjList
}		

proc stopTraffic {args} {
    #Description
    #    Stop traffic and verify traffic has stopped.
    #Parameters
    #   blocking: <bool>: True=Synchronous mode. Server will not accept APIs until the process is complete.
    #   sessionUrl: session Url
    #
    #Syntax
    #    For blocking state:
    #       POST: /api/v1/sessions/{id}/ixnetwork/traffic/operations/stopstatelesstrafficblocking
    #       DATA:  {arg1: ['/api/v1/sessions/{id}/ixnetwork/traffic/trafficItem/{id}' ...]}
    #    For non blocking state:
    #       POST: /api/v1/sessions/{id}/ixnetwork/traffic/operations/stop
    #       DATA: {'arg1': '/api/v1/sessions/{id}/ixnetwork/traffic'}
    #
    set procName [lindex [info level [info level]] 0]
    set blocking "False"
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -blocking {
		set blocking [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		# return 1
	    }
	}
    }
    
    if {$blocking == "True"} {
	set enabledTrafficItemList [getAllTrafficItemObjects -getEnabledTrafficItemsOnly "True"]
	set lst "\"arg1\": \[[string trimright $enabledTrafficItemList ","]\]"
	set url $sessionUrl/traffic/operations/stopstatelesstrafficblocking
	set response [post $url {{$lst}}]
	set id [dict get $response id]
	set url [concat $url/${id}]
	waitForComplete -response $response -url $url -timeout 120
    }
    if {$blocking == "False"} {
        set url $sessionUrl/traffic/operations/stop
	set response [post $url {{"arg1":"/api/v1/sessions/1/ixnetwork/traffic"}}]
	set id [dict get $response id]
	set url [concat $url/${id}]
	waitForComplete -response $response -url $url -timeout 120
    }
    
    checkTrafficState -expectedState [list "stopped"] -sessionUrl $sessionUrl
    after 3000
}		

proc checkTrafficState {args} {
    #Description
    #    Check the traffic state for the expected state.
    #    This is best used to verify that traffic has started before calling getting stats.
    #Traffic states are:
    #    startedWaitingForStats, startedWaitingForStreams, started, stopped,
    #    stoppedWaitingForStats, txStopWatchExpected, locked, unapplied
    #Parameters
    #    expectedState: <str>:  Input a list of expected traffic state.
    #                    Example: ['started', startedWaitingForStats'] <-- This will wait until stats has arrived.
    #    timeout: <int>: The amount of seconds you want to wait for the expected traffic state.
    #              Defaults to 45 seconds.
    #              In a situation where you have more than 10 pages of stats, you will
    #              need to increase the timeout time.
    #    ignoreException: <bool>: If True, return 1 as failed, and don't raise an Exception.
    #    sessionUrl: session Url
    #Return
    #    1: If failed.
    #
    set procName [lindex [info level [info level]] 0]
    set timeout 45
    set expectedState [list "stopped"]
    set ignoreException "False"
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -expectedState {
		set expectedState [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -ignoreException {
		set ignoreException [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -timeout {
		set timeout [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		return 1
	    }
	}
    }
    
    #if type(expectedState) != list:
    #    expectedState.split(' ')
    
    puts "checkTrafficState: Expecting state: $expectedState\n"
    set url $sessionUrl/traffic
    for {set counter 1} {$counter < [expr $timeout + 1]} {incr counter} {
	set response [get $url]
	set currentTrafficState [dict get $response state]
	if {$currentTrafficState == "unapplied"} {
            puts "\nCheckTrafficState: Traffic is UNAPPLIED"
            applyTraffic
        }
        puts "\ncheckTrafficState: $currentTrafficState: Expecting: $expectedState"
	puts "\tWaited $counter/$timeout seconds"
	
        if {$counter < $timeout && [lsearch $expectedState $currentTrafficState] == -1} {
            after 1000
	    continue
        }           
        if {$counter < $timeout && [lsearch $expectedState $currentTrafficState] != -1} {
            after 8000
            puts "checkTrafficState: Done\n"
            return 0
        }
        if {$ignoreException == "False"} {
            error "checkTrafficState: Traffic state did not reach the expected state(s): $expectedState"
        } else {
            return 1
	}	
    }
}

proc connectToLinuxIxosChassis {chassisIp username password} {
    #Description
    #   Connect to a Linux Ixos Chassis.
    #   
    #Parameters
    #   chassisIp: (str): The Linux Ixos Chassis IP address.
    #   username: (str): Login username. 
    #   password: (str): Login password.
    #   
    #Syntax
    #	POST: /api/v1/auth/session
    #
    set url "https://$chassisIp/platform/api/v1/auth/session"
    set body [list {"username": $username, "password": $password}]
    set response [post $url $body]	
    set apiKey [dict get $response apiKey]

    # userAccountUrl: https://{ip}/platform/api/v1/auth/users/{id}
    set userSessionId [dict get $response userAccountUrl]

    set ixosHeader  "https://$chassisIp/chassis/api/v2/ixos"
    set diagnosticsHeader "https://$chassisIp/chassis/api/v1/diagnostics"
    set authenticationHeader "https://$chassisIp/chassis/api/v1/auth"
    set sessionUrl $ixosHeader
}

proc createWindowsSession {ixNetRestServerIp {ixNetRestServerPort '11009'} serverOs} {
    #Description
    #   Connect to a Windows IxNetwork API Server to create a session URL. This is
    #   for both Windows and Windows server with IxNetwork Connection Manager.
    #   This will set up the session URL to use throughout the test.
    #   
    #Parameter
    #  ixNetRestServerIp: (str): The Windows IxNetwork API Server IP address.
    #  ixNetRestServerPort: (str): Default: 11009.  Provide a port number to connect to.
    #					   On a Linux API Server, a socket port is not needed. State "None".
    # Handle __import__(IxNetRestApi) to not error out
    #
    if {$ixNetRestServerIp == "None"} {
	return
    }
    
    set url "http://$ixNetRestServerIp:$ixNetRestServerPort/api/v1/sessions"
    set serverAndPort "$ixNetRestServerIp:$ixNetRestServerPort"
 
    if {$serverOs == "windowsConnectionMgr"} {
	# For Connection Manager, requires a POST to automatically get the next session.
	# {'links': [{'href': '/api/v1/sessions/8020', 'method': 'GET', 'rel': 'self'}]}
	puts "Please wait while IxNetwork Connection Mgr starts up an IxNetwork session..."
	set response [post $url {}]
	
	set counterStop 10
	set url [concat $url/$sessionIdNumber ]
	for {set counter 1} {$counter <= $counterStop} {incr counter} {
	    set response [get $url]
	    set currentState [dict get $response state]
	    
	    puts "\n\tNew Windows session current state: $currentState"
	    
	    if {$currentState != "ACTIVE" && $counter < $counterStop} {
		puts "\tWaiting $counter/$counterStop seconds"
		after 1000
	    }
	    if {$currentState != "ACTIVE" && $counter == $counterStop} {
		error "\nNew Windows session state failed to become ACTVIE state"
	    }
	    if {$currentState == "ACTIVE" && $counter < $counterStop} {
		break
	    }
	}
	# Windows connection mgr takes additional time after becoming ACTIVE.
	puts "\tWait for Windows session to become ready"
	after 20000
    }
    if {$serverOs == "windows"} {
	# windows sessionId is always 1 because it only supports one session.
	set sessionIdNumber 1
    }
    
    set sessionUrl "http://$ixNetRestServerIp:$ixNetRestServerPort/api/v1/sessions/$sessionIdNumber/ixnetwork"
    # http://192.168.70.127:11009
    set match [regexp "(.*)/api.*" $sessionUrl m header]
    set httpHeader $header
    
    # http://192.168.70.127:11009/api/v1/sessions/1
    set match [regexp "(.*)/ixnetwork.*" $sessionUrl m id]
    set sessionId $id
    set apiSessionId "/api/v1/sessions/$sessionIdNumber/ixnetwork"
    
    # Verify the API server IP and port connection.
    puts "Verifying API server connection..."
    set response [get $sessionId]
    return $sessionUrl
}

proc linuxServerWaitForSuccess {url {timeout 120}} {
    #Description
    #   Wait for a success completion on the Linux API server.
    #   
    #Paramters
    #   url: (str): The URL's ID of the operation to verify.
    #   timeout: (int): The timeout value.
    #
    puts "linuxServerWaitForSuccess"
    
    for {set counter 1} {$counter <= $timeout} {incr $counter} {
	set response [get $url {{"applicationType": "ixnrest"}}]
	set currentStatus [dict get $response message]
	puts "\tCurrentStatus: $currentStatus:  $counter/$timeout seconds"
	if {$counter < $timeout && $currentStatus != "Operation successfully completed"} {
	    after 1000
	}
	if {$counter == $timeout && $currentStatus != "Operation successfully completed"} {
	    return 1
	}
	if {$counter < $timeout && $currentStatus == "Operation successfully completed"} {
	    return 0
	}
    }
}
				
proc connectToLinuxApiServer {linuxServerIp linuxServerIpPort {apiKey None} {username 'admin'} {password 'admin'} {verifySslCert False}} {
    #Description
    #   Connect to a Linux API server.
    #   
    #Parameters
    #   linuxServerIp: (str): The Linux API server IP address.
    #   username: (str): Login username. Default = admin.
    #   password: (str): Login password. Default = admin.
    #   verifySslCert: (str): Defalt: None.  The SSL Certificate for secure access verification.
    #   
    #Syntax
    #	POST: /api/v1/auth/session
    #
    set query []

    if {$apiKey == "None"} {
	# 1: Connect to the Linux API server
	set url "https://$linuxServerIp:$linuxServerIpPort/api/v1/auth/session"
	puts "connectToLinuxApiServer: $url"
	# response = self.post(url, data={'username': username, 'password': password}, ignoreError=True)		
	set body [list {"username": $username, "password": $password}]
	set response [post $url $body]	
	
	# if not str(response.status_code).startswith('2'):
	# raise IxNetRestApiException('\nLogin username/password failed\n')
	set apiKey  [dict get $response apiKey]
	set url "https://$linuxServerIp:$linuxServerIpPort/api/v1/sessions"
	
	if {$webQuickTest == False} {
	    set data {"applicationType" : "ixnrest"}
	}
	if {$webQuickTest == True} {
	    set data {"applicationType" : "ixnetwork"}
	}
	set body [list $data]
	set response [post $url $body]	
	# self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}
	puts "linuxServerCreateSession"
	# response = self.post(url, data=data, headers=self.jsonHeader)
	
	set sessionIdNumber [dict get $response id]
	set url [concat $url/$sessionIdNumber]
	set response [get $url]		
	# response = self.get(url+'/'+str(self.sessionIdNumber))
	
	# https://192.168.70.108/ixnetworkweb/api/v1/sessions/7
	# self.sessionId = response.json()['links'][0]['href']
	set links [dict get $response links]
	set links [string range $links 1 end-1]
	set sessionId [dict get $links href]
	# Remove the redirect /ixnetworkweb from the URL. IxNetwork 8.50 will resolve this.
	set sessionId [regsub 'ixnetworkweb/' $sessionId  '')]
        # self.sessionId = self.sessionId.replace('ixnetworkweb/', '')
    
        # https://10.10.10.1:443
        set matchHeader [regexp {(https://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?))} $sessionId m header]
        set httpHeader header

        if {![regexp ":" $httpHeader } {
            set httpHeader [concat $httpHeader/$linuxServerIpPort]
	}
        set sessionUrl [concat $sessionId/ixnetwork]
    
        # /api/v1/sessions/4/ixnetwork
	set match [regexp ".*(/api.*)" $sessionId m id]
	set apiSessionId [concat $id/ixnetwork]
    
	# 3: Start the new session
	set url [concat $sessionId/operations/start]
	set response [post $url {}]		
	# response = self.post(self.sessionId+'/operations/start')
	set url [dict get $response url]
	if {linuxServerWaitForSuccess $url 60 == 1} {
	    error "IxNetRestApiException"
	}
	if {$webQuickTest == True} {
	    set sessionId "https://$linuxServerIp/ixnetworkweb/api/v1/sessions/$sessionIdNumber"
	    set sessionUrl "https://$linuxServerIp/ixnetworkweb/api/v1/sessions/$sessionIdNumber/ixnetwork"
	    set match [regexp ".*('/api')" $sessionUrl m header]
	    set httpHeader $header
	}
    }
    # If an API-Key is provided, then verify the session ID connection.
    if {$apiKey != "None"} {
	set sessionId "https://$linuxServerIp/ixnetworkweb/api/v1/sessions/$sessionIdNumber"
	set response [get $sessionId]
	# self.get(self.sessionId)
    }
}
		
proc configLicenseServerDetails {{licenseServer "None"} {licenseMode "None"} {licenseTier "None"} sessionUrl} {
    #Description
    #   Configure license server details: license server IP, license mode and license tier.
    #   
    #Parameters
    #   licenseServer: (str): License server IP address(s) in a list.
    #   licenseMode: (str): subscription | perpetual | mixed
    #   licenseTier: (str): tier1 | tier2 | tier3 ...
    #   sessionUrl : session url
    #
    #Syntax
    #   PATCH: /api/v1/sessions/{id}/ixnetwork/globals/licensing
    #
    # Each new session requires configuring the new session's license details.
    set data {}
    if {$licenseServer != "None"} {
	# data.update({'licensingServers': licenseServer})
	dict update $data {'licensingServers' : $licenseServer}
    }
    if {$licenseMode !="None"} {
	# data.update({'mode': licenseMode})
	dict update $data {'mode' : $licenseMode}
    }
    if {$licenseTier !="None"} {
	# data.update({'tier': licenseTier})
	dict update $data {'tier' : $licenseTier}
    }
    set url [concat $sessionUrl/globals/licensing']
    set body [list $data]
    set response [patch $url $body]
    # response = self.patch(self.sessionUrl+'/globals/licensing', data=data)
    showLicenseDetails $sessionUrl
}

proc showLicenseDetails {sessionUrl} {
    #Description
    #   Display the new session's license details.
    #
    #Parameter
    #   sessionUrl: session Url
    #
    #Syntax
    #	GET: /api/v1/sessions/{id}/globals/licensing
    #
    set url [concat $sessionUrl/globals/licensing']
    set response [get $url]
    # response = self.get(self.sessionUrl+'/globals/licensing')
    puts "\nVerifying sessionId license server: $sessionUrl"
    puts "\t dict get response licensingServers"
    puts "\t dict get response mode"
    puts "\t dict get response tier"
}

proc connect {args} {
    #Description
    #   Initializing default parameters and making a connection to the API server
    #   
    #Notes
    #	Starting IxNetwork 8.50, https will be enforced even for Windows connection.
    #	If you still want to use http, you need to add -restInsecure to the IxNetwork.exe appliaction under "target".
    #	
    #Examples
    #	Right click on "IxNetwork API server", select properties and under target
    #	ixnetwork.exe -restInsecure -restPort 11009 -restOnAllInterfaces -tclPort 8009
    #	
    #Parameters
    #   apiServerIp: (str): The API server IP address.
    #   serverIpPort: (str): The API server IP address socket port.
    #   serverOs: (str): windows|windowsConnectionMgr|linux
    #   connectToLinuxChassis: (str): Connect to a Linux OS chassis IP address.
    #   webQuickTest: (bool): True: Using IxNetwork Web Quick Test. Otherwise, using IxNetwork.
    #   includeDebugTraceback: (bool):
    #						   True: Traceback messsages are included in raised exceptions.
    #						   False: No traceback.  Less verbose for debugging.
    #   username: (str): The login username. For Linux API server only.
    #   password: (str): The login password. For Linux API server only.
    #   licenseServerIp: (str): The license server IP address.
    #   licenseMode: (str): subscription | perpetual | mixed
    #   licenseTier: (str): tier1 | tier2 | tier3
    #   deleteSessionAfterTest: (bool): True: Delete the session.
    #								   False: Don't delete the session.
    #   verifySslCert: (str): Optional: Include your SSL certificate for added security.
    #   serverOs: (str): Defaults to windows. windows|windowsConnectionMgr|linux.
    #   includeDebugTraceback: (bool): True: Include tracebacks in raised exceptions.
    #   sessionId: (str): The session ID on the Linux API server or Windows Connection Mgr to connect to.
    #   apiKey: (str): The Linux API server user account API-Key to use for the sessionId connection.
    #   generateLogFile: True|False|<log file name>.  If you want to generate a log file, provide
    #						the log file name.
    #						True = Then the log file default name is ixNetRestApi_debugLog.txt
    #						False = Disable generating a log file.
    #						<log file name> = The full path + file name of the log file to create.
    #  robotFrameworkStdout: (bool):  True = Print to stdout.
    #   httpInsecure: (bool): This parameter is only for Windows connections.
    #							 True: Using http.  False: Using https.
    #							 Starting 8.50: IxNetwork defaults to use https.
    #							 If you are using versions prior to 8.50, it needs to be a http connection.
    #							 In this case, set httpInsecure=True.
    #
    #Examples:
    #   Steps to connect to Linux API server steps:
    #	   1> POST: https://$apiServerIp/api/v1/auth/session
    #		  DATA: {"username": "admin", "password": "admin"}
    #		  HEADERS: {"content-type": "application/json"}
    #	   2> POST: https://$apiServerIp:$port/api/v1/sessions
    #		  DATA: {"applicationType": "ixnrest"}
    #		  HEADERS: {"content-type": "application/json", "x-api-key": "d9f4da46f3c142f48dddfa464788hgee"}
    #	   3> POST: https://$apiServerIp:443/api/v1/sessions/4/operations/start
    #		  DATA: {}
    #		  HEADERS: {"content-type": "application/json", "x-api-key": "d9f4da46f3c142f48dddfa464788hgee"}
    #	   sessionId = https://$apiServerIp:443/api/v1/sessions/$id
    #	   
    #   Steps to connect to Linux Web Quick Test:
    #	   1> POST: https://$apiServerIp:443/api/v1/auth/session
    #		  DATA: {"username": "admin", "password": "admin"}
    #		  HEADERS: {"content-type": "application/json"}
    #	   2> POST: https://$apiServeIp:443/api/v1/sessions
    #		  DATA: {"applicationType": "ixnetwork"}
    #	   3> POST: https://$apiServerIp:443/api/v1/sessions/2/operations/start
    #		  DATA: {"applicationType": "ixnetwork"}
    #	sessionId = https://$apiServerIp/ixnetworkweb/api/v1/sessions/$id
    #	
    #   Notes
    #	  To connect to an existing configuration.
    #		 Windows: Nothing special to include. The session ID is always "1".
    #		 Linux API server: Include the api-key and sessionId that you want to connect to.
    #		 Windows Connection Manager: Include just the sessionId: For example: 8021.
    #
    set debugLogFile None
    set enableDebugLogFile False
    set apiServerIp None
    set serverIpPort "11009"
    set apiServerPort None
    set linuxApiServerIp None
    set serverOs "windows"
    set connectToLinuxChassisIp None	
    set webQuickTest False
    set username None
    set password "admin"
    set licenseServerIp None
    set licenseMode None
    set licenseTier None
    set deleteSessionAfterTest True
    set verifySslCert False
    set includeDebugTraceback True
    set sessionId None
    set apiKey None
    set generateLogFile True
    set robotFrameworkStdout False
    set query []
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -apiServerIp {
		set apiServerIp [lindex $args [expr $argIndex + 1]]
		set linuxApiServerIp $apiServerIp
		incr argIndex 2			
	    }
	    -serverIpPort {
		set serverIpPort [lindex $args [expr $argIndex + 1]]				
		set apiServerPort $serverIpPort
		incr argIndex 2			
	    }
	    -serverOs {
		set serverOs [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -connectToLinuxChassisIp {
		set connectToLinuxChassisIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -webQuickTest {
		set webQuickTest [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -username {
		set username [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -password {
		set password [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -licenseServerIp {
		set licenseServerIp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -licenseMode {
		set licenseMode [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -licenseTier {
		set licenseTier [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -deleteSessionAfterTest {
		set deleteSessionAfterTest [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -verifySslCert {
		set verifySslCert [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -includeDebugTraceback {
		set includeDebugTraceback [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionId {
		set sessionId [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -apiKey {
		set apiKey [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -generateLogFile {
		set generateLogFile [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -robotFrameworkStdout {
		set robotFrameworkStdout [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		# return 1
	    }
	}
    }
    if {$generateLogFile} {
	if {$generateLogFile == True} {
	    # Default the log file name
	    set restLogFile "ixNetRestApi_debugLog.txt"
	    set enableDebugLogFile True
	    set debugLogFile restLogFile
	}
	if {$generateLogFile != True && $generateLogFile != False} {
	    set restLogFile $generateLogFile
	}
	# Instantiate a new log file here.
	set LogFile [open $restLogFile w]
	set timestamp [clock seconds]		
	puts $LogFile "Timestamp : [clock format $timestamp -format "%D: %H:%M:%S"]"
	close $LogFile
    }
    # Make Robot print to stdout
    if {$robotFrameworkStdout} {
	#from robot.libraries.BuiltIn import _Misc
	#self.robotStdout = _Misc()
    }
    if {$connectToLinuxChassisIp != "None"} {
	connectToLinuxIxosChassis $connectToLinuxChassisIp $username $password
	return
    }
    if {$serverOs == "windows"} {
	set sessionUrl [createWindowsSession $apiServerIp $serverIpPort $serverOs]
    }
    if {$serverOs == "windowsConnectionMgr"} {
	# User connecting to existing sessionId
	if {$sessionId} {
	    set sessionId "http://$apiServerIp:$serverIpPort/api/v1/sessions/$sessionId"
	    set sessionUrl "http://$apiServerIp:$serverIpPort/api/v1/sessions/$sessionId/ixnetwork"
	    set apiSessionId "/api/v1/sessions/$sessionId/ixnetwork"
	    set match [regexp "(.*)/api.*" $sessionUrl m header]
	    set httpHeader $header			
	} else {
	    # Create a new session
	    set sessionUrl [createWindowsSession $apiServerIp $serverIpPort $serverOs]
	}
    }
    if {$serverOs == "linux"} {
	if {$apiServerPort == "None"} {
	    set apiServerPort 443
	}		
	if {$apiKey != "None" && $sessionId == "None"} {
	    error "Providing an apiKey must also provide a sessionId."
	}		
	# Connect to an existing session on the Linux API server
	if {$apiKey != "None" && $sessionId != "None"} {
	    set sessionIdUrl "http://$linuxApiServerIp:$apiServerPort/api/v1/sessions/$sessionId"
	    set sessionUrl [concat $sessionId/ixnetwork]
	    # set match [regexp "(.*)/ixnetworkweb.*" $sessionUrl m header]
	    # set httpHeader $header
	    set httpHeader "http://$linuxApiServerIp:$apiServerPort"
	    
	    # set jsonHeader {"content-type": "application/json", "x-api-key": $apiKey}
	    set url "http://$linuxApiServerIp:$apiServerPort/api/v1/sessions/$sessionId"
	    set response [get $url]
	    #puts $response
	    # response = get("https://{0}:{1}/api/v1/sessions/{2}".format(linuxApiServerIp, apiServerPort, str(sessionId)))
	    
	    if {$webQuickTest == False} {
		# https://192.168.70.108/ixnetworkweb/api/v1/sessions/4
		# set sessionId [dict get $response ["links"][0]["href"]]
		set links [dict get $response links]
		set links [string range $links 1 end-1]
		set sessionIdUrl [dict get $links href]
		# Remove the redirect /ixnetworkweb from the URL. IxNetwork 8.50 will resolve this.
		set sessionIdUrl [regsub "ixnetworkweb/" $sessionIdUrl ""]

		# https://192.168.70.108/ixnetworkweb/api/v1/sessions/4/ixnetork
		set sessionUrl [concat $sessionIdUrl/ixnetwork]
		
		# /api/v1/sessions/4/ixnetwork
		# match = re.match(".*(/api.*)", sessionId)
		# apiSessionId = match.group(1) + "/ixnetwork"
		set match [regexp ".*(/api.*)" $sessionIdUrl m api]
		set apiSessionId [concat $api/ixnetwork]
		# https://10.10.10.1:443
		set matchHeader [regexp {(https://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?)} $sessionIdUrl m http]
		set httpHeader $http
	    }
	    if {$webQuickTest == True} {
		set sessionIdUrl "http://$linuxApiServerIp:$apiServerPort/ixnetwork/api/v1/sessions/$sessionId"
		set sessionUrl $sessionIdUrl
		set match [regexp "(.*)/ixnetworkweb.*" $sessionUrl m header]
		set httpHeader $header
	    }
	}
	# Create new session: connectToLinuxApiServer API knows whether to create a new session or connect to an existing
	#                     session by looking at the self.apiKey.
	if {$apiKey == "None" && $sessionId == "None"} {
    puts "muru: coming inside"
	    connectToLinuxApiServer $linuxApiServerIp $apiServerPort
	}
	if {$licenseServerIp || $licenseMode || $licenseTier} {
	    configLicenseServerDetails $licenseServerIp $licenseMode $licenseTier $sessionUrl
	}
    }
    # For Linux API Server and Windoww Connection Mgr only: Delete the session when script is done if deleteSessionAfterTest = True.
    # set deleteSessionAfterTest deleteSessionAfterTest
    
    # set match [regexp {http.*(/api.*/sessions/[0-9]+)/ixnetwork} $sessionUrl m session]
    # set headlessSessionId $session
    
    if {$includeDebugTraceback == False} {
	set sys.tracebacklimit 0
    }
    return $sessionUrl
}

proc importJsonConfigFile {args} {
    #Description
    #    To import a JSON config file to IxNetwork.
    #    You could state it to import as a modified config or creating a new config.
    #    The benefit of importing an actual JSON config file is so you could manually use
    #    IxNetwork Resource Manager to edit any part of the JSON config and add to the
    #    current configuration
    #Parameters
    #    jsonFileName: (json object): The JSON config file. Could include absolute path also.
    #    option: (str): newConfig|modify
    #    sessionUrl : session url
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set option "modify"

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -jsonFileName {
		set jsonFileName [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -option {
		set option [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
		# return 1
	    }
	}
    }
    
    if {$option == "modify"} {
        set arg3 "False"
    }	
    if {$option == "newConfig"} {
        set arg3 "True"
    }	
    
    # 1> Read the config file
    puts "Reading saved config file"
    set fp [open $jsonFileName r]
    set configContents [read $fp]
    #fileName = jsonFileName.split('/')[-1]

    # 2> Upload it to the server and give it any name you want for the filename
    #if self.ixnObj.serverOs == 'linux':
    #    octetStreamHeader = {'content-type': 'application/octet-stream', 'x-api-key': self.ixnObj.apiKey}
    #else:
    #    octetStreamHeader = self.ixnObj.jsonHeader
    
    set uploadFile [concat $sessionUrl/files?filename=$jsonFileName]
    puts "Uploading file to server: $uploadFile"
    set response [post $uploadFile $configContents]
    
    # 3> Tell IxNetwork to import the JSON config file
    set lst "\"arg1\": \"/api/v1/sessions/1/ixnetwork/resourceManager\", \"arg2\": \"$jsonFileName\",  \"arg3\": \"$arg3\""
    set body [list $lst]
    set url [concat $sessionUrl/resourceManager/operations/importconfigfile]
    set response [post $url $body]
    set id [dict get $response id]
    set url [concat $url/${id}]
    waitForComplete -response $response -url $url -timeout 300
}

proc waitForComplete {args} {
    #Description
    #   Wait for an operation progress to complete.
    #   
    #Parameters
    #   response: (json response/dict): The POST action response.  Generally, after an /operations action.
    #				 Such as /operations/startallprotocols, /operations/assignports.
    #				 
    #   silentMode: (bool):  If True, display info messages on stdout.
    #   
    #   ignoreException: (bool): ignoreException is for assignPorts.  Don't want to exit test.
    #					Verify port connectionStatus for: License Failed and Version Mismatch to report problem immediately.
    #					
    #   timeout: (int): The time allowed to wait for success completion in seconds.
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set response ""
    set url "" 
    set silentMode False 
    set ignoreException False
    set timeout 90
    
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]		
	switch -exact -- $currentArg {
	    -response {
		set response [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -url {
		set url [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -silentMode {
		set silentMode [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ignoreException {
		set ignoreException [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -timeout {
		set timeout [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		error "\n$procName: No such parameter: $currentArg"
	    }
	}
    }
    set state [dict get $response state]
    if {$silentMode == "False"} {
	puts "\n$procName:\tState: $state"
    }
    
    if {$response == []} {
	error "\n$procName: response is empty"
    }
    if {$response == "" || $state == "SUCCESS"} {
	return $response
    }
    if {$state == "ERROR" || $state=="EXCEPTION"} {
	error "\n$procName: STATE= $state :$response"
    }
    for {set counter 1} {$counter < [expr $timeout + 1]} {incr counter} {
	set response [get $url]
	set state [dict get $response state]
	if {$silentMode == "False"} {
	    if {$state != "SUCCESS"} {
		puts "\tState: $state: Wait {$counter}/{$timeout} seconds"
	    }
	    if {$state == "SUCCESS"} {
		puts "\tState: $state"
	    }
	}
	if {$counter < $timeout && ($state == "IN_PROGRESS" || $state == "down")} {
	    after 1000
	    continue
	}
	if {$counter < $timeout && ($state == "ERROR" || $state == "EXCEPTION")} {
	    # ignoreException is for assignPorts.  Don't want to exit test.
	    # Verify port connectionStatus for: License Failed and Version Mismatch to report problem immediately.
	    if {$ignoreException} {
		return $response
	    }
	    error "\n$procName : State is Error or Exception : $response"
	}	
	if {$counter < $timeout && $state == "SUCCESS"} {
	    return $response
	}
	
	if {$counter == $timeout && $state != "SUCCESS"} {
	    if {$ignoreException} {
		return $response
	    }
	    error "\n $procName : waitForComplete failed"
	}
    }
}

proc getStats {args} {
    #Description
    #	Get stats by the statistic name or get stats by providing a view object handle.
    #	
    #Parameters
    #	csvFile = None or <filename.csv>.
    #			  None will not create a CSV file.
    #			  Provide a <filename>.csv to record all stats to a CSV file.
    #			  Example: getStats(sessionUrl, csvFile='Flow_Statistics.csv')
    #			  
    #	csvEnableFileTimestamp = True or False. If True, timestamp will be appended to the filename.
    #	
    #	displayStats: True or False. True=Display stats.
    #	
    #	ignoreError: True or False.  Returns None if viewName is not found.
    #	
    #	viewObject: The view object: http://{apiServerIp:port}/api/v1/sessions/2/ixnetwork/statistics/view/13
    #				A view object handle could be obtained by calling getViewObject().
    #				
    #	viewName options (Not case sensitive):
    #	   NOTE: Not all statistics are listed here.
    #		  You could get the statistic viewName directly from the IxNetwork GUI in the statistics.
    #		  
    #	'Port Statistics'
    #	'Tx-Rx Frame Rate Statistics'
    #	'Port CPU Statistics'
    #	'Global Protocol Statistics'
    #	'Protocols Summary'
    #	'Port Summary'
    #	'BGP Peer Per Port'
    #	'OSPFv2-RTR Drill Down'
    #	'OSPFv2-RTR Per Port'
    #	'IPv4 Drill Down'
    #	'L2-L3 Test Summary Statistics'
    #	'Flow Statistics'
    #	'Traffic Item Statistics'
    #	'IGMP Host Drill Down'
    #	'IGMP Host Per Port'
    #	'IPv6 Drill Down'
    #	'MLD Host Drill Down'
    #	'MLD Host Per Port'
    #	'PIMv6 IF Drill Down'
    #	'PIMv6 IF Per Port'
    #	'Flow View'
    #	
    # Note: Not all of the viewNames are listed here. You have to get the exact names from
    #	   the IxNetwork GUI in statistics based on your protocol(s).
    #	   
    # Return a dictionary of all the stats: statDict[rowNumber][columnName] == statValue
    #   Get stats on row 2 for 'Tx Frames' = statDict[2]['Tx Frames']
    #
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set viewName "Flow Statistics"	
    set viewObject None
    set csvFile None
    set csvEnableFileTimestamp False
    set displayStats True
    set silentMode True
    set ignoreError False
	
    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -viewName {
		set viewName [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -viewObject {
		set viewObject [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -csvFile {
		set csvFile [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -csvEnableFileTimestamp {
		set csvEnableFileTimestamp [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -displayStats {
		set displayStats [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -silentMode {
		set silentMode [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -ignoreError {
		set ignoreError [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
	    }
	}
    }
	
    if {$viewObject == "None"} {
	set url [concat $sessionUrl/statistics/view]		 
	set response [get $url]
	set views {}
	foreach result $response {
	    set val $result
	    set id [dict get $val id]
	    set views [lappend views [concat $sessionUrl/statistics/view/$id]]			
	}
		 
	if {$silentMode == "False"} {
	    puts "\n$procName: Searching for viewObj for viewName: $viewName"
	}
	
	foreach view $views {
	    set response [get $view]
	    set caption [dict get $response caption]
	    set captionMatch [regexp -nocase ($viewName) $caption]
	    if {$captionMatch} {			
		# viewObj: sessionUrl + /statistics/view/11'
		set viewObject $view
		#puts "\nviewObject :$viewObject"
		break
	    }
	}				
	
	if {$viewObject == "None" && $ignoreError == False} {
	    error "\n$procName : viewObj wasn't found for viewName: $viewName"
	}		
	if {$viewObject == "None" && $ignoreError == True} {
	    return None
	}
    }
    
    if {$silentMode == "False"} {
	#puts "\nviewObj: $viewObject"
    }

    for {set counter 0} {$counter <= 30} {incr counter} {
	set url [concat $viewObject/page]
	set response [get $url]
	set totalPages [dict get $response totalPages]
	if {$totalPages == "null"} {
	    puts "\nGetting total pages is not ready yet. Waiting $counter/30 seconds"
	    after 1000
	}
	if {$totalPages != "null"} {
	    break
	}
	if {$totalPages == "null" && $counter == 30} {
	    puts "\n$procName failed: Getting total pages"
	    return 1
	}			
    }
    #Muru: not verified CSV code 
    if {$csvFile != "None"} {
	package require csv
	package require struct::matrix
	set csvFileName [regsub ' ' $csvFile  '_')]
    if {$csvEnableFileTimestamp} {
	set timestamp [clock seconds]
	set match [regexp {(.)} $csvFileName]
	if {$match} {
	    set csvFileTemp [split csvFileName '.']
	    set csvFileNameTemp [lindex $csvFileTemp 0]
	    set csvFileNameExtension [lindex $csvFileTemp 1]
	    set csvFileName [concat $csvFileNameTemp'_'$timestamp'.'$csvFileNameExtension]			
	} else {
	    set csvFileName [concat $csvFileName'_'$timestamp]
	}
    }
    set csvFile [open $csvFileName w)]
    set csvWriteObj csv.writer(csvFile)
    }

    # Get the stat column names
    set columnList [dict get $response columnCaptions]
    if {$csvFile != "None"} {
        csvWriteObj.writerow(columnList)
    }

    set flowNumber 1
    set statDict {}
    # Get the stat values
    foreach pageNumber $totalPages {
        set url [concat $viewObject/page]
        set response [get $url]
	set statValueList [dict get $response pageValues]
	foreach statValue $statValueList {
	    if {$csvFile != "None"} {
		csvWriteObj.writerow(statValue[0])
	    }
	    if {$displayStats} {
		puts "\nRow: $flowNumber"
	    }
	    dict set statDict $flowNumber {}
	    set index 0
	    puts "$statValue"
	    foreach value [lindex $statValue 0] {
		set statName [lindex $columnList $index]
		dict set statDict $flowNumber $statName $value
		if {$displayStats} {
		    puts "\t $statName: $value"
		}
		set index [expr $index + 1]
	    }				
	    set flowNumber [expr $flowNumber + 1]
	}			
    }		

    if {$csvFile != "None"} {
        close $csvFile
    }
    puts "\n"
    return $statDict
}

proc verifyForDuplicatePorts {portList} {
    # Description
    # 	Verify if the portList has any duplicate ports.
    #
    # Raise an exception if true.
    # 
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    
    set duplicatePorts {}
    foreach list $portList {
	set len [llength [lsearch -all $portList $list]]
	if {$len > 1} {
	    lappend duplicatePorts $list
	}
    }
    if {$duplicatePorts != {}} {
	set duplicatePorts [lsort -unique $duplicatePorts]
	error "\n$procName : Your portList has duplicate ports - $duplicatePorts"
    }
}

proc getVportFromPortList {portList sessionUrl} {	
    # Description
    # 	Get a list of vports from the specified portList.
    # 
    # Parameter
    # 	portList: <list>: Format: [[ixChassisIp, cardNumber1, portNumber1], [ixChassisIp, cardNumber1, portNumber2]]
    #   sessionUrl : session url
    #
    # Return
    # 	A list of vports.
    # 	[] if vportList is empty.
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set vportList []
 
    foreach eachPort $portList {
	set chassisIp [lindex [split [lindex [lindex $eachPort 0] 0] ","] 0]
	set card [lindex [split [lindex [lindex $eachPort 0] 1] ","] 1]
	set portNum [lindex [split [lindex [lindex $eachPort 0] 2] ","] 2]
	set port [concat $chassisIp:$card:$portNum]
	# {'href': '/api/v1/sessions/1/ixnetwork/',
	# 'vport': [{'id': 2, 'href': '/api/v1/sessions/1/ixnetwork/vport/2', 'assignedTo': '10.10.10.8:1:2'}]}
	set query [list [concat {"from": "/",} {"nodes":} \[[list "\"node\": \"vport\", \"properties\": \[\"assignedTo\"\],
                                \"where\": \[[list [concat \"property\": \"assignedTo\", \"regex\": \"$port\"]]\]"]\]]]
        set body [list [concat \"selects\": $query]]
	set url [concat $sessionUrl/operations/query]
	#puts "\nurl : $url"	
	set response [post $url $body]
	#puts "\nresponse : $response"
	set id [dict get $response id]
	set url [concat $url/${id}]
	#puts "\nurl : $url"
	set response [waitForComplete -response $response -url $url]
	
	set result [dict get $response result]
	set result [string range $result 1 end-1]
	set vport [dict get $result vport]
	
	if {$vport == []} {
	    error "\n$procName: The port has no vport and not assigned. Check for port typo: $port"
	}
	if {$vport != []} {
	    # Appending vportList: ['/api/v1/sessions/1/ixnetwork/vport/1', '/api/v1/sessions/1/ixnetwork/vport/2']
	    # vportList.append(vport[0]['href'])
	    set vport [string range $vport 1 end-1]
	    set href [dict get $result href]
	    lappend vportList $href
	}
    }
    return $vportList
}

proc resetPortCpu {{vportList None} {portList None} {timeout 90} sessionUrl} {
    # Description
    # 	Reset/Reboot ports CPU.
    #	Must call IxNetRestApi.py waitForComplete() afterwards to verify port state
    # 
    # Parameter
    # 	vportList: <list>: A list of one or more vports to reset.
    # 	sessionUrl : session url
	
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set url [concat $sessionUrl/vport/operations/resetportcpu]
    #puts "\nurl : $url"
    if {$vportList == "None"} {
	set vportList [list getVportFromPortList $portList]
    }
    set data \"arg1\": \"$vportList\"
    set body [list $data]
    set response [post $url $body]
    #puts "\nresponse : $response"	
    set id [dict get $response id]
    set url [concat $url/${id}]
    #puts "\nurl : $url"
    waitForComplete -response $response -url $url
}

proc verifyPortState {{timeout 70} sessionUrl} {	
    # Description
    # 	Verify port states for all the vports connected to physical ports.
    #	
    # Parameter
    # 	timeout: <int>: The timeout value to declare as failed. Default=70 seconds.
    # 	sessionUrl : session url
    #
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"
    set url [concat $sessionUrl/vport]
    #puts "\nurl : $url"
    set response [get $url]
    foreach value $response {
    	set links [dict get $value links]
	set links [string range $links 1 end-1]
	set href [dict get $links href]
	lappend vportList $href		
    }
    # vportList = [metaDatas["links"][0]['href'] for metaDatas in response.json()]
    set match [regexp "(.*)/api.*" $sessionUrl m header]
    set httpHeader $header	
    foreach eachVport $vportList {
    	for {set counter 1} {$counter <= $timeout} {incr $counter} {		
	    set url [concat $httpHeader$eachVport?includes=state,connectionStatus]
	    #puts "\nurl : $url"
	    set stateResponse [get $url]
	    # stateResponse = self.ixnObj.get(self.ixnObj.httpHeader+eachVport+'?includes=state,connectionStatus', silentMode=True)
	    set url [concat $httpHeader$eachVport?includes=assignedTo]
	    #puts "\nurl : $url"
	    set assignedToResponse [::rest::simple $url $query $args]
	    # assignedToResponse = self.ixnObj.get(self.ixnObj.httpHeader+eachVport+'?includes=assignedTo', silentMode=True)
			
	    if {"Port Released" == [dict get $stateResponse connectionStatus] } {
		error "\n$procName : [dict get $stateResponse connectionStatus]"
	    }
	    if {[dict get $stateResponse state] == "unassigned"} {
		puts "\nThe vport $eachVport is not assigned to a physical port. Skipping this vport verification"
		break
	    }
	    puts "\nPort: [dict get $assignedToResponse assignedTo]"
	    puts "\tVerifyPortState: [dict get $stateResponse state] \n\tWaiting $counter/$timeout seconds"
	    
            if {$counter < $timeout && ([dict get $stateResponse state] == "down" || [dict get $stateResponse state] == "busy") } {
		after 1000
		continue
	    }
	    if {$counter < $timeout && ([dict get $stateResponse state] == "up" || [dict get $stateResponse state] == "connectedLinkUp") } {
		break
	    }
	    if {$counter == $timeout && ([dict get $stateResponse state]== "down")} {
		# Failed
		error "Port failed to come up"
	    }
	}
    }
}

proc createVports {{portList None} {rawTrafficVportStyle False} sessionUrl} {
    # Description
    # 	This API creates virtual ports based on a portList.
    # 	Next step is to call assignPort.
    #    
    # Parameters
    # 	portList: <list>: Pass in a list of ports in the format of ixChassisIp, slotNumber, portNumber
    # 	portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]
    # 	rawTrafficVportStyle: <bool>: For raw Traffic Item src/dest endpoints, vports must be in format:
    # 								 /api/v1/sessions1/vport/{id}/protocols
    # 	sessionUrl : session url							 
    #	
    # Return
    #	 A list of vports
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set createdVportList []
    for {set index 0} {$index < [llength $portList]} {incr $index} { 
	puts "\nCreating a new virtual port"
	set url [concat $sessionUrl/vport]
	#puts "\nurl : $url"
	set response [post $url {}]
	#puts "\nresponse : $response"
	# vportObj = response.json()['links'][0]['href']
	set links [dict get $response links]
	set links [string range $links 1 end-1]
	set vportObj [dict get $links href]
		
	if {rawTrafficVportStyle == "True"} {
            lappend createdVportList [concat $vportObj/protocols]
	} else {
	    lappend createdVportList $vportObj
	}	
	if {portList != "None"} {
	    set match [regexp "(.*)/api.*" $sessionUrl m httpHeader]
	    set url [concat $sessionUrl/$vportObj]
	    set response [get $url]		
	    #puts "\nresponse : $response"
	    # response = self.ixnObj.get(self.ixnObj.httpHeader+vportObj)
	    set card [lindex [lindex $portList $index] 1]
	    set port [lindex [lindex $portList $index] 2]
	    set portNumber \"[concat $card/$port]\"
	    puts "\tName: $portNumber"
	    set body [list {"name" : $portNumber}]
	    set response [patch $url $body]	
	    #puts "\nresponse : $response"
	    # response = self.ixnObj.patch(self.ixnObj.httpHeader+vportObj, data={'name': portNumber})
	}
    }
    if {createdVportList == [] } {
	error "\n$procName : No vports created"
    }
    puts "\ncreateVports: $createdVportList"
    return $createdVportList
}

proc getPhysicalPortFromVport {vportList sessionUrl} {
    # Description
    # 	Get the physical ports assigned to the vport objects.
    #
    # Parameter
    # 	vportList: ['/api/v1/sessions/1/ixnetwork/vport/1']
    # 	sessionUrl : session url
    #
    # Returns
    # 	A list of ports: ['192.168.70.11:1:1']
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"

    set portList []
    set match [regexp "(.*)/api.*" $sessionUrl m httpHeader]
    foreach eachVport $vportList {
	set url [concat $httpHeader$eachVport]
	#puts "\nurl : $url"
	set response [get $url]
	#puts "\nresponse : $response"
	set assignedTo [dict get $response assignedTo]
	if {$assignedTo != ""} {
            lappend portList $assignedTo
	}
    }
    return $portList
}

proc getAllVportList {sessionUrl} {
    # Description
    # 	Returns a list of all the created virtual ports
    #    
    # Parameter
    #   sessionUrl : session url
    #
    # Returns
    # 	List of vports: ['/api/v1/sessions/1/ixnetwork/vport/1', '/api/v1/sessions/1/ixnetwork/vport/2']
    
    set url $sessionUrl/vport
    set response [get $url]
    #puts "\nresponse : $response"	
    foreach res $response {
	set links [dict get $res links]
	set links [string range $links 1 end-1]
	set href [dict get $links href]
	set vportList [lappend vportList $href]	
    }
    return $vportList
}

proc assignPorts {args} {
    # Description
    # 	Assuming that you already connected to an ixia chassis and ports are available for usage.
    # 	Use this API to assign physical ports to the virtual ports.
    #
    # Parameters
    # 	portList: <list>: A list of ports in a list: [ [ixChassisIp, '1','1'], [ixChassisIp, '1','2'] ]
    # 	createVports: <bool>: Optional:
    #			If True: Create vports to the amount of portList.
    # 			If False: Automatically create vport on the server side. Optimized for port bootup performance. 
    #
    # 	rawTraffic: <bool>:  If traffic item is raw, then vport needs to be /vport/{id}/protocols
    # 	resetPortCput: <bool>: Default=False. Some cards like the Novus 10GigLan requires a cpu reboot.
    # 	timeout: <int>: Timeout for port up state. Default=90 seconds.
    # 	sessionUrl : session url
    #
    # Syntaxes
    # 	POST:	/api/v1/sessions/{id}/ixnetwork/operations/assignports
    # 		 	data={arg1: [{arg1: ixChassisIp, arg2: 1, arg3: 1}, {arg1: ixChassisIp, arg2: 1, arg3: 2}],
    # 		 		  arg2: [],
    # 				  arg3: ['/api/v1/sessions/{1}/ixnetwork/vport/1',
    # 						'/api/v1/sessions/{1}/ixnetwork/vport/2'],
    #				  arg4: true}  <-- True will clear port ownership
    # 			headers={'content-type': 'application/json'}
    #
    # 	GET:  /api/v1/sessions/{id}/ixnetwork/operations/assignports/1
    # 		  data={}
    # 		  headers={}
    #
    # Expecting:   RESPONSE:  SUCCESS
	
    set portList []
    set createVports False
    set rawTraffic None
    set configPortName False
    set timeout 300
    
    set procName [lindex [info level [info level]] 0]
    puts "\nprocName: $procName"	

    set argIndex 0
    while {$argIndex < [llength $args]} {
	set currentArg [lindex $args $argIndex]
	switch -exact -- $currentArg {
	    -portList {
		set portList [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -createVports {
		set createVports [lindex $args [expr $argIndex + 1]]	
		incr argIndex 2			
	    }
	    -rawTraffic {
		set rawTraffic [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -configPortName {
		set configPortName [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -timeout {
		set timeout [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    -sessionUrl {
		set sessionUrl [lindex $args [expr $argIndex + 1]]
		incr argIndex 2			
	    }
	    default {
		error "$procName: No such parameter: $currentArg"
	    }
	}
    }
    # Verify if the portList has duplicates.
    verifyForDuplicatePorts $portList
    
    # Verify if there is existing vports. If yes, user either loaded a saved config file or 
    # the configuration already has vports.
    # If loading a saved config file and reassigning ports, assign ports to existing vports.
    set url [concat $sessionUrl/vport]
    #puts "\nurl : $url"
    set response [get $url]
    #puts "\nresponse : $response"
    
    if {$response != ""} {
        set mode 'modify'
	set count [regexp ".*/api(.*)" $sessionUrl match group]
	if {$count} {
	    set preamble $group
	}
	foreach value $response {
	    set id [dict get $value id]
	    set vportList [lappend list [concat "/api$preamble/vport/$id"]]
	}
	#puts "\nvportList : $vportList"		
	if {[llength $vportList] != [llength $portList]} {
	    error "\n$procName : virtual ports:[llength $vportList] is not equal to portList:[llength $portList]"
	}
    } else {
	if {$createVports == "False"} {
            set vportList []
	}
	if {$createVports == "True"} {
	    createVports $portList
	    set url [concat $sessionUrl/vport]
	    #puts "\nurl : $url"
	    set response [get $url]
	    #puts "\nresponse : $response"
	    set count [regexp ".*/api(.*)" $sessionUrl match group]
	    if {$count} {
		set preamble $group
	    }
	    foreach value $response {
		set id [dict get $value id]
		set vportList [lappend list [concat "/api$preamble/vport/$id"]]
	    }
	    if {[llength $vportList] != [llength $portList]} {
		error "\n$procName: virtual ports:[llength $vportList] is not equal to portList:[llength $portList]"
	    }			
	}
    }
    foreach eachPort $portList {
	#puts "\neachPortList : $eachPort"
	set chassisIp [lindex [split $eachPort ","] 0]
	set card [lindex [split $eachPort ","] 1]
	set portNum [lindex [split $eachPort ","] 2]
	set arg1 [list "\"arg1\": \"$chassisIp\", \"arg2\": \"$card\",  \"arg3\": \"$portNum\""]
	set count [llength $portList]		
	if {$count > 1} {
            set args1 [append args1 $arg1 ","]		
	} else {
	    set args1 $arg1
	}
    }
    foreach vport $vportList {
	set count [llength $vportList]
	set arg3 \"$vport\"			
	if {$count > 1} {
            set args3 [append args3 $arg3 ","]	
	} else {
	    set args3 $arg3
	}			
    }
    set args3 \[$args3\]
    set data  "\"arg1\": \[$args1\],\"arg2\": \[\], \"arg3\": $args3, \"arg4\": \"true\""
    set url [concat $sessionUrl/operations/assignports]
    #puts "\nurl : $url"
    set body [list $data]
    set response [post $url $body]
    #puts "\nresponse : $response"
    set id [dict get $response id]
    set url [concat $url/${id}]
    #puts "\nurl : $url"
    set response [waitForComplete -response $response -url $url -timeout 300]

    if {[dict get $response state] == "EXCEPTION"} {
	# Some cards like the Novus 10gLan sometimes requires a cpu reboot.
	# To reboot the port cpu, the ports have to be assigned to a vport first.
	# So it has to be done at this spot.
	resetPortCpu $vportList $portList
	verifyPortState		
	error "\n$procName : [dict get $response message]"
    } elseif {[dict get $response state] == "IN_PROGRESS" } {
	error "\n$procName: Port failed to boot up after $timeout seconds"
    } else {
	set url [concat $sessionUrl/vport]
	#puts "\nurl : $url"
	set response [get $url]
	#puts "\nresponse : $response"
	foreach res $response {
            set chassis [lindex [split [dict get $res assignedTo] ":"] 0]
	    set card [lindex [split [dict get $res assignedTo] ":"] 1]
	    set port [lindex [split [dict get $res assignedTo] ":"] 2]
	    set currentPort [list $chassisIp $card $port]
	    foreach port $portList {
	        set currentPortList [list $chassis $card $port]
		#TO be Checked with Hubert
		# if {set(currentPort) & set(currentPortList)} {
		if {"License Failed" == [dict get $res connectionStatus]} {
		    error "\n$procName : Port License failed."
		}
		if {[dict get $res connectionStatus] == "connectedLinkDown"} {
	            error "\n$procName : Port link connection is down: [dict get $res assignedTo]"
		}
		#}	
	    }
	}
    }					
    if {$configPortName == "True"} {
        # Name the vports
	set vportList [getAllVportList $sessionUrl]
	#puts "\nvportList : $vportList"
	set count [regexp "(.*)/api.*" $sessionUrl match group]
	if {$count} {
	    set httpHeader $group
	}		
	foreach vportObj $vportList {
	    #puts "\nvportObj : [lindex $vportObj 0]"
	    set port [getPhysicalPortFromVport $vportObj $sessionUrl]
	    set chassisIp [lindex [split $port ":"] 0]
	    set card [lindex [split $port ":"] 1]
	    set port [lindex [split $port ":"] 2]
	    set url [concat $httpHeader$vportObj]
	    #puts "\nurl : $url"
	    set data "\"name\": \"[concat $card/$port]\""
	    set body [list $data]
	    set response [patch $url $body]
	}
    }
    if {$rawTraffic == "True"} {
	set vportProtocolList []
	foreach vport [getAllVportList $sessionUrl] {
            lappend vportProtocolList $vport/protocols
	}
	return $vportProtocolList		
    } else {
	return $vportList
    }
}
