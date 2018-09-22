from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetworkTopology(Base):
	"""The NetworkTopology class encapsulates a user managed networkTopology node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetworkTopology property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'networkTopology'

	def __init__(self, parent):
		super(NetworkTopology, self).__init__(parent)

	@property
	def ExternalLink(self):
		"""An instance of the ExternalLink class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink.ExternalLink)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink import ExternalLink
		return ExternalLink(self)

	@property
	def IsisDceSimulatedTopologyConfig(self):
		"""An instance of the IsisDceSimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimulatedtopologyconfig.IsisDceSimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimulatedtopologyconfig import IsisDceSimulatedTopologyConfig
		return IsisDceSimulatedTopologyConfig(self)

	@property
	def IsisL3SimulatedTopologyConfig(self):
		"""An instance of the IsisL3SimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3simulatedtopologyconfig.IsisL3SimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3simulatedtopologyconfig import IsisL3SimulatedTopologyConfig
		return IsisL3SimulatedTopologyConfig(self)

	@property
	def IsisSpbSimulatedTopologyConfig(self):
		"""An instance of the IsisSpbSimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimulatedtopologyconfig.IsisSpbSimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimulatedtopologyconfig import IsisSpbSimulatedTopologyConfig
		return IsisSpbSimulatedTopologyConfig(self)

	@property
	def IsisTrillSimulatedTopologyConfig(self):
		"""An instance of the IsisTrillSimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimulatedtopologyconfig.IsisTrillSimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimulatedtopologyconfig import IsisTrillSimulatedTopologyConfig
		return IsisTrillSimulatedTopologyConfig(self)

	@property
	def LdpSimulatedTopologyConfig(self):
		"""An instance of the LdpSimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpsimulatedtopologyconfig.LdpSimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpsimulatedtopologyconfig import LdpSimulatedTopologyConfig
		return LdpSimulatedTopologyConfig(self)

	@property
	def NetTopologyCustom(self):
		"""An instance of the NetTopologyCustom class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom.NetTopologyCustom)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom import NetTopologyCustom
		return NetTopologyCustom(self)

	@property
	def NetTopologyFatTree(self):
		"""An instance of the NetTopologyFatTree class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree.NetTopologyFatTree)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree import NetTopologyFatTree
		return NetTopologyFatTree(self)

	@property
	def NetTopologyGrid(self):
		"""An instance of the NetTopologyGrid class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid.NetTopologyGrid)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid import NetTopologyGrid
		return NetTopologyGrid(self)

	@property
	def NetTopologyHubNSpoke(self):
		"""An instance of the NetTopologyHubNSpoke class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke.NetTopologyHubNSpoke)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke import NetTopologyHubNSpoke
		return NetTopologyHubNSpoke(self)

	@property
	def NetTopologyLinear(self):
		"""An instance of the NetTopologyLinear class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear.NetTopologyLinear)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear import NetTopologyLinear
		return NetTopologyLinear(self)

	@property
	def NetTopologyMesh(self):
		"""An instance of the NetTopologyMesh class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh.NetTopologyMesh)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh import NetTopologyMesh
		return NetTopologyMesh(self)

	@property
	def NetTopologyRing(self):
		"""An instance of the NetTopologyRing class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring.NetTopologyRing)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring import NetTopologyRing
		return NetTopologyRing(self)

	@property
	def NetTopologyTree(self):
		"""An instance of the NetTopologyTree class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree.NetTopologyTree)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree import NetTopologyTree
		return NetTopologyTree(self)

	@property
	def OspfSimulatedTopologyConfig(self):
		"""An instance of the OspfSimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsimulatedtopologyconfig.OspfSimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsimulatedtopologyconfig import OspfSimulatedTopologyConfig
		return OspfSimulatedTopologyConfig(self)

	@property
	def Ospfv3SimulatedTopologyConfig(self):
		"""An instance of the Ospfv3SimulatedTopologyConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3simulatedtopologyconfig.Ospfv3SimulatedTopologyConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3simulatedtopologyconfig import Ospfv3SimulatedTopologyConfig
		return Ospfv3SimulatedTopologyConfig(self)

	@property
	def SimInterface(self):
		"""An instance of the SimInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.siminterface.SimInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.siminterface import SimInterface
		return SimInterface(self)

	@property
	def SimRouter(self):
		"""An instance of the SimRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouter.SimRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouter import SimRouter
		return SimRouter(self)

	@property
	def SimRouterBridge(self):
		"""An instance of the SimRouterBridge class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouterbridge.SimRouterBridge)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouterbridge import SimRouterBridge
		return SimRouterBridge(self)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def LinksPerNetwork(self):
		"""linksPerNetwork is controled by assigned topology

		Returns:
			number
		"""
		return self._get_attribute('linksPerNetwork')

	@property
	def NodesPerNetwork(self):
		"""Number of nodes in the Network Topology, including the root node defined in the parent Device Group

		Returns:
			number
		"""
		return self._get_attribute('nodesPerNetwork')

	def add(self):
		"""Adds a new networkTopology node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved networkTopology data using find and the newly added networkTopology data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the networkTopology data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, LinksPerNetwork=None, NodesPerNetwork=None):
		"""Finds and retrieves networkTopology data from the server.

		All named parameters support regex and can be used to selectively retrieve networkTopology data from the server.
		By default the find method takes no parameters and will retrieve all networkTopology data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			LinksPerNetwork (number): linksPerNetwork is controled by assigned topology
			NodesPerNetwork (number): Number of nodes in the Network Topology, including the root node defined in the parent Device Group

		Returns:
			self: This instance with matching networkTopology data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of networkTopology data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the networkTopology data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
