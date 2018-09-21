from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbTopologyRange(Base):
	"""The SpbTopologyRange class encapsulates a user managed spbTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbTopologyRange'

	def __init__(self, parent):
		super(SpbTopologyRange, self).__init__(parent)

	@property
	def SpbBaseVidRange(self):
		"""An instance of the SpbBaseVidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbbasevidrange.SpbBaseVidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbbasevidrange import SpbBaseVidRange
		return SpbBaseVidRange(self)

	@property
	def AuxMcidConfigName(self):
		"""The auxiliary MCID configuration name.

		Returns:
			str
		"""
		return self._get_attribute('auxMcidConfigName')
	@AuxMcidConfigName.setter
	def AuxMcidConfigName(self, value):
		self._set_attribute('auxMcidConfigName', value)

	@property
	def AuxMcidSignature(self):
		"""The auxiliary MCID signature.

		Returns:
			str
		"""
		return self._get_attribute('auxMcidSignature')
	@AuxMcidSignature.setter
	def AuxMcidSignature(self, value):
		self._set_attribute('auxMcidSignature', value)

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
	def CistRootIdentiifer(self):
		"""Bridge identifier of the CIST root bridge.

		Returns:
			str
		"""
		return self._get_attribute('cistRootIdentiifer')
	@CistRootIdentiifer.setter
	def CistRootIdentiifer(self, value):
		self._set_attribute('cistRootIdentiifer', value)

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
	def McidConfigName(self):
		"""The MCID configuration name.

		Returns:
			str
		"""
		return self._get_attribute('mcidConfigName')
	@McidConfigName.setter
	def McidConfigName(self, value):
		self._set_attribute('mcidConfigName', value)

	@property
	def McidSignature(self):
		"""The MCID signature.

		Returns:
			str
		"""
		return self._get_attribute('mcidSignature')
	@McidSignature.setter
	def McidSignature(self, value):
		self._set_attribute('mcidSignature', value)

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

	def add(self, AuxMcidConfigName=None, AuxMcidSignature=None, BridgePriority=None, CistExternalRootCost=None, CistRootIdentiifer=None, EnableVbit=None, Enabled=None, LinkMetric=None, McidConfigName=None, McidSignature=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Adds a new spbTopologyRange node on the server and retrieves it in this instance.

		Args:
			AuxMcidConfigName (str): The auxiliary MCID configuration name.
			AuxMcidSignature (str): The auxiliary MCID signature.
			BridgePriority (number): The value assigned as the priority of the bridge. The default value is 32768. The maximum value is 65535. The minimum value is 0.
			CistExternalRootCost (number): The Common and Internal Spanning Tree calculated cost to reach the root bridge from the bridge where the command is entered.
			CistRootIdentiifer (str): Bridge identifier of the CIST root bridge.
			EnableVbit (bool): If true, activates the V bit.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			LinkMetric (number): The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.
			McidConfigName (str): The MCID configuration name.
			McidSignature (str): The MCID signature.
			NoOfPorts (number): The number of configured ports for the protocol. The default value is 1. The maximum value is 255. The minimum value is 0.
			PortIdentifier (number): The identifier for the configured port. The default value is 1. The maximum value is 65535. The minimum value is 0.
			SpSourceId (number): The Shortest Path source identifier. The default value is 0. The maximum value is 1048575. The minimum value is 0.

		Returns:
			self: This instance with all currently retrieved spbTopologyRange data using find and the newly added spbTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AuxMcidConfigName=None, AuxMcidSignature=None, BridgePriority=None, CistExternalRootCost=None, CistRootIdentiifer=None, EnableVbit=None, Enabled=None, LinkMetric=None, McidConfigName=None, McidSignature=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Finds and retrieves spbTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all spbTopologyRange data from the server.

		Args:
			AuxMcidConfigName (str): The auxiliary MCID configuration name.
			AuxMcidSignature (str): The auxiliary MCID signature.
			BridgePriority (number): The value assigned as the priority of the bridge. The default value is 32768. The maximum value is 65535. The minimum value is 0.
			CistExternalRootCost (number): The Common and Internal Spanning Tree calculated cost to reach the root bridge from the bridge where the command is entered.
			CistRootIdentiifer (str): Bridge identifier of the CIST root bridge.
			EnableVbit (bool): If true, activates the V bit.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			LinkMetric (number): The LSP metric related to the network. The default value is 10. The maximum value is 16777215. The minimum value is 0.
			McidConfigName (str): The MCID configuration name.
			McidSignature (str): The MCID signature.
			NoOfPorts (number): The number of configured ports for the protocol. The default value is 1. The maximum value is 255. The minimum value is 0.
			PortIdentifier (number): The identifier for the configured port. The default value is 1. The maximum value is 65535. The minimum value is 0.
			SpSourceId (number): The Shortest Path source identifier. The default value is 0. The maximum value is 1048575. The minimum value is 0.

		Returns:
			self: This instance with matching spbTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
