from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Link(Base):
	"""The Link class encapsulates a user managed link node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Link property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'link'

	def __init__(self, parent):
		super(Link, self).__init__(parent)

	@property
	def ActorKey(self):
		"""The operational Key value assigned to the port by the Actor. This is a 2 byte field with a default of 1. Minimum value is 0, maximum value is 65535.

		Returns:
			number
		"""
		return self._get_attribute('actorKey')
	@ActorKey.setter
	def ActorKey(self, value):
		self._set_attribute('actorKey', value)

	@property
	def ActorPortNumber(self):
		"""The port number assigned to the port by the Actor (the System sending the PDU). It is a 2 byte field with a default of 1. Min: 0, Max: 65535.

		Returns:
			number
		"""
		return self._get_attribute('actorPortNumber')
	@ActorPortNumber.setter
	def ActorPortNumber(self, value):
		self._set_attribute('actorPortNumber', value)

	@property
	def ActorPortPriority(self):
		"""This field specifies the port priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.

		Returns:
			number
		"""
		return self._get_attribute('actorPortPriority')
	@ActorPortPriority.setter
	def ActorPortPriority(self, value):
		self._set_attribute('actorPortPriority', value)

	@property
	def ActorSystemId(self):
		"""This field specifies the system identifier for the link Actor. It is a 6 byte field, with a default of 00-00-00-00-00-01. Min: 00-00-00-00-00-00, Max: FF-FF-FF-FF-FF-FF.

		Returns:
			str
		"""
		return self._get_attribute('actorSystemId')
	@ActorSystemId.setter
	def ActorSystemId(self, value):
		self._set_attribute('actorSystemId', value)

	@property
	def ActorSystemPriority(self):
		"""This field specifies the system priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.

		Returns:
			number
		"""
		return self._get_attribute('actorSystemPriority')
	@ActorSystemPriority.setter
	def ActorSystemPriority(self, value):
		self._set_attribute('actorSystemPriority', value)

	@property
	def AdministrativeKey(self):
		"""This field controls the aggregation of ports of the same system with similar Actor Key.

		Returns:
			number
		"""
		return self._get_attribute('administrativeKey')
	@AdministrativeKey.setter
	def AdministrativeKey(self, value):
		self._set_attribute('administrativeKey', value)

	@property
	def AggregationFlagState(self):
		"""If enabled, sets the port status to automatically allow aggregation.

		Returns:
			str(disable|auto)
		"""
		return self._get_attribute('aggregationFlagState')
	@AggregationFlagState.setter
	def AggregationFlagState(self, value):
		self._set_attribute('aggregationFlagState', value)

	@property
	def AutoPickPortMac(self):
		"""If true the source MAC is the interface MAC address.

		Returns:
			bool
		"""
		return self._get_attribute('autoPickPortMac')
	@AutoPickPortMac.setter
	def AutoPickPortMac(self, value):
		self._set_attribute('autoPickPortMac', value)

	@property
	def CollectingFlag(self):
		"""If true, the actor port state Collecting is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent

		Returns:
			bool
		"""
		return self._get_attribute('collectingFlag')
	@CollectingFlag.setter
	def CollectingFlag(self, value):
		self._set_attribute('collectingFlag', value)

	@property
	def CollectorMaxDelay(self):
		"""The maximum time in microseconds that the Frame Collector may delay the delivery of a frame received from an Aggregator to its MAC client. This is a 2 byte field with a default 0. Min: 0, Max: 65535.

		Returns:
			number
		"""
		return self._get_attribute('collectorMaxDelay')
	@CollectorMaxDelay.setter
	def CollectorMaxDelay(self, value):
		self._set_attribute('collectorMaxDelay', value)

	@property
	def DistributingFlag(self):
		"""If true, the actor port state Distributing is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.

		Returns:
			bool
		"""
		return self._get_attribute('distributingFlag')
	@DistributingFlag.setter
	def DistributingFlag(self, value):
		self._set_attribute('distributingFlag', value)

	@property
	def Enabled(self):
		"""If true, the link is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterMarkerPduDelay(self):
		"""The time gap in seconds between two consecutive Marker PDUs when transmitted periodically.

		Returns:
			str
		"""
		return self._get_attribute('interMarkerPduDelay')
	@InterMarkerPduDelay.setter
	def InterMarkerPduDelay(self, value):
		self._set_attribute('interMarkerPduDelay', value)

	@property
	def LacpActivity(self):
		"""Sets the value of LACPs Actor activity, either passive or active.

		Returns:
			str(active|passive)
		"""
		return self._get_attribute('lacpActivity')
	@LacpActivity.setter
	def LacpActivity(self, value):
		self._set_attribute('lacpActivity', value)

	@property
	def LacpTimeout(self):
		"""This timer is used to detect whether received protocol information has expired. The user can provide a custom value from 1 to 65535.

		Returns:
			number
		"""
		return self._get_attribute('lacpTimeout')
	@LacpTimeout.setter
	def LacpTimeout(self, value):
		self._set_attribute('lacpTimeout', value)

	@property
	def LacpduPeriodicTimeInterval(self):
		"""This field defines how frequently LACPDUs are sent to the link partner. The user can provide a custom values from 1 to 65535, in seconds

		Returns:
			number
		"""
		return self._get_attribute('lacpduPeriodicTimeInterval')
	@LacpduPeriodicTimeInterval.setter
	def LacpduPeriodicTimeInterval(self, value):
		self._set_attribute('lacpduPeriodicTimeInterval', value)

	@property
	def MarkerRequestMode(self):
		"""Sets the marker request mode for the Actor link.In either case, the mode parameters are specified in Marker Request Frequency.

		Returns:
			str(fixed|random)
		"""
		return self._get_attribute('markerRequestMode')
	@MarkerRequestMode.setter
	def MarkerRequestMode(self, value):
		self._set_attribute('markerRequestMode', value)

	@property
	def MarkerResponseWaitTime(self):
		"""The number of seconds to wait for Marker Response after sending a Marker Request. After this time, the Marker Response Timeout Count is incremented. If a marker response does arrive for the request after this timeout, it is not considered as a legitimate response.

		Returns:
			number
		"""
		return self._get_attribute('markerResponseWaitTime')
	@MarkerResponseWaitTime.setter
	def MarkerResponseWaitTime(self, value):
		self._set_attribute('markerResponseWaitTime', value)

	@property
	def PortMac(self):
		"""specifies the port MAC address.

		Returns:
			str
		"""
		return self._get_attribute('portMac')
	@PortMac.setter
	def PortMac(self, value):
		self._set_attribute('portMac', value)

	@property
	def SendMarkerRequestOnLagChange(self):
		"""If true, this checkbox causes LACP to send a Marker PDU on the following situations: 1) System Priority has been modified; 2) System Id has been modified; 3) Actor Key has been modified; 4) Port Number/Port Priority has been modified while we are in Individual mode.

		Returns:
			bool
		"""
		return self._get_attribute('sendMarkerRequestOnLagChange')
	@SendMarkerRequestOnLagChange.setter
	def SendMarkerRequestOnLagChange(self, value):
		self._set_attribute('sendMarkerRequestOnLagChange', value)

	@property
	def SendPeriodicMarkerRequest(self):
		"""If true, Marker Request PDUs are periodically after both actor and partner are IN SYNC and our state is aggregated. The moment we come out of this state, the periodic sending of Marker will be stopped.

		Returns:
			bool
		"""
		return self._get_attribute('sendPeriodicMarkerRequest')
	@SendPeriodicMarkerRequest.setter
	def SendPeriodicMarkerRequest(self, value):
		self._set_attribute('sendPeriodicMarkerRequest', value)

	@property
	def SupportRespondingToMarker(self):
		"""If true, LACP doesn't respond to MARKER request PDUs from the partner.

		Returns:
			bool
		"""
		return self._get_attribute('supportRespondingToMarker')
	@SupportRespondingToMarker.setter
	def SupportRespondingToMarker(self, value):
		self._set_attribute('supportRespondingToMarker', value)

	@property
	def SyncFlag(self):
		"""If enabled, the actor port state is set to True based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.

		Returns:
			str(disable|auto)
		"""
		return self._get_attribute('syncFlag')
	@SyncFlag.setter
	def SyncFlag(self, value):
		self._set_attribute('syncFlag', value)

	@property
	def UpdateRequired(self):
		"""(read only) If true, an update LAPDU is required for the link.

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')

	def add(self, ActorKey=None, ActorPortNumber=None, ActorPortPriority=None, ActorSystemId=None, ActorSystemPriority=None, AdministrativeKey=None, AggregationFlagState=None, AutoPickPortMac=None, CollectingFlag=None, CollectorMaxDelay=None, DistributingFlag=None, Enabled=None, InterMarkerPduDelay=None, LacpActivity=None, LacpTimeout=None, LacpduPeriodicTimeInterval=None, MarkerRequestMode=None, MarkerResponseWaitTime=None, PortMac=None, SendMarkerRequestOnLagChange=None, SendPeriodicMarkerRequest=None, SupportRespondingToMarker=None, SyncFlag=None):
		"""Adds a new link node on the server and retrieves it in this instance.

		Args:
			ActorKey (number): The operational Key value assigned to the port by the Actor. This is a 2 byte field with a default of 1. Minimum value is 0, maximum value is 65535.
			ActorPortNumber (number): The port number assigned to the port by the Actor (the System sending the PDU). It is a 2 byte field with a default of 1. Min: 0, Max: 65535.
			ActorPortPriority (number): This field specifies the port priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.
			ActorSystemId (str): This field specifies the system identifier for the link Actor. It is a 6 byte field, with a default of 00-00-00-00-00-01. Min: 00-00-00-00-00-00, Max: FF-FF-FF-FF-FF-FF.
			ActorSystemPriority (number): This field specifies the system priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.
			AdministrativeKey (number): This field controls the aggregation of ports of the same system with similar Actor Key.
			AggregationFlagState (str(disable|auto)): If enabled, sets the port status to automatically allow aggregation.
			AutoPickPortMac (bool): If true the source MAC is the interface MAC address.
			CollectingFlag (bool): If true, the actor port state Collecting is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent
			CollectorMaxDelay (number): The maximum time in microseconds that the Frame Collector may delay the delivery of a frame received from an Aggregator to its MAC client. This is a 2 byte field with a default 0. Min: 0, Max: 65535.
			DistributingFlag (bool): If true, the actor port state Distributing is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.
			Enabled (bool): If true, the link is enabled.
			InterMarkerPduDelay (str): The time gap in seconds between two consecutive Marker PDUs when transmitted periodically.
			LacpActivity (str(active|passive)): Sets the value of LACPs Actor activity, either passive or active.
			LacpTimeout (number): This timer is used to detect whether received protocol information has expired. The user can provide a custom value from 1 to 65535.
			LacpduPeriodicTimeInterval (number): This field defines how frequently LACPDUs are sent to the link partner. The user can provide a custom values from 1 to 65535, in seconds
			MarkerRequestMode (str(fixed|random)): Sets the marker request mode for the Actor link.In either case, the mode parameters are specified in Marker Request Frequency.
			MarkerResponseWaitTime (number): The number of seconds to wait for Marker Response after sending a Marker Request. After this time, the Marker Response Timeout Count is incremented. If a marker response does arrive for the request after this timeout, it is not considered as a legitimate response.
			PortMac (str): specifies the port MAC address.
			SendMarkerRequestOnLagChange (bool): If true, this checkbox causes LACP to send a Marker PDU on the following situations: 1) System Priority has been modified; 2) System Id has been modified; 3) Actor Key has been modified; 4) Port Number/Port Priority has been modified while we are in Individual mode.
			SendPeriodicMarkerRequest (bool): If true, Marker Request PDUs are periodically after both actor and partner are IN SYNC and our state is aggregated. The moment we come out of this state, the periodic sending of Marker will be stopped.
			SupportRespondingToMarker (bool): If true, LACP doesn't respond to MARKER request PDUs from the partner.
			SyncFlag (str(disable|auto)): If enabled, the actor port state is set to True based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.

		Returns:
			self: This instance with all currently retrieved link data using find and the newly added link data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the link data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActorKey=None, ActorPortNumber=None, ActorPortPriority=None, ActorSystemId=None, ActorSystemPriority=None, AdministrativeKey=None, AggregationFlagState=None, AutoPickPortMac=None, CollectingFlag=None, CollectorMaxDelay=None, DistributingFlag=None, Enabled=None, InterMarkerPduDelay=None, LacpActivity=None, LacpTimeout=None, LacpduPeriodicTimeInterval=None, MarkerRequestMode=None, MarkerResponseWaitTime=None, PortMac=None, SendMarkerRequestOnLagChange=None, SendPeriodicMarkerRequest=None, SupportRespondingToMarker=None, SyncFlag=None, UpdateRequired=None):
		"""Finds and retrieves link data from the server.

		All named parameters support regex and can be used to selectively retrieve link data from the server.
		By default the find method takes no parameters and will retrieve all link data from the server.

		Args:
			ActorKey (number): The operational Key value assigned to the port by the Actor. This is a 2 byte field with a default of 1. Minimum value is 0, maximum value is 65535.
			ActorPortNumber (number): The port number assigned to the port by the Actor (the System sending the PDU). It is a 2 byte field with a default of 1. Min: 0, Max: 65535.
			ActorPortPriority (number): This field specifies the port priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.
			ActorSystemId (str): This field specifies the system identifier for the link Actor. It is a 6 byte field, with a default of 00-00-00-00-00-01. Min: 00-00-00-00-00-00, Max: FF-FF-FF-FF-FF-FF.
			ActorSystemPriority (number): This field specifies the system priority of the link Actor. It is a 2 byte field, with a default or 1. Min: 0, Max: 65535.
			AdministrativeKey (number): This field controls the aggregation of ports of the same system with similar Actor Key.
			AggregationFlagState (str(disable|auto)): If enabled, sets the port status to automatically allow aggregation.
			AutoPickPortMac (bool): If true the source MAC is the interface MAC address.
			CollectingFlag (bool): If true, the actor port state Collecting is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent
			CollectorMaxDelay (number): The maximum time in microseconds that the Frame Collector may delay the delivery of a frame received from an Aggregator to its MAC client. This is a 2 byte field with a default 0. Min: 0, Max: 65535.
			DistributingFlag (bool): If true, the actor port state Distributing is set to true based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.
			Enabled (bool): If true, the link is enabled.
			InterMarkerPduDelay (str): The time gap in seconds between two consecutive Marker PDUs when transmitted periodically.
			LacpActivity (str(active|passive)): Sets the value of LACPs Actor activity, either passive or active.
			LacpTimeout (number): This timer is used to detect whether received protocol information has expired. The user can provide a custom value from 1 to 65535.
			LacpduPeriodicTimeInterval (number): This field defines how frequently LACPDUs are sent to the link partner. The user can provide a custom values from 1 to 65535, in seconds
			MarkerRequestMode (str(fixed|random)): Sets the marker request mode for the Actor link.In either case, the mode parameters are specified in Marker Request Frequency.
			MarkerResponseWaitTime (number): The number of seconds to wait for Marker Response after sending a Marker Request. After this time, the Marker Response Timeout Count is incremented. If a marker response does arrive for the request after this timeout, it is not considered as a legitimate response.
			PortMac (str): specifies the port MAC address.
			SendMarkerRequestOnLagChange (bool): If true, this checkbox causes LACP to send a Marker PDU on the following situations: 1) System Priority has been modified; 2) System Id has been modified; 3) Actor Key has been modified; 4) Port Number/Port Priority has been modified while we are in Individual mode.
			SendPeriodicMarkerRequest (bool): If true, Marker Request PDUs are periodically after both actor and partner are IN SYNC and our state is aggregated. The moment we come out of this state, the periodic sending of Marker will be stopped.
			SupportRespondingToMarker (bool): If true, LACP doesn't respond to MARKER request PDUs from the partner.
			SyncFlag (str(disable|auto)): If enabled, the actor port state is set to True based on Tx and Rx state machines. Otherwise, the flag in LACPDU remains reset for all packets sent.
			UpdateRequired (bool): (read only) If true, an update LAPDU is required for the link.

		Returns:
			self: This instance with matching link data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of link data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the link data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
