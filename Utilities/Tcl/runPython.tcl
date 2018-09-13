#!/bin/expect

set pythonPath /usr/local/python3.7.0/bin/python3.7

proc GetShellPrompt {} {
   set prompt "(%|#|>|\\\$) ?$"
   return $prompt
}

proc SendCommand { id command {timeout 120}} {
    set timeout $timeout
    #set send_human {.3 .4 0.6 .1 3}
    puts "\nSendCommand: $command"

    send -i $id "$command\r"
    expect {
        -i $id
	-re [GetShellPrompt] {
	}
        timeout {
            puts "Error: command timedout: $command"
        }
    }
}

spawn csh
expect {
    ">>>" {
    }
    "$" {
	puts "Connected"
    }
    timeout {
	puts "Error: timeout"
    }
}

# Execute a Python ReST API script
SendCommand $spawn_id "$pythonPath ../..//RestApi/Python/SampleScripts/bgpNgpf.py"

