"""
IxNetwork Watch feature pushes stats via web-socket when ever there is new stats.
This sample script assumes traffic configuration is already configured and
expects the user to manually start traffic.  Change to use API to start traffic if desired.

Dependencies
------------
- pip install ixnetwork-restpy
- pip install websocket-client
"""
from ixnetwork_restpy import SessionAssistant
import time

apiServerIp = '192.168.70.12'

# State which SesionName to connect to or which SessionId to connect to
session = SessionAssistant(IpAddress=apiServerIp, SessionName=None, SessionId=1,
                           ClearConfig=False, LogLevel='all', LogFilename='restpy.log')

ixNetwork = session.Ixnetwork

# State the stats to watch
watchPortCPU = ixNetwork.Statistics.View.find(Caption='^Port CPU Statistics$').Data
watchPortStats = ixNetwork.Statistics.View.find(Caption='^Port Statistics$').Data
watchTrafficItem = ixNetwork.Statistics.View.find(Caption='^Traffic Item Statistics$').Data

attributes_to_watch = ['pageValues']
topicPortCPU = 'Port CPU Statistics Watch'
topicPortStats = 'Port Statistics Watch'
topicTrafficItem = 'Traffic Item Statistics Watch'

# callback for watch notifications.
# Do all of your requirements in here.
# All message are in a dict object.
def my_printing_callback(ws, message):
    print(message)

watch_assistant = session.WatchAssistant(Callback=my_printing_callback)

watch_assistant.AddAttributeWatch(AttributesToWatch=attributes_to_watch, ObjectIdToWatch=watchPortCPU, Topic=topicPortCPU)
watch_assistant.AddAttributeWatch(AttributesToWatch=attributes_to_watch, ObjectIdToWatch=watchPortStats, Topic=topicPortStats)
watch_assistant.AddAttributeWatch(AttributesToWatch=attributes_to_watch, ObjectIdToWatch=watchTrafficItem, Topic=topicTrafficItem)

watch_assistant.start()

# Wait for notifications
time.sleep(30)

watch_assistant.stop()

