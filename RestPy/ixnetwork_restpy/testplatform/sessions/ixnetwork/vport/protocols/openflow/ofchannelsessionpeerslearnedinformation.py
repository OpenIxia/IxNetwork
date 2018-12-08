
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


class OfChannelSessionPeersLearnedInformation(Base):
	"""The OfChannelSessionPeersLearnedInformation class encapsulates a system managed ofChannelSessionPeersLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelSessionPeersLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelSessionPeersLearnedInformation'

	def __init__(self, parent):
		super(OfChannelSessionPeersLearnedInformation, self).__init__(parent)

	@property
	def SwitchAuxiliaryConnectionLearnedInfo(self):
		"""An instance of the SwitchAuxiliaryConnectionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchauxiliaryconnectionlearnedinfo.SwitchAuxiliaryConnectionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchauxiliaryconnectionlearnedinfo import SwitchAuxiliaryConnectionLearnedInfo
		return SwitchAuxiliaryConnectionLearnedInfo(self)

	@property
	def AveragePacketInReplyDelay(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averagePacketInReplyDelay')

	@property
	def ConfiguredPacketInReplyCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('configuredPacketInReplyCount')

	@property
	def ConfiguredPacketInSentCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('configuredPacketInSentCount')

	@property
	def LocalPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localPortNumber')

	@property
	def MasterFlowRemovedMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('masterFlowRemovedMask')

	@property
	def MasterPacketInMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('masterPacketInMask')

	@property
	def MasterPortStatusMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('masterPortStatusMask')

	@property
	def PacketInTxRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetInTxRate')

	@property
	def PacketOutRxRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetOutRxRate')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remotePortNumber')

	@property
	def ReplyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def Role(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SlaveFlowRemovedMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('slaveFlowRemovedMask')

	@property
	def SlavePacketInMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('slavePacketInMask')

	@property
	def SlavePortStatusMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('slavePortStatusMask')

	def find(self, AveragePacketInReplyDelay=None, ConfiguredPacketInReplyCount=None, ConfiguredPacketInSentCount=None, LocalPortNumber=None, MasterFlowRemovedMask=None, MasterPacketInMask=None, MasterPortStatusMask=None, PacketInTxRate=None, PacketOutRxRate=None, RemoteIp=None, RemotePortNumber=None, ReplyState=None, Role=None, SlaveFlowRemovedMask=None, SlavePacketInMask=None, SlavePortStatusMask=None):
		"""Finds and retrieves ofChannelSessionPeersLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelSessionPeersLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelSessionPeersLearnedInformation data from the server.

		Args:
			AveragePacketInReplyDelay (str): 
			ConfiguredPacketInReplyCount (str): 
			ConfiguredPacketInSentCount (str): 
			LocalPortNumber (number): 
			MasterFlowRemovedMask (number): 
			MasterPacketInMask (number): 
			MasterPortStatusMask (number): 
			PacketInTxRate (number): 
			PacketOutRxRate (number): 
			RemoteIp (str): 
			RemotePortNumber (number): 
			ReplyState (str): 
			Role (str): 
			SlaveFlowRemovedMask (number): 
			SlavePacketInMask (number): 
			SlavePortStatusMask (number): 

		Returns:
			self: This instance with matching ofChannelSessionPeersLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelSessionPeersLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelSessionPeersLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
