from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbSimEdgeTopologyList(Base):
	"""The SpbSimEdgeTopologyList class encapsulates a required spbSimEdgeTopologyList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbSimEdgeTopologyList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'spbSimEdgeTopologyList'

	def __init__(self, parent):
		super(SpbSimEdgeTopologyList, self).__init__(parent)

	@property
	def SpbSimEdgeBaseVidList(self):
		"""An instance of the SpbSimEdgeBaseVidList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgebasevidlist.SpbSimEdgeBaseVidList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgebasevidlist import SpbSimEdgeBaseVidList
		return SpbSimEdgeBaseVidList(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BaseVIDCount(self):
		"""Base VID Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('baseVIDCount')

	@property
	def CistExternalRootCost(self):
		"""CIST External Root Cost

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cistExternalRootCost')

	@property
	def CistRootId(self):
		"""CIST Root Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cistRootId')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NumberOfPorts(self):
		"""Number of Ports

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def PortIdentifier(self):
		"""Port Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portIdentifier')

	@property
	def TopologyId(self):
		"""Topology Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('topologyId')

	@property
	def Vbit(self):
		"""Enable V Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vbit')
