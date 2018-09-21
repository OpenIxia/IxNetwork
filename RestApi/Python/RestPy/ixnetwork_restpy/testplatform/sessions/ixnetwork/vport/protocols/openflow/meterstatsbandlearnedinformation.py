from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeterStatsBandLearnedInformation(Base):
	"""The MeterStatsBandLearnedInformation class encapsulates a system managed meterStatsBandLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterStatsBandLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterStatsBandLearnedInformation'

	def __init__(self, parent):
		super(MeterStatsBandLearnedInformation, self).__init__(parent)

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
	def InBandByteCount(self):
		"""Specifies Byte Band Count

		Returns:
			number
		"""
		return self._get_attribute('inBandByteCount')

	@property
	def InBandPacketCount(self):
		"""Specifies Packet Band Count

		Returns:
			number
		"""
		return self._get_attribute('inBandPacketCount')

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
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	def find(self, DataPathId=None, DataPathIdAsHex=None, InBandByteCount=None, InBandPacketCount=None, LocalIp=None, MeterId=None, RemoteIp=None):
		"""Finds and retrieves meterStatsBandLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterStatsBandLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterStatsBandLearnedInformation data from the server.

		Args:
			DataPathId (number): The Data Path identifier of the OpenFlow controller.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow controller in hexadecimal format.
			InBandByteCount (number): Specifies Byte Band Count
			InBandPacketCount (number): Specifies Packet Band Count
			LocalIp (str): Indicates the local IP of the Controller.
			MeterId (number): Specifies Meter ID
			RemoteIp (str): The Remote IP address of the selected interface.

		Returns:
			self: This instance with matching meterStatsBandLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterStatsBandLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterStatsBandLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
