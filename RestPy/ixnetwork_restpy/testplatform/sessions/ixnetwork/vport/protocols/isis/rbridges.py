from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RBridges(Base):
	"""The RBridges class encapsulates a system managed rBridges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RBridges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rBridges'

	def __init__(self, parent):
		super(RBridges, self).__init__(parent)

	@property
	def Age(self):
		"""This indicates the age in time in seconds, since it was last refreshed.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def EnableCommonMtId(self):
		"""If true, common Mt ld is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableCommonMtId')

	@property
	def ExtendedCircuitId(self):
		"""The hexadecimal format of the extended circuit.

		Returns:
			number
		"""
		return self._get_attribute('extendedCircuitId')

	@property
	def GraphId(self):
		"""This indicates the Graph ID value if FTAG is present.

		Returns:
			number
		"""
		return self._get_attribute('graphId')

	@property
	def HostName(self):
		"""The host name as retrieved from the related packets.

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def LinkMetric(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')

	@property
	def MtId(self):
		"""This indicates the MT ID.

		Returns:
			number
		"""
		return self._get_attribute('mtId')

	@property
	def PrimaryFtag(self):
		"""This indicates the Primary FTAG value if FTAG is present.

		Returns:
			number
		"""
		return self._get_attribute('primaryFtag')

	@property
	def Priority(self):
		"""This indicates the Broadcast Root Priority as advertised by this RBridge.

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def Role(self):
		"""This indicates the role of the RBridge.

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SecondaryFtag(self):
		"""This indicates the Secondary FTAG value if FTAG is present.

		Returns:
			number
		"""
		return self._get_attribute('secondaryFtag')

	@property
	def SequenceNumber(self):
		"""This indicates the sequence number of the LSP containing the route.

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SwitchId(self):
		"""This indicates the Switch ID.

		Returns:
			number
		"""
		return self._get_attribute('switchId')

	@property
	def SystemId(self):
		"""This indicates the ISIS System ID.

		Returns:
			str
		"""
		return self._get_attribute('systemId')

	def find(self, Age=None, EnableCommonMtId=None, ExtendedCircuitId=None, GraphId=None, HostName=None, LinkMetric=None, MtId=None, PrimaryFtag=None, Priority=None, Role=None, SecondaryFtag=None, SequenceNumber=None, SwitchId=None, SystemId=None):
		"""Finds and retrieves rBridges data from the server.

		All named parameters support regex and can be used to selectively retrieve rBridges data from the server.
		By default the find method takes no parameters and will retrieve all rBridges data from the server.

		Args:
			Age (number): This indicates the age in time in seconds, since it was last refreshed.
			EnableCommonMtId (bool): If true, common Mt ld is enabled.
			ExtendedCircuitId (number): The hexadecimal format of the extended circuit.
			GraphId (number): This indicates the Graph ID value if FTAG is present.
			HostName (str): The host name as retrieved from the related packets.
			LinkMetric (number): NOT DEFINED
			MtId (number): This indicates the MT ID.
			PrimaryFtag (number): This indicates the Primary FTAG value if FTAG is present.
			Priority (number): This indicates the Broadcast Root Priority as advertised by this RBridge.
			Role (str): This indicates the role of the RBridge.
			SecondaryFtag (number): This indicates the Secondary FTAG value if FTAG is present.
			SequenceNumber (number): This indicates the sequence number of the LSP containing the route.
			SwitchId (number): This indicates the Switch ID.
			SystemId (str): This indicates the ISIS System ID.

		Returns:
			self: This instance with matching rBridges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rBridges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rBridges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
