from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ConfigElement(Base):
	"""The ConfigElement class encapsulates a system managed configElement node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ConfigElement property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'configElement'

	def __init__(self, parent):
		super(ConfigElement, self).__init__(parent)

	@property
	def FramePayload(self):
		"""An instance of the FramePayload class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framepayload.framepayload.FramePayload)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framepayload.framepayload import FramePayload
		return FramePayload(self)._select()

	@property
	def FrameRate(self):
		"""An instance of the FrameRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framerate.framerate.FrameRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framerate.framerate import FrameRate
		return FrameRate(self)._select()

	@property
	def FrameRateDistribution(self):
		"""An instance of the FrameRateDistribution class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.frameratedistribution.frameratedistribution.FrameRateDistribution)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.frameratedistribution.frameratedistribution import FrameRateDistribution
		return FrameRateDistribution(self)._select()

	@property
	def FrameSize(self):
		"""An instance of the FrameSize class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framesize.framesize.FrameSize)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.framesize.framesize import FrameSize
		return FrameSize(self)._select()

	@property
	def Stack(self):
		"""An instance of the Stack class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.stack.Stack)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.stack import Stack
		return Stack(self)

	@property
	def StackLink(self):
		"""An instance of the StackLink class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stacklink.stacklink.StackLink)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stacklink.stacklink import StackLink
		return StackLink(self)

	@property
	def TransmissionControl(self):
		"""An instance of the TransmissionControl class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissioncontrol.transmissioncontrol.TransmissionControl)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissioncontrol.transmissioncontrol import TransmissionControl
		return TransmissionControl(self)._select()

	@property
	def TransmissionDistribution(self):
		"""An instance of the TransmissionDistribution class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissiondistribution.transmissiondistribution.TransmissionDistribution)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.transmissiondistribution.transmissiondistribution import TransmissionDistribution
		return TransmissionDistribution(self)

	@property
	def Crc(self):
		"""The Cyclic Redundancy Check frame of the configured encapsulation set.

		Returns:
			str(badCrc|goodCrc)
		"""
		return self._get_attribute('crc')
	@Crc.setter
	def Crc(self, value):
		self._set_attribute('crc', value)

	@property
	def DestinationMacMode(self):
		"""The destination MAC address that is to be configured.

		Returns:
			str(arp|manual)
		"""
		return self._get_attribute('destinationMacMode')
	@DestinationMacMode.setter
	def DestinationMacMode(self, value):
		self._set_attribute('destinationMacMode', value)

	@property
	def EnableDisparityError(self):
		"""If true, enables disparity error

		Returns:
			bool
		"""
		return self._get_attribute('enableDisparityError')
	@EnableDisparityError.setter
	def EnableDisparityError(self, value):
		self._set_attribute('enableDisparityError', value)

	@property
	def EncapsulationName(self):
		"""Indicates the name of the encapsulation set.

		Returns:
			str
		"""
		return self._get_attribute('encapsulationName')

	@property
	def EndpointSetId(self):
		"""Indicates the identification of the endpoint set.

		Returns:
			number
		"""
		return self._get_attribute('endpointSetId')

	@property
	def PreambleCustomSize(self):
		"""Indicates the customized preamble size of the frame.

		Returns:
			number
		"""
		return self._get_attribute('preambleCustomSize')
	@PreambleCustomSize.setter
	def PreambleCustomSize(self, value):
		self._set_attribute('preambleCustomSize', value)

	@property
	def PreambleFrameSizeMode(self):
		"""The preamble size to synchronize sender and receiver of the configured encapsulation set.

		Returns:
			str(auto|custom)
		"""
		return self._get_attribute('preambleFrameSizeMode')
	@PreambleFrameSizeMode.setter
	def PreambleFrameSizeMode(self, value):
		self._set_attribute('preambleFrameSizeMode', value)

	def find(self, Crc=None, DestinationMacMode=None, EnableDisparityError=None, EncapsulationName=None, EndpointSetId=None, PreambleCustomSize=None, PreambleFrameSizeMode=None):
		"""Finds and retrieves configElement data from the server.

		All named parameters support regex and can be used to selectively retrieve configElement data from the server.
		By default the find method takes no parameters and will retrieve all configElement data from the server.

		Args:
			Crc (str(badCrc|goodCrc)): The Cyclic Redundancy Check frame of the configured encapsulation set.
			DestinationMacMode (str(arp|manual)): The destination MAC address that is to be configured.
			EnableDisparityError (bool): If true, enables disparity error
			EncapsulationName (str): Indicates the name of the encapsulation set.
			EndpointSetId (number): Indicates the identification of the endpoint set.
			PreambleCustomSize (number): Indicates the customized preamble size of the frame.
			PreambleFrameSizeMode (str(auto|custom)): The preamble size to synchronize sender and receiver of the configured encapsulation set.

		Returns:
			self: This instance with matching configElement data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of configElement data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the configElement data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
