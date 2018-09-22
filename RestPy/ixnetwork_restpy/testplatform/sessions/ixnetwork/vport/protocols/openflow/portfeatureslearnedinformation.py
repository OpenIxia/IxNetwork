from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PortFeaturesLearnedInformation(Base):
	"""The PortFeaturesLearnedInformation class encapsulates a system managed portFeaturesLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortFeaturesLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'portFeaturesLearnedInformation'

	def __init__(self, parent):
		super(PortFeaturesLearnedInformation, self).__init__(parent)

	@property
	def AdvertisedFeatures(self):
		"""The current features, like link modes, link types, and link features that the port advertises.

		Returns:
			str
		"""
		return self._get_attribute('advertisedFeatures')

	@property
	def Config(self):
		"""Signifies the configuration supported by the port.

		Returns:
			str
		"""
		return self._get_attribute('config')

	@property
	def CurrentFeatures(self):
		"""The current features like the link modes, link types, and link features that the port supports.

		Returns:
			str
		"""
		return self._get_attribute('currentFeatures')

	@property
	def CurrentSpeed(self):
		"""The current speed of the port in kbps.

		Returns:
			number
		"""
		return self._get_attribute('currentSpeed')

	@property
	def DataPathId(self):
		"""The Data Path identifier of the OpenFlow switch.

		Returns:
			str
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
	def EthernetAddress(self):
		"""The Ethernet address of the switch.

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')

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
	def MaxSpeed(self):
		"""The maximum speed of the port in kbps.

		Returns:
			number
		"""
		return self._get_attribute('maxSpeed')

	@property
	def Name(self):
		"""Signifies the name of the port.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def PeerAdvertisedFeatures(self):
		"""The current features, like, link modes, link types, and link features, that the peer advertises.

		Returns:
			str
		"""
		return self._get_attribute('peerAdvertisedFeatures')

	@property
	def PortNumber(self):
		"""The port number.

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

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

	@property
	def State(self):
		"""Signifies the states supported by the port.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def SupportedFeatures(self):
		"""The features like link modes, link types, and link features that is supported by the switch.

		Returns:
			str
		"""
		return self._get_attribute('supportedFeatures')

	def find(self, AdvertisedFeatures=None, Config=None, CurrentFeatures=None, CurrentSpeed=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, EthernetAddress=None, Latency=None, LocalIp=None, MaxSpeed=None, Name=None, NegotiatedVersion=None, PeerAdvertisedFeatures=None, PortNumber=None, RemoteIp=None, ReplyState=None, State=None, SupportedFeatures=None):
		"""Finds and retrieves portFeaturesLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve portFeaturesLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all portFeaturesLearnedInformation data from the server.

		Args:
			AdvertisedFeatures (str): The current features, like link modes, link types, and link features that the port advertises.
			Config (str): Signifies the configuration supported by the port.
			CurrentFeatures (str): The current features like the link modes, link types, and link features that the port supports.
			CurrentSpeed (number): The current speed of the port in kbps.
			DataPathId (str): The Data Path identifier of the OpenFlow switch.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow switch in hexadecimal format.
			ErrorCode (str): The error code of the received error.
			ErrorType (str): The type of the error received.
			EthernetAddress (str): The Ethernet address of the switch.
			Latency (number): The latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): Indicates the local IP of the Controller.
			MaxSpeed (number): The maximum speed of the port in kbps.
			Name (str): Signifies the name of the port.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			PeerAdvertisedFeatures (str): The current features, like, link modes, link types, and link features, that the peer advertises.
			PortNumber (number): The port number.
			RemoteIp (str): The Remote IP address of the selected interface.
			ReplyState (str): The state of reply for the Open Flow channel.
			State (str): Signifies the states supported by the port.
			SupportedFeatures (str): The features like link modes, link types, and link features that is supported by the switch.

		Returns:
			self: This instance with matching portFeaturesLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of portFeaturesLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the portFeaturesLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=portFeaturesLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
