# coding: latin-1
################################################################################
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
################################################################################
# coding: ASCII
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


class ixNetworkSetup(object):
    '''
    Encapsulates the ixNetwork setup info:
        - api server + REST port
        - chassis
        - ports
    and REST API urls for ease of use.
    '''

    def __init__(self, session):
        # edit these variables to match your setup
        ports = [(2, 15), (2, 16)]
        self.__apiServer = 'localhost'
        self.__restPort = '11009'
        self.__chassis = '10.215.132.25'
        self.__ports = [(self.__chassis, card, port) for card, port in ports]

        self.__serverUrl = 'http://%s:%s' % (self.__apiServer, self.__restPort)
        self.__apiUrl = '%s/api/v1' % self.__serverUrl
        self.__sessionUrl = '%s/sessions/%s/ixnetwork' % (self.__apiUrl, session)
        self.__trafficUrl = '%s/traffic' % self.__sessionUrl
        self.__reporterUrl = '%s/reporter' % self.__sessionUrl

    @property
    def apiServer(self):
        return self.__apiServer

    @property
    def restPort(self):
        return self.__restPort

    @property
    def chassis(self):
        return self.__chassis

    @property
    def ports(self):
        return self.__ports

    @property
    def serverUrl(self):
        return self.__serverUrl

    @property
    def apiUrl(self):
        return self.__apiUrl

    @property
    def sessionUrl(self):
        return self.__sessionUrl

    @property
    def trafficUrl(self):
        return self.__trafficUrl

    @property
    def reporterUrl(self):
        return self.__reporterUrl
