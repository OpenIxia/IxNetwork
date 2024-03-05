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
#     This script demonstrates how to use IxNetwork-IxReporter API             #
#     to generate a detailed pdf report using a custom template                #
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

# NOTE: add the restAPI module dirpath to the syspath
# in order to  be able to import it
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import restAPI as rest
from sample_script_settings import ixNetworkSetup

# Assuming the session number is 1,change accordingly
__SESSION_ID__ = 1
__CONFIG_NAME__ = 'ixReporter.ixncfg'

# reporter test parameters
__TEST_CATEGORY__   = 'IxReporter API Demo'
__TEST_DUT_NAME__   = 'No DUT. Using B2B ports.'
__TESTER_NAME__     = 'John Smith'
__TEST_HIGHLIGHTS__ = 'Ixia Summary PDF Report Sample'
__TEST_NAME__       = 'Ixia Sample'
__TEST_OBJECTIVES__ = 'Demo the IxReporter API'

# reporter Output settings
__OUTPUT_FORMAT__ = 'pdf'
__OUTPUT_PATH__   = 'C:\\DetailedReport.%s' % __OUTPUT_FORMAT__
__TEMPLATE_NAME__ = 'OSPF-Detailed.repx'

# Sample script start
ix = ixNetworkSetup(__SESSION_ID__)

# Clean up IxNetwork by creating a new config
rest.ixNetExec(ix.sessionUrl, 'newConfig')

# Load an IxNetwork configuration
rest.ixNetLoadConfig(ix.sessionUrl, __CONFIG_NAME__)

# Assign physical ports
rest.ixNetAssignPorts(ix.sessionUrl, ix.ports)
time.sleep(10)

# Start all protocols
rest.ixNetExec(ix.sessionUrl, 'startallprotocols')
time.sleep(10)

# configure Reporter test parameters
rest.ixNetSetAtt(ix.sessionUrl + '/reporter/testParameters',
    {
        'testCategory'   : __TEST_CATEGORY__,
        'testDUTName'    : __TEST_DUT_NAME__,
        'testerName'     : __TESTER_NAME__,
        'testHighlights' : __TEST_HIGHLIGHTS__,
        'testName'       : __TEST_NAME__,
        'testObjectives' : __TEST_OBJECTIVES__
    }
)

# extract the template directory path
templatePath = rest.ixNetGetAtt(ix.reporterUrl + '/generate', 'templatePath')
templatePath = '\\'.join(templatePath.split('\\')[:-1])

# set the file path for the custom template
templatePath = '\\'.join([templatePath, __TEMPLATE_NAME__])

# configure Reporter Output settings
rest.ixNetSetAtt(ix.sessionUrl + '/reporter/generate',
    {'outputFormat'    : __OUTPUT_FORMAT__,
        'outputPath'   : __OUTPUT_PATH__,
        'templatePath' : templatePath
    }
)

# save summary results
rest.ixNetExec(ix.reporterUrl + '/saveResults', 'saveSummaryResults', payload={'arg1': ix.reporterUrl + '/saveResults'})
# wait for the results to be saved
while rest.ixNetGetAtt(ix.reporterUrl + '/saveResults', 'state') != 'done':
    time.sleep(1)

# generate report
rest.ixNetExec(ix.reporterUrl + '/generate', 'generateReport', payload={'arg1': ix.reporterUrl + '/generate'})

# wait for the report to be generated
while rest.ixNetGetAtt(ix.reporterUrl + '/generate', 'state') != 'done':
    time.sleep(1)
