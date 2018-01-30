"""
Description:

    Monitor specified Traffic Item by its name and/or monitor protocol sessions up/down (flapping)
    and send email alerts if the frames delta counter is equal or greater than
    the user defined threshold value.

    A separate email alert is sent foreach unique Traffic Item and protocol session.

    Supports single session Windows and Linux API server. If monitoring a session on Linux API Server,
    include parameter -apiKey <apiKey> and -sessionId <sessionId>

Features:
  - Traffic Item monitoring.
      - Monitor one or more Traffic Items.
      - Monitor protocol sessions also on a sepate termianl.
      - Use regex for -trafficName input.
      - Set frame loss threshold.
      - Stats includes:
           - timestamp, trafficItemName, packetLossDuration, txLineRate, rxLineRate, lossFramesDelta
      - For protocol session monitoring, set protocol session flapping threshold.
      - Send email alerts for each Traffic Item if it reach the threshold.
      - Set the stat monitoring polling interval.
      - Each Traffic Item will have its own recorded stats in json file.
        The json file name is the name of the TrafficItem.stats.
    - Statistics result filename: monitorTraffic.json

  - Protocol Session flap monitoring.
      - Statistics result filename: monitorProtocol.json
      - On seperate terminal.
      - One or more protocols to monitor.
        Stats includes:
           - timestamp, protocol, port, flapMarker, flap, flapDelta.
      - Available protocols: bgp, ospf, isis, igmp, pim, mld
      - Each port/protocol will send it's own threshold alert.
      - Each protocol will have its own recorded stats.
        The text file name is the name of the protocol.stats.

      Time       Protocol  Port                 Up    Down   FlapMarker  Flapped   FlapDelta
      ---------------------------------------------------------------------------------------
      19:45:55   BGP       1/1                  3     0      8           18        10
      19:45:55   BGP       2/1                  3     0      8           18        10

Command Line Parameters:

       For help:
          Enter: python monitorTraffic.py help


       For monitoring Traffic Items:
          To show a list of configured Traffic Items:
              Enter: python monitorTraffic.py -showTrafficItemNames

          Enter: python monitorTraffic.py -apiServerIp 192.168.70.127 -trafficName 'traf.*1 traf.*2' -frameLossThreshold 500 \
          -recordStatsToFile

       For monitoring protocol session flappings:
          Enter: python monitorTraffic.py -apiServerIp 192.168.70.127 -protocolSessions "bgp" -frameLossThreshold 2 \
          -recordStatsToFile

"""

from __future__ import absolute_import, print_function
import os, sys, requests, json, time, re, datetime, traceback
from IxNetRestApi import *
from IxNetRestApiStatistics import Statistics
from IxNetRestApiTraffic import Traffic

class Variables():
    ixNetRestServerIp = '192.168.70.127'
    ixNetRestServerPort = '11009'
    connectToApiServer = 'windows'
    getStatInterval = 2
    recordStatsToFile = False
    apiKey = None
    sessionId = None
    jsonFileForTraffic = 'monitorTraffic.json'
    jsonFileForProtocol = 'monitorProtocoljson'
    jsonData= {}
    Variables.statObj = None
    Variables.trafficObj = None

    # These two variables are reserved for connecting to a Linux API server.
    # Send email alerts
    emailSubject = 'ALERT: IxNetwork Traffic Monitoring Failed:'
    emailFrom = 'monitorTraffic.py Script'
    emailSendFrom = 'hgee@ixiacom.com'
    emailSenderPassword = '-'
    emailSmtpServer = 'pod51011.outlook.com'
    emailSmtpServerPort = 587
    sendEmailTo = emailSendFrom
    sendAlert = False
    emailPasswordFile = None

    # Don't touch these variables.
    trafficItemsToMonitor = []     ;# List of Traffic Items Names to monitor.
    protocolSessionsToMonitor = [] ;# List of protocol sessions to monitor.
    statisticFileTopLineFlag = {}  ;# Do it once flag.
    framesDeltaBeginMarker = {}    ;# Mark the current delta frame loss when starting this app.
    sendEmailAlertOnceFlag = {}    ;# Dict for each traffic item or for each protocol/port session.
    externalExecution = False
    frameLossDeltaThreshold = 0
    displayMaxLineOutput = 10
    displayMaxLineOutputFlag = 0
    sessionUrl = None
    sessionObj = None
    monitorTrafficColumnNames = 0

