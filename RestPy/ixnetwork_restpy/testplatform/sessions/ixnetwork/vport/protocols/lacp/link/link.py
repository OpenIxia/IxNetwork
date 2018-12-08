
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorKey')
	@ActorKey.setter
	def ActorKey(self, value):
		self._set_attribute('actorKey', value)

	@property
	def ActorPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorPortNumber')
	@ActorPortNumber.setter
	def ActorPortNumber(self, value):
		self._set_attribute('actorPortNumber', value)

	@property
	def ActorPortPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorPortPriority')
	@ActorPortPriority.setter
	def ActorPortPriority(self, value):
		self._set_attribute('actorPortPriority', value)

	@property
	def ActorSystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actorSystemId')
	@ActorSystemId.setter
	def ActorSystemId(self, value):
		self._set_attribute('actorSystemId', value)

	@property
	def ActorSystemPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actorSystemPriority')
	@ActorSystemPriority.setter
	def ActorSystemPriority(self, value):
		self._set_attribute('actorSystemPriority', value)

	@property
	def AdministrativeKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('administrativeKey')
	@AdministrativeKey.setter
	def AdministrativeKey(self, value):
		self._set_attribute('administrativeKey', value)

	@property
	def AggregationFlagState(self):
		"""

		Returns:
			str(disable|auto)
		"""
		return self._get_attribute('aggregationFlagState')
	@AggregationFlagState.setter
	def AggregationFlagState(self, value):
		self._set_attribute('aggregationFlagState', value)

	@property
	def AutoPickPortMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoPickPortMac')
	@AutoPickPortMac.setter
	def AutoPickPortMac(self, value):
		self._set_attribute('autoPickPortMac', value)

	@property
	def CollectingFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('collectingFlag')
	@CollectingFlag.setter
	def CollectingFlag(self, value):
		self._set_attribute('collectingFlag', value)

	@property
	def CollectorMaxDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('collectorMaxDelay')
	@CollectorMaxDelay.setter
	def CollectorMaxDelay(self, value):
		self._set_attribute('collectorMaxDelay', value)

	@property
	def DistributingFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('distributingFlag')
	@DistributingFlag.setter
	def DistributingFlag(self, value):
		self._set_attribute('distributingFlag', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterMarkerPduDelay(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interMarkerPduDelay')
	@InterMarkerPduDelay.setter
	def InterMarkerPduDelay(self, value):
		self._set_attribute('interMarkerPduDelay', value)

	@property
	def LacpActivity(self):
		"""

		Returns:
			str(active|passive)
		"""
		return self._get_attribute('lacpActivity')
	@LacpActivity.setter
	def LacpActivity(self, value):
		self._set_attribute('lacpActivity', value)

	@property
	def LacpTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lacpTimeout')
	@LacpTimeout.setter
	def LacpTimeout(self, value):
		self._set_attribute('lacpTimeout', value)

	@property
	def LacpduPeriodicTimeInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lacpduPeriodicTimeInterval')
	@LacpduPeriodicTimeInterval.setter
	def LacpduPeriodicTimeInterval(self, value):
		self._set_attribute('lacpduPeriodicTimeInterval', value)

	@property
	def MarkerRequestMode(self):
		"""

		Returns:
			str(fixed|random)
		"""
		return self._get_attribute('markerRequestMode')
	@MarkerRequestMode.setter
	def MarkerRequestMode(self, value):
		self._set_attribute('markerRequestMode', value)

	@property
	def MarkerResponseWaitTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('markerResponseWaitTime')
	@MarkerResponseWaitTime.setter
	def MarkerResponseWaitTime(self, value):
		self._set_attribute('markerResponseWaitTime', value)

	@property
	def PortMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('portMac')
	@PortMac.setter
	def PortMac(self, value):
		self._set_attribute('portMac', value)

	@property
	def SendMarkerRequestOnLagChange(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendMarkerRequestOnLagChange')
	@SendMarkerRequestOnLagChange.setter
	def SendMarkerRequestOnLagChange(self, value):
		self._set_attribute('sendMarkerRequestOnLagChange', value)

	@property
	def SendPeriodicMarkerRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendPeriodicMarkerRequest')
	@SendPeriodicMarkerRequest.setter
	def SendPeriodicMarkerRequest(self, value):
		self._set_attribute('sendPeriodicMarkerRequest', value)

	@property
	def SupportRespondingToMarker(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportRespondingToMarker')
	@SupportRespondingToMarker.setter
	def SupportRespondingToMarker(self, value):
		self._set_attribute('supportRespondingToMarker', value)

	@property
	def SyncFlag(self):
		"""

		Returns:
			str(disable|auto)
		"""
		return self._get_attribute('syncFlag')
	@SyncFlag.setter
	def SyncFlag(self, value):
		self._set_attribute('syncFlag', value)

	@property
	def UpdateRequired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')

	def add(self, ActorKey=None, ActorPortNumber=None, ActorPortPriority=None, ActorSystemId=None, ActorSystemPriority=None, AdministrativeKey=None, AggregationFlagState=None, AutoPickPortMac=None, CollectingFlag=None, CollectorMaxDelay=None, DistributingFlag=None, Enabled=None, InterMarkerPduDelay=None, LacpActivity=None, LacpTimeout=None, LacpduPeriodicTimeInterval=None, MarkerRequestMode=None, MarkerResponseWaitTime=None, PortMac=None, SendMarkerRequestOnLagChange=None, SendPeriodicMarkerRequest=None, SupportRespondingToMarker=None, SyncFlag=None):
		"""Adds a new link node on the server and retrieves it in this instance.

		Args:
			ActorKey (number): 
			ActorPortNumber (number): 
			ActorPortPriority (number): 
			ActorSystemId (str): 
			ActorSystemPriority (number): 
			AdministrativeKey (number): 
			AggregationFlagState (str(disable|auto)): 
			AutoPickPortMac (bool): 
			CollectingFlag (bool): 
			CollectorMaxDelay (number): 
			DistributingFlag (bool): 
			Enabled (bool): 
			InterMarkerPduDelay (str): 
			LacpActivity (str(active|passive)): 
			LacpTimeout (number): 
			LacpduPeriodicTimeInterval (number): 
			MarkerRequestMode (str(fixed|random)): 
			MarkerResponseWaitTime (number): 
			PortMac (str): 
			SendMarkerRequestOnLagChange (bool): 
			SendPeriodicMarkerRequest (bool): 
			SupportRespondingToMarker (bool): 
			SyncFlag (str(disable|auto)): 

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
			ActorKey (number): 
			ActorPortNumber (number): 
			ActorPortPriority (number): 
			ActorSystemId (str): 
			ActorSystemPriority (number): 
			AdministrativeKey (number): 
			AggregationFlagState (str(disable|auto)): 
			AutoPickPortMac (bool): 
			CollectingFlag (bool): 
			CollectorMaxDelay (number): 
			DistributingFlag (bool): 
			Enabled (bool): 
			InterMarkerPduDelay (str): 
			LacpActivity (str(active|passive)): 
			LacpTimeout (number): 
			LacpduPeriodicTimeInterval (number): 
			MarkerRequestMode (str(fixed|random)): 
			MarkerResponseWaitTime (number): 
			PortMac (str): 
			SendMarkerRequestOnLagChange (bool): 
			SendPeriodicMarkerRequest (bool): 
			SupportRespondingToMarker (bool): 
			SyncFlag (str(disable|auto)): 
			UpdateRequired (bool): 

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
