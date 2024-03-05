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
#    This module contains required definitions for restAPI sample scripts      #
#                                                                              #
################################################################################


import json
import requests
import time

_URL_HEADERS_JSON = {'content-type': 'application/json'}


class TestFailedError(Exception):
    ''' Custom exception'''
    pass


def addIxNetObject(sessionUrl, obj, data='', logging=True):
    '''
    Args:
        obj(str): object type
    Returns:
        requests.models.Response Object
    Usage:
        addIxNetObject(sessionUrl, 'vport')
    '''
    addPortUrl = '%s/%s' % (sessionUrl, obj)

    if logging:
        print 'POST: ' + addPortUrl

    if data:
        response = requests.post(addPortUrl, json.dumps(data), headers=_URL_HEADERS_JSON)
    else:
        response = requests.post(addPortUrl, headers=_URL_HEADERS_JSON)

    if not response.ok:
        TestFailedError(response.text)

    return response


def getIxNetPorts(sessionUrl, logging=True):
    '''
    Get ixNetwork ports, returns response in requests form
    Args:
        sessionUrl(str):
    Returns:
       requests.models.Response Object
    Usage:
        aa = getIxNetPorts(ixNetUrl, 1)
    '''
    try:
        getPortsUrl = sessionUrl + '/vport'
        response = requests.get(getPortsUrl)

        if logging:
            print 'GET: ' + getPortsUrl

    except Exception, e:
        raise Exception('Error code: ', e)
    if not response.ok:
        TestFailedError(response.text)
    return response


def ixNetExec(objUrl, execName, payload=None):
    '''
    ixNet exec with no arguments, returns response in requests form
    Args:
        objUrl(str):
        execName(str):
        payload(dict):
    Returns:
        requests.models.Response Object
    Usage:
        ixNetExec(ixNetUrl, 1, 'newConfig')
    '''
    try:
        urlString = ''.join([objUrl, '/operations/', execName])

        if payload is None:
            print 'POST: ' + urlString
            response = requests.post(url=urlString, headers=_URL_HEADERS_JSON)
        else:
            print 'POST: ' + urlString + '  <-- Payload: ' + str(payload)
            response = requests.post(url=urlString, headers=_URL_HEADERS_JSON, data=json.dumps(payload))

        if response.json()['id'] != '':
            waitForComplete(objUrl, response)

        if not response.ok:
            raise TestFailedError(response.text)
        return response

    except Exception, e:
        raise Exception('Got an error code: ', e)


def waitForComplete(sessionUrl, requestSess, timeout=120):
    '''
    Wait for the current operation to complete
    Args:
        sessionUrl(str):
        requestSess
        timeout(int):
    Returns:
        requests.models.Response Object
    Usage:
        waitForComplete(sessionUrl, response)
    '''
    a = requestSess.json()
    for key in a:
        if 'errors' in key:
            raise Exception('FAIL : need To Exit ', a['errors'])
    state = a['state']
    print state
    if state == 'SUCCESS':
        return 'Current state: ' + state

    if state != 'COMPLETED':
        print 'WAIT FOR ACTION TO COMPLETE'
        url = a['url'].split('operations/')[1]
        print 'Current state: ' + state
        it = 0
        while state == 'IN_PROGRESS':
            if timeout == it:
                raise TestFailedError('Operation is still in progress after : ' + str(timeout) + ' seconds')
            time.sleep(1)
            stateURL_ = sessionUrl + '/operations/' + url
            _stateURL = stateURL_.replace('//', '/')
            stateURL = _stateURL.replace('http:/', 'http://')
            state = ixNetGetAtt(stateURL, 'state', False)
            print 'Current state: ' + state + ' after ' + str(it) + ' seconds'
            it = it + 1
    if state == 'ERROR':
        raise TestFailedError('FAIL : process did not went to Completed state')


def ixNetAssignPorts(sessionUrl, realPorts):
    '''
    ixNet assign ports
    Args:
        sessionUrl(str):
        realPorts[(list of tuples)]: the ports to be assigned
    Returns:
        requests.models.Response Object
    Usage:
        py.ports = [('10.205.11.22', '3', '15'), ('10.205.11.22', '3', '16')]
        ixNetAssignPorts(ixNetUrl, 1, py.ports)
    '''
    try:
        print 'Assigning Multiple Ports at once'
        urlString = sessionUrl + '/operations/assignports'

        # get the vports in current session
        vportIds = [str(v['id']) for v in getIxNetPorts(sessionUrl).json()]
        datas = []
        portIds = []

        # create data and post foreach real port
        for vPortId, (chassis, card, port) in zip(vportIds, realPorts):
            datas.append({'arg1': chassis, 'arg2': str(card), 'arg3': str(port)})
            portIds.append(sessionUrl + '/vport/' + vPortId)

        payload = {'arg1': datas, 'arg2': [], 'arg3': portIds, 'arg4': True}
        print 'POST: ' + urlString + ' <--- DATA: ' + str(payload)
        response = requests.post(url=urlString, data=json.dumps(payload), headers=_URL_HEADERS_JSON)
        waitForComplete(sessionUrl, response)

        if not response.ok:
            TestFailedError(response.text)
        return response
    except Exception, e:
        print str(e)


