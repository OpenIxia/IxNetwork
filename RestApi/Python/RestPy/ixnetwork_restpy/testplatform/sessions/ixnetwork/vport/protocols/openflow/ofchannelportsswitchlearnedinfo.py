from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfChannelPortsSwitchLearnedInfo(Base):
	"""The OfChannelPortsSwitchLearnedInfo class encapsulates a system managed ofChannelPortsSwitchLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelPortsSwitchLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelPortsSwitchLearnedInfo'

	def __init__(self, parent):
		super(OfChannelPortsSwitchLearnedInfo, self).__init__(parent)

	@property
	def AdvertisedFeatures(self):
		"""This describes the advertised features of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('advertisedFeatures')

	@property
	def Config(self):
		"""This describes the current configuration of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('config')

	@property
	def CurrentFeatures(self):
		"""This describes the current features of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('currentFeatures')

	@property
	def CurrentSpeed(self):
		"""This describes the current speed of the port.

		Returns:
			number
		"""
		return self._get_attribute('currentSpeed')

	@property
	def DataPathId(self):
		"""This describes the datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""This describes the datapath ID, in hexadecimal format, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def EthernetAddress(self):
		"""This describes the hardware address of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')

	@property
	def LocalIp(self):
		"""This describes the local IP of the switch.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MaximumSpeed(self):
		"""This describes the maximum speed of the port.

		Returns:
			number
		"""
		return self._get_attribute('maximumSpeed')

	@property
	def Name(self):
		"""This describes the name of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def PeerAdvertisedFeatures(self):
		"""This describes the peer advertised features of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('peerAdvertisedFeatures')

	@property
	def PortNumber(self):
		"""This describes the port number of the physical port.

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

	@property
	def RemoteIp(self):
		"""This describes the IP address of the remote end of the OF channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def State(self):
		"""This describes the current state of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def SupportedFeatures(self):
		"""This describes the supported features of the physical port.

		Returns:
			str
		"""
		return self._get_attribute('supportedFeatures')

	def find(self, AdvertisedFeatures=None, Config=None, CurrentFeatures=None, CurrentSpeed=None, DataPathId=None, DataPathIdAsHex=None, EthernetAddress=None, LocalIp=None, MaximumSpeed=None, Name=None, PeerAdvertisedFeatures=None, PortNumber=None, RemoteIp=None, State=None, SupportedFeatures=None):
		"""Finds and retrieves ofChannelPortsSwitchLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelPortsSwitchLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelPortsSwitchLearnedInfo data from the server.

		Args:
			AdvertisedFeatures (str): This describes the advertised features of the physical port.
			Config (str): This describes the current configuration of the physical port.
			CurrentFeatures (str): This describes the current features of the physical port.
			CurrentSpeed (number): This describes the current speed of the port.
			DataPathId (str): This describes the datapath ID of the switch.
			DataPathIdAsHex (str): This describes the datapath ID, in hexadecimal format, of the switch.
			EthernetAddress (str): This describes the hardware address of the physical port.
			LocalIp (str): This describes the local IP of the switch.
			MaximumSpeed (number): This describes the maximum speed of the port.
			Name (str): This describes the name of the physical port.
			PeerAdvertisedFeatures (str): This describes the peer advertised features of the physical port.
			PortNumber (number): This describes the port number of the physical port.
			RemoteIp (str): This describes the IP address of the remote end of the OF channel.
			State (str): This describes the current state of the physical port.
			SupportedFeatures (str): This describes the supported features of the physical port.

		Returns:
			self: This instance with matching ofChannelPortsSwitchLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelPortsSwitchLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelPortsSwitchLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