class IxNetRestApiException(Exception): pass

def help():
    os.system('clear')
    print('\nParameters:')
    print('\t-connectToApiServer   : windows|linux. The IxNetwork API server connecting to.')
    print('\t-apiServerIp          : The IxNetwork API server IP to connect to')
    print('\t-apiServerIpPort      : The IxNetwork API server IP port.')
    print('\t                        Windows default=11009. Linux default=443')
    print('\n\t-showTrafficItemNames : Display all the configured Traffic Item names')
    print('\t-trafficName          : all or Traffic Item names to monitor inside double quotes')
    print('\t                        Ex: -trafficName all')
    print('\t                        Ex: Use regex: -trafficName "traffic_1 .*2 traf.*3"\n')
    print('\t-protocolSessions     : The protocol sessions to monitor inside double quotes')
    print('\t                            Available protocols: bgp, ospf, isis, igmp, pim, mld')
    print('\t                      : Ex: -protocolSessionToMonitor "bgp, ospf"\n')
    print('\t-frameLossThreshold   : Send email alert when frame loss is reached')
    print('\t-emailSendFrom        : Your email address')
    print('\t-getStatInterval      : The interval period in seconds to get stats')
    print('\t-emailPasswordFile    : By default, your email password is not required unless you')
    print('\t                        need to include it. Then you need to put your email password into a file and')
    print('\t                        state the full path and filename as the value')
    print('\t-sendAlert            : Defaults to false. Add this parameter if you want email notifications.')
    print('\t-externalExecution    : Defaults to false. Set to true if executing this script from another script.')
    print('\t-recordStatsToFile    : To record statistics to a text file -> traffic_item_name.stats')
    print('\t-displayMaxLines      : Display the max lines of stats per terminal screen')
    print('\t-apiKey               : Only for connecting to an existing session on Linux. The Linux API server user API-KEY')
    print('\t-sessioinId           : Only for connecting to an existing session on Linux. The session ID number')
    print('\n\n')
    print('Example:')
    print('\n  Connecting to a  Windows API server:')
    print('\n\tpython monitorTraffic.py -apiServerIp 192.168.70.127 -trafficName all -displayMaxLines 5')
    print('\tpython monitorTraffic.py -apiServerIp 192.168.70.127 -protocolSessions bgp -displayMaxLines 3')
    print('\n  Connecting to a Linux API server:')
    print('\n\tpython monitorTraffic.py -connectToApiServer linux -apiServerIp 192.168.70.127 -apiServerIpPort 443\n\t\t-apiKey 75c3663f920b4fe986ab1d1c39bc1658 -sessionId 3 -trafficName all\n\t\t-displayMaxLines 5 -getStatInterval 3')

    print('\n\tpython monitorTraffic.py -connectToApiServer linux -apiServerIp 192.168.70.127 -apiServerIpPort 443\n\t\t-apiKey 75c3663f920b4fe986ab1d1c39bc1658 -sessionId 3 -protocolSessions bgp\n\t\t-displayMaxLines 3 -getStatInterval 3')
    print()

def connect():
    if Variables.connectToApiServer == 'windows':
        restObj = Connect(apiServerIp=Variables.ixNetRestServerIp, serverIpPort=Variables.ixNetRestServerPort)

    if Variables.connectToApiServer == 'linux':
        print('\napiKey:', Variables.apiKey)
        print('sessionId:', Variables.sessionId)
        print('apiServerIpPort:', Variables.ixNetRestServerPort)

        restObj = Connect(apiServerIp=Variables.ixNetRestServerIp,
                          serverIpPort=Variables.ixNetRestServerPort,
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=False,
                          verifySslCert=False,
                          serverOs=Variables.connectToApiServer,
                          apiKey=Variables.apiKey,
                          sessionId=Variables.sessionId
                        )

    Variables.sessionUrl = restObj.sessionUrl
    Variables.sessionObj = restObj
    statObj = Statistics(restObj)
    trafficObj = Traffic(restObj)
    Variables.statObj = statObj
    Variables.trafficObj = trafficObj

