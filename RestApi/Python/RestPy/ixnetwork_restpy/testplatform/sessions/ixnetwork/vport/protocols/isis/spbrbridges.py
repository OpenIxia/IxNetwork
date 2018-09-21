from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbRbridges(Base):
	"""The SpbRbridges class encapsulates a system managed spbRbridges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbRbridges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'spbRbridges'

	def __init__(self, parent):
		super(SpbRbridges, self).__init__(parent)

	@property
	def Age(self):
		"""(read only) This indicates the age in time in seconds, since it was last refreshed.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def AuxillaryMcidConfigName(self):
		"""The auxiliary MCID configuration name.

		Returns:
			str
		"""
		return self._get_attribute('auxillaryMcidConfigName')

	@property
	def BaseVid(self):
		"""The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('baseVid')

	@property
	def BridgeMacAddress(self):
		"""The 6-byte MAC address assigned to this bridge. Part of the bridge identifier (bridge ID).

		Returns:
			str
		"""
		return self._get_attribute('bridgeMacAddress')

	@property
	def BridgePriority(self):
		"""The Bridge Priority for this bridge.The valid range is 0 to 61,440, in multiples of 4,096. (default = 32,768).

		Returns:
			number
		"""
		return self._get_attribute('bridgePriority')

	@property
	def EctAlgorithm(self):
		"""The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithm')

	@property
	def HostName(self):
		"""(read only) The host name as retrieved from the related packets.

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def IsId(self):
		"""The I-component service identifier. The maximum value is 16777215. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('isId')

	@property
	def LinkMetric(self):
		"""The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')

	@property
	def MBit(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('mBit')

	@property
	def McidConfigName(self):
		"""The MCID configuration name.

		Returns:
			str
		"""
		return self._get_attribute('mcidConfigName')

	@property
	def RBit(self):
		"""The Restart State bit.

		Returns:
			bool
		"""
		return self._get_attribute('rBit')

	@property
	def SequenceNumber(self):
		"""(read only) This indicates the sequence number of the LSP containing the route.

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SystemId(self):
		"""(read only) This indicates the ISIS System ID.

		Returns:
			str
		"""
		return self._get_attribute('systemId')

	@property
	def TBit(self):
		"""The external route tag bit.

		Returns:
			bool
		"""
		return self._get_attribute('tBit')

	@property
	def UseFlagBit(self):
		"""Allows to use flag bit.

		Returns:
			bool
		"""
		return self._get_attribute('useFlagBit')

	def find(self, Age=None, AuxillaryMcidConfigName=None, BaseVid=None, BridgeMacAddress=None, BridgePriority=None, EctAlgorithm=None, HostName=None, IsId=None, LinkMetric=None, MBit=None, McidConfigName=None, RBit=None, SequenceNumber=None, SystemId=None, TBit=None, UseFlagBit=None):
		"""Finds and retrieves spbRbridges data from the server.

		All named parameters support regex and can be used to selectively retrieve spbRbridges data from the server.
		By default the find method takes no parameters and will retrieve all spbRbridges data from the server.

		Args:
			Age (number): (read only) This indicates the age in time in seconds, since it was last refreshed.
			AuxillaryMcidConfigName (str): The auxiliary MCID configuration name.
			BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
			BridgeMacAddress (str): The 6-byte MAC address assigned to this bridge. Part of the bridge identifier (bridge ID).
			BridgePriority (number): The Bridge Priority for this bridge.The valid range is 0 to 61,440, in multiples of 4,096. (default = 32,768).
			EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
			HostName (str): (read only) The host name as retrieved from the related packets.
			IsId (number): The I-component service identifier. The maximum value is 16777215. The minimum value is 0.
			LinkMetric (number): The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.
			MBit (bool): NOT DEFINED
			McidConfigName (str): The MCID configuration name.
			RBit (bool): The Restart State bit.
			SequenceNumber (number): (read only) This indicates the sequence number of the LSP containing the route.
			SystemId (str): (read only) This indicates the ISIS System ID.
			TBit (bool): The external route tag bit.
			UseFlagBit (bool): Allows to use flag bit.

		Returns:
			self: This instance with matching spbRbridges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbRbridges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbRbridges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
