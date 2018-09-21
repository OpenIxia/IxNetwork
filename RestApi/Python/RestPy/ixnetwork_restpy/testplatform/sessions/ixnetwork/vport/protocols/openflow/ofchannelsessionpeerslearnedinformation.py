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
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('averagePacketInReplyDelay')

	@property
	def ConfiguredPacketInReplyCount(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('configuredPacketInReplyCount')

	@property
	def ConfiguredPacketInSentCount(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('configuredPacketInSentCount')

	@property
	def LocalPortNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('localPortNumber')

	@property
	def MasterFlowRemovedMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('masterFlowRemovedMask')

	@property
	def MasterPacketInMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('masterPacketInMask')

	@property
	def MasterPortStatusMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('masterPortStatusMask')

	@property
	def PacketInTxRate(self):
		"""Per second transmission rate of PacketIn messages from the time of protocol start. This is calculated only if Calculate PacketOut Rx Rate is enabled for the switch otherwise it is always 0.

		Returns:
			number
		"""
		return self._get_attribute('packetInTxRate')

	@property
	def PacketOutRxRate(self):
		"""Per second reception rate of PacketOut messages from the time of protocol start. This is calculated only if Calculate PacketOut Rx Rate is enabled for the switch otherwise it is always 0.

		Returns:
			number
		"""
		return self._get_attribute('packetOutRxRate')

	@property
	def RemoteIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePortNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('remotePortNumber')

	@property
	def ReplyState(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def Role(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SlaveFlowRemovedMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('slaveFlowRemovedMask')

	@property
	def SlavePacketInMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('slavePacketInMask')

	@property
	def SlavePortStatusMask(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('slavePortStatusMask')

	def find(self, AveragePacketInReplyDelay=None, ConfiguredPacketInReplyCount=None, ConfiguredPacketInSentCount=None, LocalPortNumber=None, MasterFlowRemovedMask=None, MasterPacketInMask=None, MasterPortStatusMask=None, PacketInTxRate=None, PacketOutRxRate=None, RemoteIp=None, RemotePortNumber=None, ReplyState=None, Role=None, SlaveFlowRemovedMask=None, SlavePacketInMask=None, SlavePortStatusMask=None):
		"""Finds and retrieves ofChannelSessionPeersLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelSessionPeersLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelSessionPeersLearnedInformation data from the server.

		Args:
			AveragePacketInReplyDelay (str): NOT DEFINED
			ConfiguredPacketInReplyCount (str): NOT DEFINED
			ConfiguredPacketInSentCount (str): NOT DEFINED
			LocalPortNumber (number): NOT DEFINED
			MasterFlowRemovedMask (number): NOT DEFINED
			MasterPacketInMask (number): NOT DEFINED
			MasterPortStatusMask (number): NOT DEFINED
			PacketInTxRate (number): Per second transmission rate of PacketIn messages from the time of protocol start. This is calculated only if Calculate PacketOut Rx Rate is enabled for the switch otherwise it is always 0.
			PacketOutRxRate (number): Per second reception rate of PacketOut messages from the time of protocol start. This is calculated only if Calculate PacketOut Rx Rate is enabled for the switch otherwise it is always 0.
			RemoteIp (str): NOT DEFINED
			RemotePortNumber (number): NOT DEFINED
			ReplyState (str): NOT DEFINED
			Role (str): NOT DEFINED
			SlaveFlowRemovedMask (number): NOT DEFINED
			SlavePacketInMask (number): NOT DEFINED
			SlavePortStatusMask (number): NOT DEFINED

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