def writeToJson(monitoring):
    if monitoring == 'traffic':
        jsonFile = Variables.jsonFileForTraffic
    if monitoring == 'protocol':
        jsonFile = Variables.jsonFileForProtocol

    # Write to a json file:
    with open(jsonFile, 'w') as outFile:
        json.dump(Variables.jsonData, outFile, sort_keys=True)

def sendEmail(emailTo, bodyMessage):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import email.utils
    import smtplib

    body = MIMEText('%s' % bodyMessage, 'plain')

    message = MIMEMultipart()
    message['subject'] = Variables.emailSubject
    message['To'] = ','.join(emailTo.split(' '))
    message['From'] = Variables.emailFrom
    message.attach(body)
    server = smtplib.SMTP('%s:%d' % (Variables.emailSmtpServer, Variables.emailSmtpServerPort))
    server.ehlo()
    server.starttls()
    if Variables.emailSenderPassword:
        server.login(Variables.emailSendFrom, Variables.emailSenderPassword)
    else:
        server.login(Variables.emailSendFrom)
    server.sendmail(Variables.emailSendFrom, emailTo.split(' '), message.as_string())
    server.quit()
    print('\nEmail is sent')

def monitorTraffic():
    #stats = Variables.sessionObj.getStats(viewName='Traffic Item Statistics', displayStats=False, silentMode=True)
    stats = Variables.statObj.getStats(viewName='Traffic Item Statistics', displayStats=False, silentMode=True)
    now = datetime.datetime.now()

    if Variables.displayMaxLineOutputFlag == 0:
        if Variables.monitorTrafficColumnNames == Variables.displayMaxLineOutput:
            Variables.monitorTrafficColumnNames = 0
            statisticTopLine = '\n{0:10} {1:17} {2:15} {3:15} {4:15} {5:15} {6:15} {7:12} {8:10}'.format(
                'Time', 'TrafficItemName', 'TxRate', 'RxRate', 'TxFrames', 'RxFrames', 'LossDur(ms)', 'LossDelta', 'LossThreshold' )
            print(statisticTopLine)
            print('-'*140)
        Variables.monitorTrafficColumnNames += 1
        Variables.displayMaxLineOutputFlag == 1

        if Variables.displayMaxLineOutputFlag == 1 and Variables.monitorTrafficColumnNames == Variables.displayMaxLineOutput:
            Variables.displayMaxLineOutputFlag = 0

    for trafficItemStats,values in stats.items():
        if values['Traffic Item'] in Variables.trafficItemsToMonitor:
            trafficItemName = values['Traffic Item']
            txRate = values['Tx Frame Rate']
            rxRate = values['Rx Frame Rate']
            txFrames = values['Tx Frames']
            rxFrames = values['Rx Frames']
            #lossPct = values['Loss %']
            framesDelta = values['Frames Delta']

            try:
                pktLossDuration = values['Packet Loss Duration (ms)']
            except:
                pktLossDuration = 'NotEnabled'

            if  trafficItemName not in Variables.statisticFileTopLineFlag:
                Variables.statisticFileTopLineFlag[trafficItemName] = 0

            if Variables.recordStatsToFile:
                if Variables.statisticFileTopLineFlag[trafficItemName] == 0:
                    Variables.jsonData[trafficItemName]['columnNames'] = statisticTopLine.split()
                    writeToJson(monitoring='traffic')

                    #with open(trafficItemName+'.stats', 'a') as statFile:
                    #    statFile.write(statisticTopLine+'\n')
                    Variables.statisticFileTopLineFlag[trafficItemName] = 1

            statistics = '{0:10} {1:17} {2:15} {3:15} {4:15} {5:15} {6:15} {7:12} {8:10}'.format(
                now.strftime('%H:%M:%S'),
                trafficItemName,
                txRate,
                rxRate,
                txFrames,
                rxFrames,
                pktLossDuration,
                framesDelta,
                str(Variables.frameLossDeltaThreshold).strip()
                )
            print(statistics)

            if Variables.recordStatsToFile:
                Variables.jsonData[trafficItemName]['statistics'].append(statistics.split())
                writeToJson(monitoring='traffic')

                #with open(trafficItemName+'.stats', 'a') as statFile:
                #    statFile.write(statistics+'\n')
            if Variables.frameLossDeltaThreshold != 0:
                if int(framesDelta) >= Variables.frameLossDeltaThreshold:
                    if Variables.sendEmailAlertOnceFlag[trafficItemName] == 0:
                        Variables.sendEmailAlertOnceFlag[trafficItemName] = 1
                        bodyMessage = '\nThe Traffic Item reached the delta frame loss threshold: {0}'.format(
                            Variables.frameLossDeltaThreshold)
                        bodyMessage = bodyMessage + '\n\tTrafficItemName: {0}'.format(trafficItemName)
                        print('\n', bodyMessage)
                        if Variables.sendAlert == True:
                            print('\nSending email alert to: {0}\n'.format(Variables.sendEmailTo))
                            sendEmail(Variables.sendEmailTo, bodyMessage)
    #print()

