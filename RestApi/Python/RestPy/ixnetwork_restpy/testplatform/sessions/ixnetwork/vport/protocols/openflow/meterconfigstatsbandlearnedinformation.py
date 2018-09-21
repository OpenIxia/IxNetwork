from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeterConfigStatsBandLearnedInformation(Base):
	"""The MeterConfigStatsBandLearnedInformation class encapsulates a system managed meterConfigStatsBandLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterConfigStatsBandLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterConfigStatsBandLearnedInformation'

	def __init__(self, parent):
		super(MeterConfigStatsBandLearnedInformation, self).__init__(parent)

	@property
	def BurstSize(self):
		"""Specifies the Burst Size

		Returns:
			number
		"""
		return self._get_attribute('burstSize')

	@property
	def DataPathId(self):
		"""The Data Path identifier of the OpenFlow Controller.

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path identifier of the OpenFlow Controller in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def Experimenter(self):
		"""Specifies the Experimenter Value

		Returns:
			str
		"""
		return self._get_attribute('experimenter')

	@property
	def LocalIp(self):
		"""Indicates the local IP of the Controller.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MeterId(self):
		"""Specifies Meter Id

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def PrecedenceLevel(self):
		"""Specifies the Precedence Level Value

		Returns:
			str
		"""
		return self._get_attribute('precedenceLevel')

	@property
	def Rate(self):
		"""Specifies the rate

		Returns:
			number
		"""
		return self._get_attribute('rate')

	@property
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def Type(self):
		"""Specifies the Band Type

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, BurstSize=None, DataPathId=None, DataPathIdAsHex=None, Experimenter=None, LocalIp=None, MeterId=None, PrecedenceLevel=None, Rate=None, RemoteIp=None, Type=None):
		"""Finds and retrieves meterConfigStatsBandLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterConfigStatsBandLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterConfigStatsBandLearnedInformation data from the server.

		Args:
			BurstSize (number): Specifies the Burst Size
			DataPathId (number): The Data Path identifier of the OpenFlow Controller.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow Controller in hexadecimal format.
			Experimenter (str): Specifies the Experimenter Value
			LocalIp (str): Indicates the local IP of the Controller.
			MeterId (number): Specifies Meter Id
			PrecedenceLevel (str): Specifies the Precedence Level Value
			Rate (number): Specifies the rate
			RemoteIp (str): The Remote IP address of the selected interface.
			Type (str): Specifies the Band Type

		Returns:
			self: This instance with matching meterConfigStatsBandLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterConfigStatsBandLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterConfigStatsBandLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
