from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PortStatLearnedInformation(Base):
	"""The PortStatLearnedInformation class encapsulates a system managed portStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'portStatLearnedInformation'

	def __init__(self, parent):
		super(PortStatLearnedInformation, self).__init__(parent)

	@property
	def Collisions(self):
		"""Indicates the number of collisions.

		Returns:
			str
		"""
		return self._get_attribute('collisions')

	@property
	def CrcErrors(self):
		"""Signifies the number of CRC errors.

		Returns:
			str
		"""
		return self._get_attribute('crcErrors')

	@property
	def DataPathId(self):
		"""Signifies the datapath ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Signifies the datapath ID of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def Duration(self):
		"""The time in seconds, for which the port has been alive.

		Returns:
			number
		"""
		return self._get_attribute('duration')

	@property
	def DurationInNsec(self):
		"""The time in nanoseconds, for which the port has been alive beyond Duration (sec).

		Returns:
			number
		"""
		return self._get_attribute('durationInNsec')

	@property
	def ErrorCode(self):
		"""Signifies the error code of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""Signifies the type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def FrameAlignmentErrors(self):
		"""Signifies the number of Frame Alignment errors.

		Returns:
			str
		"""
		return self._get_attribute('frameAlignmentErrors')

	@property
	def Latency(self):
		"""Signifies the latency measurement for the OpenFlow channel in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""Signifies the local IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def PacketsDroppedByRx(self):
		"""Signifies the number of packets dropped by the receiving port.

		Returns:
			str
		"""
		return self._get_attribute('packetsDroppedByRx')

	@property
	def PacketsDroppedByTx(self):
		"""Signifies the number of packets dropped by the transmitting port.

		Returns:
			str
		"""
		return self._get_attribute('packetsDroppedByTx')

	@property
	def PacketsWithRxOverrun(self):
		"""Signifies the number of packets with received overruns.

		Returns:
			str
		"""
		return self._get_attribute('packetsWithRxOverrun')

	@property
	def PortNo(self):
		"""Signifies the port number used.

		Returns:
			number
		"""
		return self._get_attribute('portNo')

	@property
	def ReceivedBytes(self):
		"""Signifies the number of bytes received.

		Returns:
			str
		"""
		return self._get_attribute('receivedBytes')

	@property
	def ReceivedErrors(self):
		"""Signifies the number of received errors.

		Returns:
			str
		"""
		return self._get_attribute('receivedErrors')

	@property
	def ReceivedPackets(self):
		"""Signifies the number of packets received.

		Returns:
			str
		"""
		return self._get_attribute('receivedPackets')

	@property
	def RemoteIp(self):
		"""Signifies the Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Signifies the reply state of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def TransmitErrors(self):
		"""Signifies the number of Transmit errors.

		Returns:
			str
		"""
		return self._get_attribute('transmitErrors')

	@property
	def TransmittedBytes(self):
		"""Signifies the number of bytes transmitted.

		Returns:
			str
		"""
		return self._get_attribute('transmittedBytes')

	@property
	def TransmittedPackets(self):
		"""Signifies the number of packets transmitted.

		Returns:
			str
		"""
		return self._get_attribute('transmittedPackets')

	def find(self, Collisions=None, CrcErrors=None, DataPathId=None, DataPathIdAsHex=None, Duration=None, DurationInNsec=None, ErrorCode=None, ErrorType=None, FrameAlignmentErrors=None, Latency=None, LocalIp=None, NegotiatedVersion=None, PacketsDroppedByRx=None, PacketsDroppedByTx=None, PacketsWithRxOverrun=None, PortNo=None, ReceivedBytes=None, ReceivedErrors=None, ReceivedPackets=None, RemoteIp=None, ReplyState=None, TransmitErrors=None, TransmittedBytes=None, TransmittedPackets=None):
		"""Finds and retrieves portStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve portStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all portStatLearnedInformation data from the server.

		Args:
			Collisions (str): Indicates the number of collisions.
			CrcErrors (str): Signifies the number of CRC errors.
			DataPathId (str): Signifies the datapath ID of the OpenFlow switch.
			DataPathIdAsHex (str): Signifies the datapath ID of the OpenFlow switch in hexadecimal format.
			Duration (number): The time in seconds, for which the port has been alive.
			DurationInNsec (number): The time in nanoseconds, for which the port has been alive beyond Duration (sec).
			ErrorCode (str): Signifies the error code of the error received.
			ErrorType (str): Signifies the type of the error received.
			FrameAlignmentErrors (str): Signifies the number of Frame Alignment errors.
			Latency (number): Signifies the latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): Signifies the local IP address of the selected interface.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			PacketsDroppedByRx (str): Signifies the number of packets dropped by the receiving port.
			PacketsDroppedByTx (str): Signifies the number of packets dropped by the transmitting port.
			PacketsWithRxOverrun (str): Signifies the number of packets with received overruns.
			PortNo (number): Signifies the port number used.
			ReceivedBytes (str): Signifies the number of bytes received.
			ReceivedErrors (str): Signifies the number of received errors.
			ReceivedPackets (str): Signifies the number of packets received.
			RemoteIp (str): Signifies the Remote IP address of the selected interface.
			ReplyState (str): Signifies the reply state of the OF Channel.
			TransmitErrors (str): Signifies the number of Transmit errors.
			TransmittedBytes (str): Signifies the number of bytes transmitted.
			TransmittedPackets (str): Signifies the number of packets transmitted.

		Returns:
			self: This instance with matching portStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of portStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the portStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
