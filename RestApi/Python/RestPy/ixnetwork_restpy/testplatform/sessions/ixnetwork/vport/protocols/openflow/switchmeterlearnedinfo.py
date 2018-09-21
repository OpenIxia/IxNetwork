from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchMeterLearnedInfo(Base):
	"""The SwitchMeterLearnedInfo class encapsulates a system managed switchMeterLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchMeterLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchMeterLearnedInfo'

	def __init__(self, parent):
		super(SwitchMeterLearnedInfo, self).__init__(parent)

	@property
	def SwitchMeterBandLearnedInfo(self):
		"""An instance of the SwitchMeterBandLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchmeterbandlearnedinfo.SwitchMeterBandLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchmeterbandlearnedinfo import SwitchMeterBandLearnedInfo
		return SwitchMeterBandLearnedInfo(self)

	@property
	def BytesInInput(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('bytesInInput')

	@property
	def DatapathId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('datapathId')

	@property
	def DatapathIdAsHex(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('datapathIdAsHex')

	@property
	def DurationNSec(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('durationNSec')

	@property
	def DurationSec(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('durationSec')

	@property
	def FlowCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('flowCount')

	@property
	def LocalIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MeterConfigurationFlags(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('meterConfigurationFlags')

	@property
	def MeterId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def NumOfBands(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numOfBands')

	@property
	def PacketsInInput(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('packetsInInput')

	def find(self, BytesInInput=None, DatapathId=None, DatapathIdAsHex=None, DurationNSec=None, DurationSec=None, FlowCount=None, LocalIp=None, MeterConfigurationFlags=None, MeterId=None, NumOfBands=None, PacketsInInput=None):
		"""Finds and retrieves switchMeterLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchMeterLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchMeterLearnedInfo data from the server.

		Args:
			BytesInInput (number): NOT DEFINED
			DatapathId (str): NOT DEFINED
			DatapathIdAsHex (str): NOT DEFINED
			DurationNSec (number): NOT DEFINED
			DurationSec (number): NOT DEFINED
			FlowCount (number): NOT DEFINED
			LocalIp (str): NOT DEFINED
			MeterConfigurationFlags (str): NOT DEFINED
			MeterId (number): NOT DEFINED
			NumOfBands (number): NOT DEFINED
			PacketsInInput (number): NOT DEFINED

		Returns:
			self: This instance with matching switchMeterLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchMeterLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchMeterLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