def monitorProtocol():
    # Each port will send an email alert if its protocol session flaps.

    for eachProtocolSession in Variables.protocolSessionsToMonitor:
        #stats = Variables.sessionObj.getStats(viewName=eachProtocolSession, displayStats=False, silentMode=True, ignoreError=True)
        stats = Variables.statObj.getStats(viewName=eachProtocolSession, displayStats=False, silentMode=True, ignoreError=True)
        if stats is None:
            raise Exception('\nProtocol is not enabled:', eachProtocolSession)
        protocolName = eachProtocolSession.split(' ')[0].lower()
        now = datetime.datetime.now()
        statFileName = protocolName+'.stats'

        if Variables.displayMaxLineOutputFlag == 0:
            if Variables.monitorTrafficColumnNames == Variables.displayMaxLineOutput:
                Variables.monitorTrafficColumnNames = 0
                statisticTopLine = '\n{0:10} {1:9} {2:20} {3:5} {4:6} {5:11} {6:9} {7:10}'.format(
                    'Time', 'Protocol', 'Port', 'Up', 'Down', 'FlapMarker', 'Flapped', 'FlapDelta')
                print(statisticTopLine)
                print('-'*85)
            Variables.monitorTrafficColumnNames += 1
            Variables.displayMaxLineOutputFlag == 1

            if Variables.displayMaxLineOutputFlag == 1 and Variables.monitorTrafficColumnNames == Variables.displayMaxLineOutput:
                Variables.displayMaxLineOutputFlag = 0

        maxLineCounter = 1
        for statName,values in stats.items():
            if Variables.displayMaxLineOutputFlag == 0:
                if maxLineCounter == Variables.displayMaxLineOutput:
                    print(statisticTopLine)
                    print('-'*85)

            if Variables.recordStatsToFile:
                # Instantiate a new stat file to store stats and create a column name
                # line at the top of the file.
                if Variables.statisticFileTopLineFlag[protocolName] == 0:
                    #with open(statFileName, 'a') as statFile:
                    #    statFile.write(statisticTopLine+'\n')
                    Variables.statisticFileTopLineFlag[protocolName] = 1
                    if Variables.recordStatsToFile:
                        Variables.jsonData[protocolName]['columnNames'] = statisticTopLine.split()
                        writeToJson(monitoring='protocol')

                # No protocol stat because the protocol is not up.
                if stats is None:
                    statistics = '{0:10} {1} is not up'.format(now.strftime('%H:%M:%S'), protocolName)
                    print(statistics)
                    with open(statFileName, 'a') as statFile:
                        statFile.write(statistics+'\n')
                    continue

            try:
                port = values['Port']
                sessionsUp = int(values['Sessions Up'].strip())
                sessionsDown = int(values['Sessions Down'].strip())
                sessionsFlapCount = int(values['Session Flap Count'].strip())

                # Set the starting marker by getting the current framesDelta count
                if (protocolName,port) not in Variables.framesDeltaBeginMarker:
                    Variables.framesDeltaBeginMarker[protocolName,port] = sessionsFlapCount

                # Set send email flag to send email one time only.
                if (protocolName,port) not in Variables.sendEmailAlertOnceFlag:
                    Variables.sendEmailAlertOnceFlag[protocolName,port] = 0

                flapDelta = sessionsFlapCount - Variables.framesDeltaBeginMarker[protocolName,port]
                statistics = '{0:10} {1:9} {2:20} {3:5} {4:6} {5:11} {6:9} {7:10}'.format(
                    now.strftime('%H:%M:%S'),
                    eachProtocolSession.split(' ')[0],
                    port,
                    str(sessionsUp),
                    str(sessionsDown),
                    str(Variables.framesDeltaBeginMarker[protocolName,port]),
                    str(sessionsFlapCount),
                    str(flapDelta))

                maxLineCounter += 1
                if int(maxLineCounter) == int(Variables.displayMaxLineOutput):
                    maxLineCounter = 0

                print(statistics)
                if Variables.recordStatsToFile:
                    #with open(statFileName, 'a') as statFile:
                    #    statFile.write(statistics+'\n')
                    if Variables.recordStatsToFile:
                        Variables.jsonData[protocolName]['statistics'].append(statistics.split())
                        writeToJson(monitoring='protocol')

                # Time       Protocol  Port                 Up    Down   FlapMarker  Flapped   FlapDelta
                # -------------------------------------------------------------------------------------
                # 20:01:41   BGP       1/1                  2     1      40          42        2

                # protocolName,port = bgp, 2/1
                # framesDeltaBeginMarker: {('bgp', '2/1'): 28, ('bgp', '1/1'): 28}
                if (protocolName,port) in Variables.framesDeltaBeginMarker:
                    if flapDelta >= Variables.frameLossDeltaThreshold:
                        if Variables.sendEmailAlertOnceFlag[protocolName,port] == 0:
                            Variables.sendEmailAlertOnceFlag[protocolName,port] = 1
                            bodyMessage = '\nThe {0} protocol session on port "{1}" flapped: '.format(protocolName, port)
                            bodyMessage = bodyMessage + '\n\n\tProtocolSessionName: {0}'.format(protocolName)
                            bodyMessage = bodyMessage + '\n\tSessionsFlapMarker: {0}'.format(
                                str(Variables.framesDeltaBeginMarker[protocolName,port]))
                            bodyMessage = bodyMessage + '\n\tSessionsFlapCount: {0}'.format(sessionsFlapCount)
                            bodyMessage = bodyMessage + '\n\tSessionsFlapDelta: {0}\n'.format(flapDelta)
                            print('\n%s' % bodyMessage)
                            if Variables.sendAlert == True:
                                print('\tSending email alert to: {0}\n'.format(Variables.sendEmailTo))
                                sendEmail(Variables.sendEmailTo, bodyMessage)

            except Exception as errMsg:
                statistics = '{0:10} {1} is not up'.format(now.strftime('%H:%M:%S'), protocolName)
                print('{0}: Exception: {1}'.format(statistics, errMsg))

            '''
            BGP session stats
              Session Flap Count:  0
              Sessions Established:  1
              Route Withdraws Rx:  0
              KeepAlives Rx:  115
              Sessions Up:  1
              Opens Rx:  1
              Messages Rx:  216
              Sessions Total:  1
              Hold Timer Expireds Rx:  0
              Established State Count:  1
              OpenConfirm State Count:  0
              Updates Tx:  100
              Messages Tx:  216
              KeepAlives Tx:  115
              Graceful Restarts Failed:  0
              Graceful Restarts Attempted:  0
              Notifications Tx:  0
              Routes Rx:  100
              End of RIB Rx:  0
              Sessions Not Started:  0
              Sessions Configured:  1
              Notifications Rx:  0
              Idle State Count:  0
              Updates Rx:  100
              Opens Tx:  1
              Sessions Down:  0
              OpenSent State Count:  0
              Routes Withdrawn:  0
              Routes Advertised:  100
              Port:  2/1
              Active State Count:  0
              Hold Timer Expireds Tx:  0
              Routes Rx Graceful Restart:  0
              Connect State Count:  0
        '''
    #print()