def ixNetSetAtt(urlString, att):
    '''
    Args:
        urlString(str):
    Returns:
        requests.models.Response Object
    Usage:
        attribute = {'name':'PortCreatedFromRest'}
        response = ixNetSetAtt(ix.sessionUrl, '/vport/1', attribute)
    '''
    try:
        print 'PATCH: ' + urlString + ' <-- Attribute: ' + str(att)
        response = requests.patch(url=urlString, data=json.dumps(att), headers=_URL_HEADERS_JSON)
        if '[200]' not in str(response):
            raise TestFailedError(response.json()['errors'])
        return response
    except Exception, e:
        raise Exception('Got an error code: ', e)


def ixNetGetAtt(getAttUrl, att, logging=True):
    '''
    ixNet getA method, return result in text mode
    Args:
        getAttUrl(str): the url of the item containing the attribute
        att(str): the name of the attribute
        logging(bool): enable/disable logging
    Returns:
        str: the requested attribute, if it exists
    Usage:
         aa = ixNetGetAtt(ix.sessionUrl, 1, 'vport/1', 'name')
    '''
    try:
        if logging:
            print 'GET: ' + getAttUrl
        response = requests.get(getAttUrl)
        res = response.json()
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if '[200]' not in str(response):
        raise TestFailedError(response.json()['errors'])
    attUrl = res[att]
    return attUrl


def ixNetLoadConfig(ixNetSessionUrl, configName):
    '''
    ixNet exec loadConfig
    Args:
        sessionUrl(str): the url to the ixNetSession
        configName(str): path to the config
    Returns:
        requests.models.Response Object
    Usage:
        configName = 'config.configName.ixncfg'
        ixNetLoadConfig(ixNetSessionUrl, configName)
    '''
    urlHeadersData = {'content-type': 'application/octet-stream'}
    print 'Uploading IxNetwork config to server'
    if '\\' in configName:
        configName = configName.split('\\')[-1]
    uploadUrl = ixNetSessionUrl + '/files/' + configName

    # read the config as binary
    with open(configName, mode='rb') as file:
        configContent = file.read()

    # send the config to server files location
    r = requests.post(uploadUrl, headers=urlHeadersData, data=configContent)
    if configName in r.text:
        print 'IxNetwork config uploaded Correctly, now loading the config'
        dataJson = {'filename': configName}
        loadConfigUrl = ixNetSessionUrl + '/operations/loadConfig'
        r = requests.post(url=loadConfigUrl, data=json.dumps(dataJson), headers=_URL_HEADERS_JSON)
        responseCode = str(r)
        if 'Response [200]' not in responseCode:
            print r.text
            return False
        else:
            return True
    else:
        print 'Config Not uploaded correctly to server'
        return False


def generateApplyStartTraffic(ixNetSessionUrl, refreshBeforeApply=False):
    '''
    Args:
        ixNetSessionUrl(str):
        refreshBeforeApply(bool):
    Returns:
        0
    Usage:
        generateApplyStartTraffic(ixNetSessionUrl,refreshBeforeApply=False,timeOut=90)
    '''
    print 'Generate Apply Start Traffic...'
    trafficURL = ixNetSessionUrl + '/traffic/'
    print 'Set refreshLearnedInfoBeforeApply for Traffic to %s' % (str(refreshBeforeApply),)
    if refreshBeforeApply:
        if __setAndCheckAttributeValue(trafficURL, 'refreshLearnedInfoBeforeApply', 'true'):
            return 1
    else:
        if __setAndCheckAttributeValue(trafficURL, 'refreshLearnedInfoBeforeApply', 'false'):
            return 1

    # Apply Traffic
    print 'Applying the traffic ....'
    response = requests.get(trafficURL, headers=_URL_HEADERS_JSON)
    res = response.json()
    node = res['links'][-1]['href']
    data = {'arg1': node}
    ixNetExec(trafficURL, 'apply', data)

    print 'Starting the traffic...'
    data = {'arg1': [node]}
    ixNetExec(trafficURL, 'startStatelessTraffic', data)
    print 'SUCCESS:Generate Apply Start Traffic...'
    return 0


