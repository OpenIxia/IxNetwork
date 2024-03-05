################################################################################
# Version 1.0    $Revision: #1 $                                                #
# $Author: cm $                                                      #
#                                                                              #
#    Copyright 1997 - 2016 by IXIA                                             #
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
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

If you want to run these sample script from the windows please install python2.6+
on the client and also install the httplib2 module accordingly. Now copy these test
files to the python directory (or any preferred test directory) and run them from
command prompt.

In order to modify setup parameters, please refer to the "HARNESS VARS" at the beginning of the script.
py = Py()
py.ports           = [('10.10.10.10', '1', '1'), ('10.10.10.10', '2', '1')] # [(chassisIP), cardID, portID]
py.ixTclServer  =  "11.11.11.11" # ixNetwork client IP
py.ixRestPort   =  "12345" # REST port for the ixN client
py.IP_list = ["1.1.1.1", "1.1.1.2"] # card IPs to be used in the test

In the logs folder, you can find samples of logs for the given scripts.

Please contact support for any clarification.
Thank You.

Ref:
https://code.google.com/p/httplib2/wiki/Install
http://stackoverflow.com/questions/5956891/how-do-i-install-httplib2-for-python-under-windows-7-64