try:
    stoppedTrafficFlag = 0
    displayLineOutputFlag = 0
    monitorTrafficItemList = None
    protocolSessionsToMonitor = None

    parameters = sys.argv[1:]
    argIndex = 0
    while argIndex < len(parameters):
        currentArg = parameters[argIndex]
        if currentArg == '-trafficName':
            # This list could be in regex
            monitorTrafficItemList = parameters[argIndex+1].split(' ')
            argIndex+=2
        elif currentArg == '-protocolSessions':
            protocolSessionsToMonitor = parameters[argIndex+1].split(' ')
            argIndex+=2
        elif currentArg == '-showTrafficItemNames':
            connect()
            #trafficItemList = Variables.sessionObj.getAllTrafficItemNames()
            trafficItemList = Variables.trafficObj.getAllTrafficItemNames()
            print('\n\nList of configured Traffic Item names:\n')
            for index in range(0, len(trafficItemList)):
                print('\t{0}:'.format(index+1), trafficItemList[index])
            print('\n\n')
            sys.exit()
        elif currentArg == '-apiServerIp':
            Variables.ixNetRestServerIp = parameters[argIndex+1]
            argIndex+=2
        elif currentArg == '-apiServerIpPort':
            Variables.ixNetRestServerPort = parameters[argIndex+1]
            argIndex+=2
        elif currentArg == '-frameLossThreshold':
            Variables.frameLossDeltaThreshold = int(parameters[argIndex+1])
            argIndex+=2
        elif currentArg == '-emailSendFrom':
            Variables.emailSendFrom = parameters[argIndex+1]
            argIndex+=2
        elif currentArg == '-emailPasswordFile':
            Variables.emailPasswordFile = parameters[argIndex+1]
            argIndex+=2
        elif currentArg == '-getStatInterval':
            Variables.getStatInterval = int(parameters[argIndex+1])
            argIndex+=2
        elif currentArg == '-recordStatsToFile':
            Variables.recordStatsToFile = True
            argIndex+=1
        elif currentArg == '-sendAlert':
            Variables.sendAlert = parameters[argIndex+1]
            Variables.sendAlert = True
            argIndex+=2
        elif currentArg == '-externalExecution':
            argIndex+=1
            Variables.externalExecution = True
        elif currentArg == '-displayMaxLines':
            Variables.displayMaxLineOutput = int(parameters[argIndex+1])
            argIndex+=2
        elif currentArg == '-connectToApiServer':
             Variables.connectToApiServer = parameters[argIndex+1]
             argIndex +=2
        elif currentArg == '-apiKey':
             Variables.apiKey = parameters[argIndex+1]
             argIndex +=2
        elif currentArg == '-sessionId':
             Variables.sessionId = int(parameters[argIndex+1])
             argIndex +=2
        elif currentArg == 'help':
            help()
            sys.exit()
        else:
            sys.exit('\nNo such parameter: %s\n' % currentArg)

    Variables.monitorTrafficColumnNames = Variables.displayMaxLineOutput

    connect()

    Variables.jsonData = {}

    if Variables.sendAlert == True:
        if Variables.emailPasswordFile != None:
            if os.path.exists(Variables.emailPasswordFile) == False:
                sys.exit('\nError: No such user email password file: %s' % Variables.emailPasswordFile)

            with open(Variables.emailPasswordFile) as getPassword:
                Variables.emailSenderPassword = getPassword.readline().strip()

    if monitorTrafficItemList and Variables.protocolSessionsToMonitor:
        sys.exit('\nError: Select either -trafficName or -protocolSessions')

    if protocolSessionsToMonitor:
        # Default the threshold to 1 flap
        if Variables.frameLossDeltaThreshold == 0:
            Variables.frameLossDeltaThreshold = 1

        for eachProtocol in protocolSessionsToMonitor:
            if eachProtocol == 'bgp':
                Variables.protocolSessionsToMonitor.append('BGP Peer Per Port')
            elif eachProtocol == 'ospf':
                Variables.protocolSessionsToMonitor.append('OSPFv2 RTR Per Port')
                eachProtocol = 'ospfv2'
            elif eachProtocol == 'igmp':
                Variables.protocolSessionsToMonitor.append('IGMP Host Per Port')
            elif eachProtocol == 'mld':
                Variables.protocolSessionsToMonitor.append('MLD Host Per Port')
            elif eachProtocol == 'pim':
                Variables.protocolSessionsToMonitor.append('PIMv6 IF Per Port')
            else:
                sys.exit('\nError: The protocol is not currently not supported and needs to be added in the app: %s' % eachProtocol)

            if Variables.recordStatsToFile:
                # Initialize the flag for each protocol. Used by monitorProtocol()
                Variables.statisticFileTopLineFlag[eachProtocol] = 0
                # Create a result file for each protocol session
                #with open(eachProtocol+'.stats', 'w') as newResultFile:
                #    newResultFile.write('')

                #with open(eachProtocol+'.json', 'w') as newResultFile:
                #    newResultFile.write('')

                Variables.jsonData.update({
                    eachProtocol: {
                        'columnNames': [],
                        'statistics': []
                    },
                })
                writeToJson(monitoring='protocol')

    if monitorTrafficItemList and not monitorTrafficItemList[0] == 'all':
        configuredTrafficItems = Variables.sessionObj.getAllTrafficItemNames()
        for monitorTrafficItemName in monitorTrafficItemList:
            discoveredTrafficItemFlag = 0
            for eachConfiguredTrafficItem in configuredTrafficItems:
                if bool(re.search(monitorTrafficItemName, eachConfiguredTrafficItem, re.I)) == True:
                    Variables.trafficItemsToMonitor.append(eachConfiguredTrafficItem)
                    Variables.sendEmailAlertOnceFlag[eachConfiguredTrafficItem] = 0
                    discoveredTrafficItemFlag = 1

                    if Variables.recordStatsToFile:
                        # Initialize the flag for each TrafficItem. Used by monitorTraffic()
                        Variables.statisticFileTopLineFlag[monitorTrafficItemName.split(' ')[0]] = 0
                        Variables.jsonData.update({
                            eachConfiguredTrafficItem: {
                                'columnNames': [],
                                'statistics': []
                            },
                        })
                        writeToJson(monitoring='traffic')

                        # Don't record a result file. Dangerous!  If monitoring for days or weeks continuously,
                        # the result file get huge without knowing it.
                        #
                        # Create a result file for each monitoring Traffic Item
                        #with open(eachConfiguredTrafficItem+'.stats', 'w') as newResultFile:
                        #    newResultFile.write('')
                        #with open(eachConfiguredTrafficItem+'.json', 'w') as newResultFile:
                        #    newResultFile.write('')
                    break

            if discoveredTrafficItemFlag == 0:
                errorMsg = '\n\nNo Traffic Item name found in configuration: {0}\n'.format(monitorTrafficItemName)
                errorMsg = errorMsg + '\n\tList of Configured Traffic Item names:\n\t{0}\n\n'.format(configuredTrafficItems)
                raise IxNetRestApiException(errorMsg)
    else:
        Variables.trafficItemNameToMonitor = Variables.sessionObj.getAllTrafficItemNames()
        for eachConfiguredTrafficItem in Variables.trafficItemNameToMonitor:
            Variables.trafficItemsToMonitor.append(eachConfiguredTrafficItem)
            Variables.sendEmailAlertOnceFlag[eachConfiguredTrafficItem] = 0
            discoveredTrafficItemFlag = 1

            if Variables.recordStatsToFile:
                # Initialize the flag for each TrafficItem. Used by monitorTraffic()
                Variables.statisticFileTopLineFlag[eachConfiguredTrafficItem.split(' ')[0]] = 0
                Variables.jsonData.update({
                    eachConfiguredTrafficItem: {
                        'columnNames': [],
                        'statistics': []
                    },
                })
                writeToJson(monitoring='traffic')

    while True:
        if monitorTrafficItemList:
            response = Variables.sessionObj.get(Variables.sessionUrl+'/traffic', silentMode=True)
            trafficState =  response.json()['state']

            if trafficState == 'started':
                monitorTraffic()
                stoppedTrafficFlag = 0

            if trafficState == 'stopped' and stoppedTrafficFlag == 0:
                monitorTraffic()
                print('\nTraffic is not running.  Waiting for traffic ...\n')
                stoppedTrafficFlag = 1

            if trafficState == 'stopped' and stoppedTrafficFlag == 1:
                time.sleep(1)
                continue

        if protocolSessionsToMonitor:
            monitorProtocol()

        if Variables.externalExecution == True:
            break

        time.sleep(Variables.getStatInterval)

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if not bool(re.search('ConnectionError', traceback.format_exc())):
        print('\n%s' % traceback.format_exc())
    #sys.exit('\nTest aborted. Traceback: {0}\n'.format(errMsg))
    sys.exit('\nTest aborted. Traceback: {0}\n'.format(traceback.format_exc()))