def __setAndCheckAttributeValue(ixNetSessionUrl, attr, value):
    '''
    __setAndCheckAttributeValue - set and verify the value
    Args:
        ixNetSessionUrl(str):
        attr(str):
        value:
    Returns:
        0
    Usage:
        __setAndCheckAttributeValue(trafficURL,'refreshLearnedInfoBeforeApply','false')
    '''
    print 'Verifying for the node :', ixNetSessionUrl
    isError = 1
    retVal = str(value).lower()
    setVal = {attr: value}
    print '', attr, value, retVal, setVal

    try:
        ixNetSetAtt(ixNetSessionUrl, setVal)
    except Exception, e:
        print 'Error while setting %s node attribute %s value %s' % (ixNetSessionUrl, attr, value)
        print str(e)
        return isError

    retAttrVal = str(ixNetGetAtt(ixNetSessionUrl, attr))
    if retVal != str(retAttrVal).lower():
        print 'FAIL:getAttribute value (%s) does not match with expected value (%s)' % (retAttrVal, retVal)
        return isError
    return 0


def ixNetGetViewUrl(ixNetSessionUrl, viewName):
    '''
    Retrieve view url
    Args:
        ixNetSessionUrl(str): session url
        viewName(str): name of the view
    Returns:
        url(str): if the viewName exists
    Raises:
        ValueError : if the view name does not exist
    Usage:
        ixNetGetView(
            ixNetSessionUrl, 'Protocols Summary')
    '''
    getUrl = ixNetSessionUrl + '/statistics/view/'

    response = requests.get(getUrl).json()
    for view in response:
        if view['caption'] == str(viewName):
            return getUrl + str(view['id'])
    raise ValueError('View name does not exist')


def ixNetCreateCustomView(sessionUrl, caption=None, viewType=None, visible=True):
    '''
    Creates a custom view
    Params:
    sessionUrl('str'):
    caption('str'):
    viewType('str'):
    visible('str'):

    Returns:
        (str): the url of the created custom view
    '''
    statsView = 'statistics/view/'
    customView = addIxNetObject(sessionUrl, statsView).json()
    customViewId = customView['links'][0]['href'].split(statsView)[-1]
    customViewUrl = '%s/statistics/view/%s' % (sessionUrl, customViewId)

    if viewType is not None:
        ixNetSetAtt(customViewUrl, {'type': viewType})

    if caption is not None:
        ixNetSetAtt(customViewUrl, {'caption': caption})
        customViewUrl = ixNetGetViewUrl(sessionUrl, caption)

    ixNetSetAtt(customViewUrl, {'visible': visible})
    return customViewUrl


def ixNetGetLink(objectUrl, link):
    '''Returns the link/links from a page'''
    return requests.get(objectUrl + link).json()


def getStatistics(viewUrl):
    '''Returns the all the stats urls that exist in a view'''
    statsCount = requests.get(viewUrl + '/statistic?skip=0&take=0').json()['count']
    return ['%s/statistic/%s' % (viewUrl, id + 1) for id in range(statsCount)]


def setAllStatisticsStates(viewUrl, enabled=True):
    '''Sets the state for all the statistics in a view'''
    statsCount = requests.get(viewUrl + '/statistic?skip=0&take=0').json()['count']
    for id in range(statsCount):
        ixNetSetAtt('%s/statistic/%s' % (viewUrl, id + 1), {'enabled': enabled})


def setStatisticState(viewUrl, statisticName, enabled=True):
    '''
    Sets the state of a stat in a view
    The stat is identified by name
    '''
    statistics = requests.get(viewUrl + '/statistic').json()['data']
    for statistic in statistics:
        if statistic['caption'] == statisticName:
            ixNetSetAtt('%s/statistic/%s' % (viewUrl, statistic['id']), {'enabled': enabled})


def getStatisticUrlByName(sessionUrl, statisticName):
    '''Returns the url of a stat.'''
    statistics = requests.get(sessionUrl + '/statistics/view').json()
    for statistic in statistics:
        if statistic['caption'] == statisticName:
            return statistic['links'][0]['href']


def setStatisticStateByIndex(viewUrl, statisticIndex, enabled=True):
    '''
    Sets the state of a stat in a view
    The stat is identified by index
    '''
    if statisticIndex > requests.get(viewUrl + '/statistic?skip=0&take=100').json()['count']:
        raise IndexError
    ixNetSetAtt('%s/statistic/%s' % (viewUrl, statisticIndex), {'enabled': enabled})
