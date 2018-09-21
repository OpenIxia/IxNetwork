from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbmNodeTopologyRange(Base):
	"""The SpbmNodeTopologyRange class encapsulates a user managed spbmNodeTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbmNodeTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbmNodeTopologyRange'

	def __init__(self, parent):
		super(SpbmNodeTopologyRange, self).__init__(parent)

	@property
	def SpbmNodeBaseVidRange(self):
		"""An instance of the SpbmNodeBaseVidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodebasevidrange.SpbmNodeBaseVidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodebasevidrange import SpbmNodeBaseVidRange
		return SpbmNodeBaseVidRange(self)

	@property
	def BridgePriority(self):
		"""The value assigned as the priority of the bridge. The default value is 32768. The maximum value is 65535. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('bridgePriority')
	@BridgePriority.setter
	def BridgePriority(self, value):
		self._set_attribute('bridgePriority', value)

	@property
	def CistExternalRootCost(self):
		"""The Common and Internal Spanning Tree calculated cost to reach the root bridge from the bridge where the command is entered.

		Returns:
			number
		"""
		return self._get_attribute('cistExternalRootCost')
	@CistExternalRootCost.setter
	def CistExternalRootCost(self, value):
		self._set_attribute('cistExternalRootCost', value)

	@property
	def CistRootIdentifier(self):
		"""Bridge identifier of the CIST root bridge.

		Returns:
			str
		"""
		return self._get_attribute('cistRootIdentifier')
	@CistRootIdentifier.setter
	def CistRootIdentifier(self, value):
		self._set_attribute('cistRootIdentifier', value)

	@property
	def EnableVbit(self):
		"""If true, activates the V bit.

		Returns:
			bool
		"""
		return self._get_attribute('enableVbit')
	@EnableVbit.setter
	def EnableVbit(self, value):
		self._set_attribute('enableVbit', value)

	@property
	def Enabled(self):
		"""If true, the topology range will be part of the simulated network.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterNodeLinkMetricIncrement(self):
		"""The incremental value of the Inter Node link metric.

		Returns:
			number
		"""
		return self._get_attribute('interNodeLinkMetricIncrement')
	@InterNodeLinkMetricIncrement.setter
	def InterNodeLinkMetricIncrement(self, value):
		self._set_attribute('interNodeLinkMetricIncrement', value)

	@property
	def InterNodeSpSourceIdIncrement(self):
		"""The inter node Shortest Path source identifier.

		Returns:
			number
		"""
		return self._get_attribute('interNodeSpSourceIdIncrement')
	@InterNodeSpSourceIdIncrement.setter
	def InterNodeSpSourceIdIncrement(self, value):
		self._set_attribute('interNodeSpSourceIdIncrement', value)

	@property
	def LinkMetric(self):
		"""The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')
	@LinkMetric.setter
	def LinkMetric(self, value):
		self._set_attribute('linkMetric', value)

	@property
	def NoOfPorts(self):
		"""The number of configured ports for the protocol. The default value is 1. The maximum value is 255. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('noOfPorts')
	@NoOfPorts.setter
	def NoOfPorts(self, value):
		self._set_attribute('noOfPorts', value)

	@property
	def PortIdentifier(self):
		"""The identifier for the configured port. The default value is 1. The maximum value is 65535. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('portIdentifier')
	@PortIdentifier.setter
	def PortIdentifier(self, value):
		self._set_attribute('portIdentifier', value)

	@property
	def SpSourceId(self):
		"""The Shortest Path source identifier. The default value is 0. The maximum value is 1048575. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('spSourceId')
	@SpSourceId.setter
	def SpSourceId(self, value):
		self._set_attribute('spSourceId', value)

	def add(self, BridgePriority=None, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, Enabled=None, InterNodeLinkMetricIncrement=None, InterNodeSpSourceIdIncrement=None, LinkMetric=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Adds a new spbmNodeTopologyRange node on the server and retrieves it in this instance.

		Args:
			BridgePriority (number): The value assigned as the priority of the bridge. The default value is 32768. The maximum value is 65535. The minimum value is 0.
			CistExternalRootCost (number): The Common and Internal Spanning Tree calculated cost to reach the root bridge from the bridge where the command is entered.
			CistRootIdentifier (str): Bridge identifier of the CIST root bridge.
			EnableVbit (bool): If true, activates the V bit.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			InterNodeLinkMetricIncrement (number): The incremental value of the Inter Node link metric.
			InterNodeSpSourceIdIncrement (number): The inter node Shortest Path source identifier.
			LinkMetric (number): The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.
			NoOfPorts (number): The number of configured ports for the protocol. The default value is 1. The maximum value is 255. The minimum value is 0.
			PortIdentifier (number): The identifier for the configured port. The default value is 1. The maximum value is 65535. The minimum value is 0.
			SpSourceId (number): The Shortest Path source identifier. The default value is 0. The maximum value is 1048575. The minimum value is 0.

		Returns:
			self: This instance with all currently retrieved spbmNodeTopologyRange data using find and the newly added spbmNodeTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbmNodeTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BridgePriority=None, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, Enabled=None, InterNodeLinkMetricIncrement=None, InterNodeSpSourceIdIncrement=None, LinkMetric=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Finds and retrieves spbmNodeTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbmNodeTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all spbmNodeTopologyRange data from the server.

		Args:
			BridgePriority (number): The value assigned as the priority of the bridge. The default value is 32768. The maximum value is 65535. The minimum value is 0.
			CistExternalRootCost (number): The Common and Internal Spanning Tree calculated cost to reach the root bridge from the bridge where the command is entered.
			CistRootIdentifier (str): Bridge identifier of the CIST root bridge.
			EnableVbit (bool): If true, activates the V bit.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			InterNodeLinkMetricIncrement (number): The incremental value of the Inter Node link metric.
			InterNodeSpSourceIdIncrement (number): The inter node Shortest Path source identifier.
			LinkMetric (number): The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.
			NoOfPorts (number): The number of configured ports for the protocol. The default value is 1. The maximum value is 255. The minimum value is 0.
			PortIdentifier (number): The identifier for the configured port. The default value is 1. The maximum value is 65535. The minimum value is 0.
			SpSourceId (number): The Shortest Path source identifier. The default value is 0. The maximum value is 1048575. The minimum value is 0.

		Returns:
			self: This instance with matching spbmNodeTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbmNodeTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbmNodeTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
