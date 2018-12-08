
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


class DestinationRange(Base):
	"""The DestinationRange class encapsulates a user managed destinationRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DestinationRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'destinationRange'

	def __init__(self, parent):
		super(DestinationRange, self).__init__(parent)

	@property
	def Egress(self):
		"""An instance of the Egress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.egress.Egress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.egress import Egress
		return Egress(self)._select()

	@property
	def Ingress(self):
		"""An instance of the Ingress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.ingress.Ingress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.ingress import Ingress
		return Ingress(self)._select()

	@property
	def TunnelLeafRange(self):
		"""An instance of the TunnelLeafRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelleafrange.TunnelLeafRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelleafrange import TunnelLeafRange
		return TunnelLeafRange(self)

	@property
	def TunnelTailTrafficEndPoint(self):
		"""An instance of the TunnelTailTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunneltailtrafficendpoint.TunnelTailTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunneltailtrafficendpoint import TunnelTailTrafficEndPoint
		return TunnelTailTrafficEndPoint(self)

	@property
	def Behavior(self):
		"""

		Returns:
			str(ingress|egress)
		"""
		return self._get_attribute('behavior')
	@Behavior.setter
	def Behavior(self, value):
		self._set_attribute('behavior', value)

	@property
	def EmulationType(self):
		"""

		Returns:
			str(reserved|rsvpTe|rsvpTeP2mP)
		"""
		return self._get_attribute('emulationType')
	@EmulationType.setter
	def EmulationType(self, value):
		self._set_attribute('emulationType', value)

	@property
	def EnableReplyingLspPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableReplyingLspPing')
	@EnableReplyingLspPing.setter
	def EnableReplyingLspPing(self, value):
		self._set_attribute('enableReplyingLspPing', value)

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
	def IpAddressFrom(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipAddressFrom')
	@IpAddressFrom.setter
	def IpAddressFrom(self, value):
		self._set_attribute('ipAddressFrom', value)

	@property
	def IpCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IsConnectedIpAppended(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isConnectedIpAppended')
	@IsConnectedIpAppended.setter
	def IsConnectedIpAppended(self, value):
		self._set_attribute('isConnectedIpAppended', value)

	@property
	def IsHeadIpPrepended(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isHeadIpPrepended')
	@IsHeadIpPrepended.setter
	def IsHeadIpPrepended(self, value):
		self._set_attribute('isHeadIpPrepended', value)

	@property
	def IsLeafIpPrepended(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLeafIpPrepended')
	@IsLeafIpPrepended.setter
	def IsLeafIpPrepended(self, value):
		self._set_attribute('isLeafIpPrepended', value)

	@property
	def IsSendingAsRro(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsRro')
	@IsSendingAsRro.setter
	def IsSendingAsRro(self, value):
		self._set_attribute('isSendingAsRro', value)

	@property
	def IsSendingAsSrro(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsSrro')
	@IsSendingAsSrro.setter
	def IsSendingAsSrro(self, value):
		self._set_attribute('isSendingAsSrro', value)

	@property
	def P2mpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('p2mpId')
	@P2mpId.setter
	def P2mpId(self, value):
		self._set_attribute('p2mpId', value)

	def add(self, Behavior=None, EmulationType=None, EnableReplyingLspPing=None, Enabled=None, IpAddressFrom=None, IpCount=None, IsConnectedIpAppended=None, IsHeadIpPrepended=None, IsLeafIpPrepended=None, IsSendingAsRro=None, IsSendingAsSrro=None, P2mpId=None):
		"""Adds a new destinationRange node on the server and retrieves it in this instance.

		Args:
			Behavior (str(ingress|egress)): 
			EmulationType (str(reserved|rsvpTe|rsvpTeP2mP)): 
			EnableReplyingLspPing (bool): 
			Enabled (bool): 
			IpAddressFrom (str): 
			IpCount (number): 
			IsConnectedIpAppended (bool): 
			IsHeadIpPrepended (bool): 
			IsLeafIpPrepended (bool): 
			IsSendingAsRro (bool): 
			IsSendingAsSrro (bool): 
			P2mpId (str): 

		Returns:
			self: This instance with all currently retrieved destinationRange data using find and the newly added destinationRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the destinationRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Behavior=None, EmulationType=None, EnableReplyingLspPing=None, Enabled=None, IpAddressFrom=None, IpCount=None, IsConnectedIpAppended=None, IsHeadIpPrepended=None, IsLeafIpPrepended=None, IsSendingAsRro=None, IsSendingAsSrro=None, P2mpId=None):
		"""Finds and retrieves destinationRange data from the server.

		All named parameters support regex and can be used to selectively retrieve destinationRange data from the server.
		By default the find method takes no parameters and will retrieve all destinationRange data from the server.

		Args:
			Behavior (str(ingress|egress)): 
			EmulationType (str(reserved|rsvpTe|rsvpTeP2mP)): 
			EnableReplyingLspPing (bool): 
			Enabled (bool): 
			IpAddressFrom (str): 
			IpCount (number): 
			IsConnectedIpAppended (bool): 
			IsHeadIpPrepended (bool): 
			IsLeafIpPrepended (bool): 
			IsSendingAsRro (bool): 
			IsSendingAsSrro (bool): 
			P2mpId (str): 

		Returns:
			self: This instance with matching destinationRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of destinationRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the destinationRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
