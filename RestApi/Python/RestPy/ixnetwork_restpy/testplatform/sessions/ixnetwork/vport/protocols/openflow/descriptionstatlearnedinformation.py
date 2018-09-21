from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DescriptionStatLearnedInformation(Base):
	"""The DescriptionStatLearnedInformation class encapsulates a system managed descriptionStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DescriptionStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'descriptionStatLearnedInformation'

	def __init__(self, parent):
		super(DescriptionStatLearnedInformation, self).__init__(parent)

	@property
	def DataPathDescription(self):
		"""Indicates a description of datapath.

		Returns:
			str
		"""
		return self._get_attribute('dataPathDescription')

	@property
	def DataPathId(self):
		"""Indicates the datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Indicates the datapath ID, in Hex, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

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
	def HardwareDescription(self):
		"""Indicates the hardware description of the switch.

		Returns:
			str
		"""
		return self._get_attribute('hardwareDescription')

	@property
	def Latency(self):
		"""Indicates the duration elapsed (in microsecond) between the learned info request and response.

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
	def ManufacturerDescription(self):
		"""Indicates the description of the switch manufacturer.

		Returns:
			str
		"""
		return self._get_attribute('manufacturerDescription')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def RemoteIp(self):
		"""Indicates the IP of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Indicates the reply state of the switch.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def SerialNumber(self):
		"""Indicates the Serial Number of the switch.

		Returns:
			str
		"""
		return self._get_attribute('serialNumber')

	@property
	def SoftwareDescription(self):
		"""Indicates the description of the software installed on the switch.

		Returns:
			str
		"""
		return self._get_attribute('softwareDescription')

	def find(self, DataPathDescription=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, HardwareDescription=None, Latency=None, LocalIp=None, ManufacturerDescription=None, NegotiatedVersion=None, RemoteIp=None, ReplyState=None, SerialNumber=None, SoftwareDescription=None):
		"""Finds and retrieves descriptionStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve descriptionStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all descriptionStatLearnedInformation data from the server.

		Args:
			DataPathDescription (str): Indicates a description of datapath.
			DataPathId (str): Indicates the datapath ID of the switch.
			DataPathIdAsHex (str): Indicates the datapath ID, in Hex, of the switch.
			ErrorCode (str): Signifies the error code of the error received.
			ErrorType (str): Signifies the type of the error received.
			HardwareDescription (str): Indicates the hardware description of the switch.
			Latency (number): Indicates the duration elapsed (in microsecond) between the learned info request and response.
			LocalIp (str): Indicates the local IP of the Controller.
			ManufacturerDescription (str): Indicates the description of the switch manufacturer.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			RemoteIp (str): Indicates the IP of the remote end of the OF Channel.
			ReplyState (str): Indicates the reply state of the switch.
			SerialNumber (str): Indicates the Serial Number of the switch.
			SoftwareDescription (str): Indicates the description of the software installed on the switch.

		Returns:
			self: This instance with matching descriptionStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of descriptionStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the descriptionStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
