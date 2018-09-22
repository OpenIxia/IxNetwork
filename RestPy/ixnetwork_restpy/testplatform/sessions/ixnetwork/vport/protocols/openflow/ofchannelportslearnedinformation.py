from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfChannelPortsLearnedInformation(Base):
	"""The OfChannelPortsLearnedInformation class encapsulates a system managed ofChannelPortsLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelPortsLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelPortsLearnedInformation'

	def __init__(self, parent):
		super(OfChannelPortsLearnedInformation, self).__init__(parent)

	@property
	def AdvertisedFeatures(self):
		"""Signifies the advertised features of the port.

		Returns:
			str
		"""
		return self._get_attribute('advertisedFeatures')

	@property
	def Config(self):
		"""Signifies the configuration name.

		Returns:
			str
		"""
		return self._get_attribute('config')

	@property
	def CurrentFeatures(self):
		"""Signifies the current features of the port.

		Returns:
			str
		"""
		return self._get_attribute('currentFeatures')

	@property
	def CurrentSpeed(self):
		"""Indicates the current speed.

		Returns:
			number
		"""
		return self._get_attribute('currentSpeed')

	@property
	def DataPathId(self):
		"""The Datapath identifier of the Open Flow channel.

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path identifier of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def EthernetAddress(self):
		"""Signifies the Ethernet IP address of the switch.

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')

	@property
	def LocalIp(self):
		"""Signifies the local IP of the switch that the OF Channel is connected to.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MaximumSpeed(self):
		"""Indicates the maximum speed.

		Returns:
			number
		"""
		return self._get_attribute('maximumSpeed')

	@property
	def Name(self):
		"""Signifies the name of the port.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def PeerAdvertisedFeatures(self):
		"""Signifies the features advertised by the peer port.

		Returns:
			str
		"""
		return self._get_attribute('peerAdvertisedFeatures')

	@property
	def PortNumber(self):
		"""Indicates the port number used by the corresponding switch.

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

	@property
	def RemoteIp(self):
		"""Signifies the remote IP of the switch that the OF Channel is connected to.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def State(self):
		"""Signifies the state of the port.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def SupportedFeatures(self):
		"""Signifies the features supported by the port.

		Returns:
			str
		"""
		return self._get_attribute('supportedFeatures')

	def find(self, AdvertisedFeatures=None, Config=None, CurrentFeatures=None, CurrentSpeed=None, DataPathId=None, DataPathIdAsHex=None, EthernetAddress=None, LocalIp=None, MaximumSpeed=None, Name=None, PeerAdvertisedFeatures=None, PortNumber=None, RemoteIp=None, State=None, SupportedFeatures=None):
		"""Finds and retrieves ofChannelPortsLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelPortsLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelPortsLearnedInformation data from the server.

		Args:
			AdvertisedFeatures (str): Signifies the advertised features of the port.
			Config (str): Signifies the configuration name.
			CurrentFeatures (str): Signifies the current features of the port.
			CurrentSpeed (number): Indicates the current speed.
			DataPathId (number): The Datapath identifier of the Open Flow channel.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow switch in hexadecimal format.
			EthernetAddress (str): Signifies the Ethernet IP address of the switch.
			LocalIp (str): Signifies the local IP of the switch that the OF Channel is connected to.
			MaximumSpeed (number): Indicates the maximum speed.
			Name (str): Signifies the name of the port.
			PeerAdvertisedFeatures (str): Signifies the features advertised by the peer port.
			PortNumber (number): Indicates the port number used by the corresponding switch.
			RemoteIp (str): Signifies the remote IP of the switch that the OF Channel is connected to.
			State (str): Signifies the state of the port.
			SupportedFeatures (str): Signifies the features supported by the port.

		Returns:
			self: This instance with matching ofChannelPortsLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelPortsLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelPortsLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
