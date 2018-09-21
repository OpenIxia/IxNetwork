from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeterStatsLearnedInformation(Base):
	"""The MeterStatsLearnedInformation class encapsulates a system managed meterStatsLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterStatsLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterStatsLearnedInformation'

	def __init__(self, parent):
		super(MeterStatsLearnedInformation, self).__init__(parent)

	@property
	def MeterStatsBandLearnedInformation(self):
		"""An instance of the MeterStatsBandLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterstatsbandlearnedinformation.MeterStatsBandLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterstatsbandlearnedinformation import MeterStatsBandLearnedInformation
		return MeterStatsBandLearnedInformation(self)

	@property
	def ByteInCount(self):
		"""Specifies Byte in Count

		Returns:
			number
		"""
		return self._get_attribute('byteInCount')

	@property
	def DataPathId(self):
		"""The Data Path identifier of the OpenFlow controller.

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path identifier of the OpenFlow controller in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def DurationNSec(self):
		"""Specifies Duration Nano Second

		Returns:
			number
		"""
		return self._get_attribute('durationNSec')

	@property
	def DurationSec(self):
		"""Specifies Duration in Second

		Returns:
			number
		"""
		return self._get_attribute('durationSec')

	@property
	def ErrorCode(self):
		"""The error code of the received error.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""The type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def FlowCount(self):
		"""Specifies the Flow Count

		Returns:
			number
		"""
		return self._get_attribute('flowCount')

	@property
	def LastErrorCode(self):
		"""The Last error code of the received error.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""The type of the Last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

	@property
	def Latency(self):
		"""The latency measurement for the OpenFlow channel in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""Indicates the local IP of the Controller.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MeterId(self):
		"""Specifies Meter ID

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfBandStats(self):
		"""Specifies the number of band

		Returns:
			number
		"""
		return self._get_attribute('numberOfBandStats')

	@property
	def PacketInCount(self):
		"""Specifies Packet In Count

		Returns:
			number
		"""
		return self._get_attribute('packetInCount')

	@property
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""The state of reply for the Open Flow channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, ByteInCount=None, DataPathId=None, DataPathIdAsHex=None, DurationNSec=None, DurationSec=None, ErrorCode=None, ErrorType=None, FlowCount=None, LastErrorCode=None, LastErrorType=None, Latency=None, LocalIp=None, MeterId=None, NegotiatedVersion=None, NumberOfBandStats=None, PacketInCount=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves meterStatsLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterStatsLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterStatsLearnedInformation data from the server.

		Args:
			ByteInCount (number): Specifies Byte in Count
			DataPathId (number): The Data Path identifier of the OpenFlow controller.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow controller in hexadecimal format.
			DurationNSec (number): Specifies Duration Nano Second
			DurationSec (number): Specifies Duration in Second
			ErrorCode (str): The error code of the received error.
			ErrorType (str): The type of the error received.
			FlowCount (number): Specifies the Flow Count
			LastErrorCode (str): The Last error code of the received error.
			LastErrorType (str): The type of the Last error received.
			Latency (number): The latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): Indicates the local IP of the Controller.
			MeterId (number): Specifies Meter ID
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			NumberOfBandStats (number): Specifies the number of band
			PacketInCount (number): Specifies Packet In Count
			RemoteIp (str): The Remote IP address of the selected interface.
			ReplyState (str): The state of reply for the Open Flow channel.

		Returns:
			self: This instance with matching meterStatsLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterStatsLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterStatsLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
