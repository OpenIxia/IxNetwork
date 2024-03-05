# coding: latin-1
################################################################################
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
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
# coding: ASCII
################################################################################
#                                                                              #
# Description:                                                                 #
#    This script demonstrates how to create a custom view                      #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    OS        Windows 7 Professional (64 bit)                                 #
#    IxOS      8.10  EB (8.10.1251.65)                                         #
#    IxNetwork 8.10  EA (8.10.1045.7)                                          #
#                                                                              #
################################################################################

# Import REST Library and other modules, if necessary
import time
from datetime import datetime

# NOTE: add the restAPI module dirpath to the syspath
# in order to  be able to import it
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

import restAPI as rest
from sample_script_settings import ixNetworkSetup

# Assuming the session number is 1,change accordingly
__SESSION_ID__  = 1
__CONFIG_NAME__ = 'config.custom-views.ixncfg'

__CUSTOM_VIEW_NAME__ = 'traffic-flow'
__CUSTOM_VIEW_TYPE__ = 'layer23TrafficFlow'

# Sample script start
ix = ixNetworkSetup(__SESSION_ID__)

# Clean up IxNetwork by creating a new config
rest.ixNetExec(ix.sessionUrl, 'newConfig')

# Load an IxNetwork configuration
rest.ixNetLoadConfig(ix.sessionUrl, __CONFIG_NAME__)

# Assign physical ports
rest.ixNetAssignPorts(ix.sessionUrl, ix.ports)

# Start all protocols
rest.ixNetExec(ix.sessionUrl, 'startallprotocols')
time.sleep(30)

# Generate, apply and start the traffic
rest.generateApplyStartTraffic(ix.sessionUrl, True)

# Wait 90 seconds for the traffic to start
startTime = datetime.now()
while rest.ixNetGetAtt(ix.trafficUrl, 'state') != 'started':
    if (datetime.now() - startTime).seconds > 90:
        raise Exception('Waited for 90 sec, Traffic still not in started state !')
    time.sleep(1)

# Letting the traffic for 30 seconds
time.sleep(30)

# Create a custom view
newViewUrl = rest.ixNetCreateCustomView(ix.sessionUrl, __CUSTOM_VIEW_NAME__, __CUSTOM_VIEW_TYPE__, visible=True)

# Retrieve relevant filters for the view
portFilters = rest.ixNetGetLink(newViewUrl, '/availablePortFilter')
portFilterUrls = [portFilter['links'][0]['href'] for portFilter in portFilters]

trackingFilters = rest.ixNetGetLink(newViewUrl, '/availableTrackingFilter')
trackingFiltersUrls = [trackingFilter['links'][0]['href'] for trackingFilter in trackingFilters]

trafficItemFilters = rest.ixNetGetLink(newViewUrl, '/availableTrafficItemFilter')
trafficItemFiltersUrls = [trafficItemFilter['links'][0]['href'] for trafficItemFilter in trafficItemFilters]

# Configure the filter selection area; set the filter on all the traffic ports
rest.ixNetSetAtt(
    newViewUrl + '/layer23TrafficFlowFilter',
    {
        'portFilterIds'         : portFilterUrls,
        'aggregatedAcrossPorts' : 'false',
        'trafficItemFilterIds'  : trafficItemFiltersUrls
    }
)

# Configure the enumeration filter - Sorting and Grouping Hierarchy
for url in trackingFiltersUrls:
    data = [
        {
            'trackingFilterId': url,
            'sortDirection': 'ascending'
        }
    ]
    rest.addIxNetObject('%s/layer23TrafficFlowFilter' % newViewUrl, '/enumerationFilter', data=data)

# Enable all statistics for the custom view
rest.setAllStatisticsStates(newViewUrl, enabled=True)

# Enable the custom view to start retrieving stats
rest.ixNetSetAtt(newViewUrl, {'enabled': True})
