from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Topology(Base):
	"""The Topology class encapsulates a required topology node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Topology property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'topology'

	def __init__(self, parent):
		super(Topology, self).__init__(parent)

	@property
	def Ancp(self):
		"""An instance of the Ancp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ancp.ancp.Ancp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ancp.ancp import Ancp
		return Ancp(self)._select()

	@property
	def BfdRouter(self):
		"""An instance of the BfdRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bfdrouter.bfdrouter.BfdRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bfdrouter.bfdrouter import BfdRouter
		return BfdRouter(self)._select()

	@property
	def BgpIpv4Peer(self):
		"""An instance of the BgpIpv4Peer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.bgpipv4peer.BgpIpv4Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.bgpipv4peer import BgpIpv4Peer
		return BgpIpv4Peer(self)._select()

	@property
	def BgpIpv6Peer(self):
		"""An instance of the BgpIpv6Peer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv6peer.bgpipv6peer.BgpIpv6Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv6peer.bgpipv6peer import BgpIpv6Peer
		return BgpIpv6Peer(self)._select()

	@property
	def CfmBridge(self):
		"""An instance of the CfmBridge class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.cfmbridge.cfmbridge.CfmBridge)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.cfmbridge.cfmbridge import CfmBridge
		return CfmBridge(self)._select()

	@property
	def Dhcpv4client(self):
		"""An instance of the Dhcpv4client class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.dhcpv4client.Dhcpv4client)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.dhcpv4client import Dhcpv4client
		return Dhcpv4client(self)._select()

	@property
	def Dhcpv4relayAgent(self):
		"""An instance of the Dhcpv4relayAgent class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4relayagent.dhcpv4relayagent.Dhcpv4relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4relayagent.dhcpv4relayagent import Dhcpv4relayAgent
		return Dhcpv4relayAgent(self)._select()

	@property
	def Dhcpv4server(self):
		"""An instance of the Dhcpv4server class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.dhcpv4server.Dhcpv4server)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.dhcpv4server import Dhcpv4server
		return Dhcpv4server(self)._select()

	@property
	def Dhcpv6client(self):
		"""An instance of the Dhcpv6client class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.dhcpv6client.Dhcpv6client)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.dhcpv6client import Dhcpv6client
		return Dhcpv6client(self)._select()

	@property
	def Dhcpv6relayAgent(self):
		"""An instance of the Dhcpv6relayAgent class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6relayagent.dhcpv6relayagent.Dhcpv6relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6relayagent.dhcpv6relayagent import Dhcpv6relayAgent
		return Dhcpv6relayAgent(self)._select()

	@property
	def Dhcpv6server(self):
		"""An instance of the Dhcpv6server class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.dhcpv6server.Dhcpv6server)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.dhcpv6server import Dhcpv6server
		return Dhcpv6server(self)._select()

	@property
	def DotOneX(self):
		"""An instance of the DotOneX class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dotonex.dotonex.DotOneX)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dotonex.dotonex import DotOneX
		return DotOneX(self)._select()

	@property
	def Ethernet(self):
		"""An instance of the Ethernet class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ethernet.ethernet.Ethernet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ethernet.ethernet import Ethernet
		return Ethernet(self)._select()

	@property
	def Geneve(self):
		"""An instance of the Geneve class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.geneve.geneve.Geneve)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.geneve.geneve import Geneve
		return Geneve(self)._select()

	@property
	def Greoipv4(self):
		"""An instance of the Greoipv4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv4.greoipv4.Greoipv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv4.greoipv4 import Greoipv4
		return Greoipv4(self)._select()

	@property
	def Greoipv6(self):
		"""An instance of the Greoipv6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv6.greoipv6.Greoipv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv6.greoipv6 import Greoipv6
		return Greoipv6(self)._select()

	@property
	def IgmpHost(self):
		"""An instance of the IgmpHost class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmphost.igmphost.IgmpHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmphost.igmphost import IgmpHost
		return IgmpHost(self)._select()

	@property
	def IgmpQuerier(self):
		"""An instance of the IgmpQuerier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmpquerier.igmpquerier.IgmpQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmpquerier.igmpquerier import IgmpQuerier
		return IgmpQuerier(self)._select()

	@property
	def Ipv4(self):
		"""An instance of the Ipv4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv4.ipv4.Ipv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv4.ipv4 import Ipv4
		return Ipv4(self)._select()

	@property
	def Ipv6(self):
		"""An instance of the Ipv6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6.ipv6.Ipv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6.ipv6 import Ipv6
		return Ipv6(self)._select()

	@property
	def Ipv6Autoconfiguration(self):
		"""An instance of the Ipv6Autoconfiguration class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6autoconfiguration.ipv6autoconfiguration.Ipv6Autoconfiguration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6autoconfiguration.ipv6autoconfiguration import Ipv6Autoconfiguration
		return Ipv6Autoconfiguration(self)._select()

	@property
	def IsisFabricPathRouter(self):
		"""An instance of the IsisFabricPathRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisfabricpathrouter.isisfabricpathrouter.IsisFabricPathRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisfabricpathrouter.isisfabricpathrouter import IsisFabricPathRouter
		return IsisFabricPathRouter(self)

	@property
	def IsisL3Router(self):
		"""An instance of the IsisL3Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.isisl3router.IsisL3Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.isisl3router import IsisL3Router
		return IsisL3Router(self)

	@property
	def IsisSpbRouter(self):
		"""An instance of the IsisSpbRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisspbrouter.isisspbrouter.IsisSpbRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisspbrouter.isisspbrouter import IsisSpbRouter
		return IsisSpbRouter(self)._select()

	@property
	def IsisTrillRouter(self):
		"""An instance of the IsisTrillRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isistrillrouter.isistrillrouter.IsisTrillRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isistrillrouter.isistrillrouter import IsisTrillRouter
		return IsisTrillRouter(self)

	@property
	def Lac(self):
		"""An instance of the Lac class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lac.lac.Lac)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lac.lac import Lac
		return Lac(self)._select()

	@property
	def Lacp(self):
		"""An instance of the Lacp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lacp.lacp.Lacp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lacp.lacp import Lacp
		return Lacp(self)._select()

	@property
	def LdpBasicRouter(self):
		"""An instance of the LdpBasicRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouter.ldpbasicrouter.LdpBasicRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouter.ldpbasicrouter import LdpBasicRouter
		return LdpBasicRouter(self)._select()

	@property
	def LdpBasicRouterV6(self):
		"""An instance of the LdpBasicRouterV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouterv6.ldpbasicrouterv6.LdpBasicRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouterv6.ldpbasicrouterv6 import LdpBasicRouterV6
		return LdpBasicRouterV6(self)._select()

	@property
	def LdpTargetedRouter(self):
		"""An instance of the LdpTargetedRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouter.ldptargetedrouter.LdpTargetedRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouter.ldptargetedrouter import LdpTargetedRouter
		return LdpTargetedRouter(self)._select()

	@property
	def LdpTargetedRouterV6(self):
		"""An instance of the LdpTargetedRouterV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouterv6.ldptargetedrouterv6.LdpTargetedRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouterv6.ldptargetedrouterv6 import LdpTargetedRouterV6
		return LdpTargetedRouterV6(self)._select()

	@property
	def LightweightDhcpv6relayAgent(self):
		"""An instance of the LightweightDhcpv6relayAgent class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lightweightdhcpv6relayagent.lightweightdhcpv6relayagent.LightweightDhcpv6relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lightweightdhcpv6relayagent.lightweightdhcpv6relayagent import LightweightDhcpv6relayAgent
		return LightweightDhcpv6relayAgent(self)._select()

	@property
	def Lns(self):
		"""An instance of the Lns class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lns.lns.Lns)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lns.lns import Lns
		return Lns(self)._select()

	@property
	def MldHost(self):
		"""An instance of the MldHost class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldhost.mldhost.MldHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldhost.mldhost import MldHost
		return MldHost(self)._select()

	@property
	def MldQuerier(self):
		"""An instance of the MldQuerier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldquerier.mldquerier.MldQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldquerier.mldquerier import MldQuerier
		return MldQuerier(self)._select()

	@property
	def MsrpListener(self):
		"""An instance of the MsrpListener class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrplistener.msrplistener.MsrpListener)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrplistener.msrplistener import MsrpListener
		return MsrpListener(self)._select()

	@property
	def MsrpTalker(self):
		"""An instance of the MsrpTalker class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrptalker.msrptalker.MsrpTalker)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrptalker.msrptalker import MsrpTalker
		return MsrpTalker(self)._select()

	@property
	def NetconfClient(self):
		"""An instance of the NetconfClient class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfclient.netconfclient.NetconfClient)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfclient.netconfclient import NetconfClient
		return NetconfClient(self)._select()

	@property
	def NetconfServer(self):
		"""An instance of the NetconfServer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfserver.netconfserver.NetconfServer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfserver.netconfserver import NetconfServer
		return NetconfServer(self)._select()

	@property
	def Ntpclock(self):
		"""An instance of the Ntpclock class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ntpclock.ntpclock.Ntpclock)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ntpclock.ntpclock import Ntpclock
		return Ntpclock(self)._select()

	@property
	def OpenFlowChannel(self):
		"""An instance of the OpenFlowChannel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.openflowchannel.OpenFlowChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.openflowchannel import OpenFlowChannel
		return OpenFlowChannel(self)._select()

	@property
	def OpenFlowController(self):
		"""An instance of the OpenFlowController class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.openflowcontroller.OpenFlowController)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.openflowcontroller import OpenFlowController
		return OpenFlowController(self)._select()

	@property
	def Ospfv2Router(self):
		"""An instance of the Ospfv2Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.ospfv2router.Ospfv2Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.ospfv2router import Ospfv2Router
		return Ospfv2Router(self)

	@property
	def Ospfv3Router(self):
		"""An instance of the Ospfv3Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv3router.ospfv3router.Ospfv3Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv3router.ospfv3router import Ospfv3Router
		return Ospfv3Router(self)._select()

	@property
	def Ovsdbcontroller(self):
		"""An instance of the Ovsdbcontroller class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbcontroller.ovsdbcontroller.Ovsdbcontroller)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbcontroller.ovsdbcontroller import Ovsdbcontroller
		return Ovsdbcontroller(self)._select()

	@property
	def Ovsdbserver(self):
		"""An instance of the Ovsdbserver class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbserver.ovsdbserver.Ovsdbserver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbserver.ovsdbserver import Ovsdbserver
		return Ovsdbserver(self)._select()

	@property
	def Pcc(self):
		"""An instance of the Pcc class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pcc.pcc.Pcc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pcc.pcc import Pcc
		return Pcc(self)._select()

	@property
	def PimRouter(self):
		"""An instance of the PimRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pimrouter.pimrouter.PimRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pimrouter.pimrouter import PimRouter
		return PimRouter(self)._select()

	@property
	def Pppoxclient(self):
		"""An instance of the Pppoxclient class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxclient.pppoxclient.Pppoxclient)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxclient.pppoxclient import Pppoxclient
		return Pppoxclient(self)._select()

	@property
	def Pppoxserver(self):
		"""An instance of the Pppoxserver class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxserver.pppoxserver.Pppoxserver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxserver.pppoxserver import Pppoxserver
		return Pppoxserver(self)._select()

	@property
	def Ptp(self):
		"""An instance of the Ptp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ptp.ptp.Ptp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ptp.ptp import Ptp
		return Ptp(self)._select()

	@property
	def RsvpteIf(self):
		"""An instance of the RsvpteIf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvpteif.rsvpteif.RsvpteIf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvpteif.rsvpteif import RsvpteIf
		return RsvpteIf(self)._select()

	@property
	def RsvpteLsps(self):
		"""An instance of the RsvpteLsps class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvptelsps.rsvptelsps.RsvpteLsps)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvptelsps.rsvptelsps import RsvpteLsps
		return RsvpteLsps(self)._select()

	@property
	def StaticLag(self):
		"""An instance of the StaticLag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.staticlag.staticlag.StaticLag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.staticlag.staticlag import StaticLag
		return StaticLag(self)._select()

	@property
	def Vxlan(self):
		"""An instance of the Vxlan class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.vxlan.vxlan.Vxlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.vxlan.vxlan import Vxlan
		return Vxlan(self)._select()

	@property
	def ApplyOnTheFlyState(self):
		"""Checks whether the apply changes operation is allowed

		Returns:
			str(allowed|notAllowed|nothingToApply)
		"""
		return self._get_attribute('applyOnTheFlyState')

	@property
	def NgpfProtocolRateMode(self):
		"""Decides whether protocol's sessions will started in normal or smooth mode

		Returns:
			str(basic|smooth)
		"""
		return self._get_attribute('ngpfProtocolRateMode')
	@NgpfProtocolRateMode.setter
	def NgpfProtocolRateMode(self, value):
		self._set_attribute('ngpfProtocolRateMode', value)

	@property
	def ProtocolActionsInProgress(self):
		"""Lists all current protocol actions in progress

		Returns:
			list(str)
		"""
		return self._get_attribute('protocolActionsInProgress')

	@property
	def ProtocolStackingMode(self):
		"""Decides whether protocol's sessions will started sequentially or parallelly across the layers

		Returns:
			str(parallel|sequential)
		"""
		return self._get_attribute('protocolStackingMode')
	@ProtocolStackingMode.setter
	def ProtocolStackingMode(self, value):
		self._set_attribute('protocolStackingMode', value)

	@property
	def Status(self):
		"""The current state of the scenario

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def Vports(self):
		"""List of virtual ports included in the port level configuration

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('vports')

	def AbortApplyOnTheFly(self):
		"""Executes the abortApplyOnTheFly operation on the server.

		Aborts any on the fly changes that are outstanding

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AbortApplyOnTheFly', payload=locals(), response_object=None)

	def ApplyOnTheFly(self):
		"""Executes the applyOnTheFly operation on the server.

		Apply any outstanding on the fly changes

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: Details about the operation's state.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ApplyOnTheFly', payload=locals(), response_object=None)

	def ConfigureAll(self):
		"""Executes the configureAll operation on the server.

		Configures all protocols in current scenario

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ConfigureAll', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology|/api/v1/sessions/1/ixnetwork/topology|/api/v1/sessions/1/ixnetwork/topology|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
