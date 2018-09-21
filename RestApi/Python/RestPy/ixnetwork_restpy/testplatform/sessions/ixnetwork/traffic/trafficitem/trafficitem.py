from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrafficItem(Base):
	"""The TrafficItem class encapsulates a user managed trafficItem node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrafficItem property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trafficItem'

	def __init__(self, parent):
		super(TrafficItem, self).__init__(parent)

	@property
	def AppLibProfile(self):
		"""An instance of the AppLibProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile.AppLibProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibprofile import AppLibProfile
		return AppLibProfile(self)

	@property
	def ConfigElement(self):
		"""An instance of the ConfigElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.configelement.ConfigElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.configelement import ConfigElement
		return ConfigElement(self)

	@property
	def DynamicUpdate(self):
		"""An instance of the DynamicUpdate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.dynamicupdate.dynamicupdate.DynamicUpdate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.dynamicupdate.dynamicupdate import DynamicUpdate
		return DynamicUpdate(self)

	@property
	def EgressTracking(self):
		"""An instance of the EgressTracking class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking.EgressTracking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.egresstracking import EgressTracking
		return EgressTracking(self)

	@property
	def EndpointSet(self):
		"""An instance of the EndpointSet class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset.EndpointSet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.endpointset.endpointset import EndpointSet
		return EndpointSet(self)

	@property
	def HighLevelStream(self):
		"""An instance of the HighLevelStream class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.highlevelstream.HighLevelStream)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.highlevelstream import HighLevelStream
		return HighLevelStream(self)

	@property
	def Tracking(self):
		"""An instance of the Tracking class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.tracking.Tracking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.tracking import Tracking
		return Tracking(self)

	@property
	def TransmissionDistribution(self):
		"""An instance of the TransmissionDistribution class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.transmissiondistribution.transmissiondistribution.TransmissionDistribution)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.transmissiondistribution.transmissiondistribution import TransmissionDistribution
		return TransmissionDistribution(self)

	@property
	def AllowSelfDestined(self):
		"""If true, this helps to send traffic from routes on an Ixia port to other routes on the same Ixia port.

		Returns:
			bool
		"""
		return self._get_attribute('allowSelfDestined')
	@AllowSelfDestined.setter
	def AllowSelfDestined(self, value):
		self._set_attribute('allowSelfDestined', value)

	@property
	def BiDirectional(self):
		"""If true, this enables traffic to be sent in forward and reverse destination.

		Returns:
			bool
		"""
		return self._get_attribute('biDirectional')
	@BiDirectional.setter
	def BiDirectional(self, value):
		self._set_attribute('biDirectional', value)

	@property
	def EgressEnabled(self):
		"""Enables the egress.

		Returns:
			bool
		"""
		return self._get_attribute('egressEnabled')
	@EgressEnabled.setter
	def EgressEnabled(self, value):
		self._set_attribute('egressEnabled', value)

	@property
	def EnableDynamicMplsLabelValues(self):
		"""Enables the dynamic MPLS label values.

		Returns:
			bool
		"""
		return self._get_attribute('enableDynamicMplsLabelValues')
	@EnableDynamicMplsLabelValues.setter
	def EnableDynamicMplsLabelValues(self, value):
		self._set_attribute('enableDynamicMplsLabelValues', value)

	@property
	def Enabled(self):
		"""If true, this enables the selected traffic item.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Errors(self):
		"""Displays the errors.

		Returns:
			list(str)
		"""
		return self._get_attribute('errors')

	@property
	def FlowGroupCount(self):
		"""Indicates the number of flow groups.

		Returns:
			number
		"""
		return self._get_attribute('flowGroupCount')

	@property
	def HasOpenFlow(self):
		"""Indicates whether or not this trafficItem has openflow.

		Returns:
			bool
		"""
		return self._get_attribute('hasOpenFlow')
	@HasOpenFlow.setter
	def HasOpenFlow(self, value):
		self._set_attribute('hasOpenFlow', value)

	@property
	def HostsPerNetwork(self):
		"""The number of emulated hosts for the traffic stream.

		Returns:
			number
		"""
		return self._get_attribute('hostsPerNetwork')
	@HostsPerNetwork.setter
	def HostsPerNetwork(self, value):
		self._set_attribute('hostsPerNetwork', value)

	@property
	def InterAsBgpPreference(self):
		"""Signifies the inter as BGP prefence

		Returns:
			str(one|two)
		"""
		return self._get_attribute('interAsBgpPreference')
	@InterAsBgpPreference.setter
	def InterAsBgpPreference(self, value):
		self._set_attribute('interAsBgpPreference', value)

	@property
	def InterAsLdpPreference(self):
		"""Preferences inter as LDP

		Returns:
			str(one|two)
		"""
		return self._get_attribute('interAsLdpPreference')
	@InterAsLdpPreference.setter
	def InterAsLdpPreference(self, value):
		self._set_attribute('interAsLdpPreference', value)

	@property
	def MaxNumberOfVpnLabelStack(self):
		"""Signifies the maximum number of VPN label stack

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfVpnLabelStack')
	@MaxNumberOfVpnLabelStack.setter
	def MaxNumberOfVpnLabelStack(self, value):
		self._set_attribute('maxNumberOfVpnLabelStack', value)

	@property
	def MergeDestinations(self):
		"""If true, merges the traffic flow in the destination ranges.

		Returns:
			bool
		"""
		return self._get_attribute('mergeDestinations')
	@MergeDestinations.setter
	def MergeDestinations(self, value):
		self._set_attribute('mergeDestinations', value)

	@property
	def MulticastForwardingMode(self):
		"""

		Returns:
			str(loadBalancing|replication)
		"""
		return self._get_attribute('multicastForwardingMode')
	@MulticastForwardingMode.setter
	def MulticastForwardingMode(self, value):
		self._set_attribute('multicastForwardingMode', value)

	@property
	def Name(self):
		"""The name of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NumVlansForMulticastReplication(self):
		"""Set the number of vlans for multicast replication

		Returns:
			number
		"""
		return self._get_attribute('numVlansForMulticastReplication')
	@NumVlansForMulticastReplication.setter
	def NumVlansForMulticastReplication(self, value):
		self._set_attribute('numVlansForMulticastReplication', value)

	@property
	def OrdinalNo(self):
		"""Signifies the ordinal number

		Returns:
			number
		"""
		return self._get_attribute('ordinalNo')
	@OrdinalNo.setter
	def OrdinalNo(self, value):
		self._set_attribute('ordinalNo', value)

	@property
	def OriginatorType(self):
		"""Indicates who created this trafficItem.

		Returns:
			str(endUser|quickTest)
		"""
		return self._get_attribute('originatorType')
	@OriginatorType.setter
	def OriginatorType(self, value):
		self._set_attribute('originatorType', value)

	@property
	def RoundRobinPacketOrdering(self):
		"""This option enables Round Robin Packet Ordering within endpoints across Rx ports.

		Returns:
			bool
		"""
		return self._get_attribute('roundRobinPacketOrdering')
	@RoundRobinPacketOrdering.setter
	def RoundRobinPacketOrdering(self, value):
		self._set_attribute('roundRobinPacketOrdering', value)

	@property
	def RouteMesh(self):
		"""The traffic flow type between each pair of source route endpoint and destination route endpoint.

		Returns:
			str(fullMesh|oneToOne)
		"""
		return self._get_attribute('routeMesh')
	@RouteMesh.setter
	def RouteMesh(self, value):
		self._set_attribute('routeMesh', value)

	@property
	def SrcDestMesh(self):
		"""Select the options to set the traffic mesh type between the Source Endpoint and Destination endpoint.

		Returns:
			str(fullMesh|manyToMany|none|oneToOne)
		"""
		return self._get_attribute('srcDestMesh')
	@SrcDestMesh.setter
	def SrcDestMesh(self, value):
		self._set_attribute('srcDestMesh', value)

	@property
	def State(self):
		"""(Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def Suspend(self):
		"""Suspends all traffic on this stream.

		Returns:
			bool
		"""
		return self._get_attribute('suspend')
	@Suspend.setter
	def Suspend(self, value):
		self._set_attribute('suspend', value)

	@property
	def TrafficItemType(self):
		"""Helps to configure and edit a traffic item that is sent across Ixia ports.

		Returns:
			str(application|applicationLibrary|l2L3|quick)
		"""
		return self._get_attribute('trafficItemType')
	@TrafficItemType.setter
	def TrafficItemType(self, value):
		self._set_attribute('trafficItemType', value)

	@property
	def TrafficType(self):
		"""Helps to select the type of traffic endpoint to be configured.

		Returns:
			str(atm|avb1722|avbRaw|ethernetVlan|fc|fcoe|frameRelay|hdlc|ipv4|ipv4ApplicationTraffic|ipv6|ipv6ApplicationTraffic|ppp|raw)
		"""
		return self._get_attribute('trafficType')
	@TrafficType.setter
	def TrafficType(self, value):
		self._set_attribute('trafficType', value)

	@property
	def TransmitMode(self):
		"""The transmit mode for this traffic item

		Returns:
			str(interleaved|sequential)
		"""
		return self._get_attribute('transmitMode')
	@TransmitMode.setter
	def TransmitMode(self, value):
		self._set_attribute('transmitMode', value)

	@property
	def TransportLdpPreference(self):
		"""Transports LDP preference

		Returns:
			str(one|two)
		"""
		return self._get_attribute('transportLdpPreference')
	@TransportLdpPreference.setter
	def TransportLdpPreference(self, value):
		self._set_attribute('transportLdpPreference', value)

	@property
	def TransportRsvpTePreference(self):
		"""Transports RSVP TE preference

		Returns:
			str(one|two)
		"""
		return self._get_attribute('transportRsvpTePreference')
	@TransportRsvpTePreference.setter
	def TransportRsvpTePreference(self, value):
		self._set_attribute('transportRsvpTePreference', value)

	@property
	def UseControlPlaneFrameSize(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useControlPlaneFrameSize')
	@UseControlPlaneFrameSize.setter
	def UseControlPlaneFrameSize(self, value):
		self._set_attribute('useControlPlaneFrameSize', value)

	@property
	def UseControlPlaneRate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useControlPlaneRate')
	@UseControlPlaneRate.setter
	def UseControlPlaneRate(self, value):
		self._set_attribute('useControlPlaneRate', value)

	@property
	def Warnings(self):
		"""Displays the warnings.

		Returns:
			list(str)
		"""
		return self._get_attribute('warnings')

	def add(self, AllowSelfDestined=None, BiDirectional=None, EgressEnabled=None, EnableDynamicMplsLabelValues=None, Enabled=None, HasOpenFlow=None, HostsPerNetwork=None, InterAsBgpPreference=None, InterAsLdpPreference=None, MaxNumberOfVpnLabelStack=None, MergeDestinations=None, MulticastForwardingMode=None, Name=None, NumVlansForMulticastReplication=None, OrdinalNo=None, OriginatorType=None, RoundRobinPacketOrdering=None, RouteMesh=None, SrcDestMesh=None, Suspend=None, TrafficItemType=None, TrafficType=None, TransmitMode=None, TransportLdpPreference=None, TransportRsvpTePreference=None, UseControlPlaneFrameSize=None, UseControlPlaneRate=None):
		"""Adds a new trafficItem node on the server and retrieves it in this instance.

		Args:
			AllowSelfDestined (bool): If true, this helps to send traffic from routes on an Ixia port to other routes on the same Ixia port.
			BiDirectional (bool): If true, this enables traffic to be sent in forward and reverse destination.
			EgressEnabled (bool): Enables the egress.
			EnableDynamicMplsLabelValues (bool): Enables the dynamic MPLS label values.
			Enabled (bool): If true, this enables the selected traffic item.
			HasOpenFlow (bool): Indicates whether or not this trafficItem has openflow.
			HostsPerNetwork (number): The number of emulated hosts for the traffic stream.
			InterAsBgpPreference (str(one|two)): Signifies the inter as BGP prefence
			InterAsLdpPreference (str(one|two)): Preferences inter as LDP
			MaxNumberOfVpnLabelStack (number): Signifies the maximum number of VPN label stack
			MergeDestinations (bool): If true, merges the traffic flow in the destination ranges.
			MulticastForwardingMode (str(loadBalancing|replication)): 
			Name (str): The name of the traffic item.
			NumVlansForMulticastReplication (number): Set the number of vlans for multicast replication
			OrdinalNo (number): Signifies the ordinal number
			OriginatorType (str(endUser|quickTest)): Indicates who created this trafficItem.
			RoundRobinPacketOrdering (bool): This option enables Round Robin Packet Ordering within endpoints across Rx ports.
			RouteMesh (str(fullMesh|oneToOne)): The traffic flow type between each pair of source route endpoint and destination route endpoint.
			SrcDestMesh (str(fullMesh|manyToMany|none|oneToOne)): Select the options to set the traffic mesh type between the Source Endpoint and Destination endpoint.
			Suspend (bool): Suspends all traffic on this stream.
			TrafficItemType (str(application|applicationLibrary|l2L3|quick)): Helps to configure and edit a traffic item that is sent across Ixia ports.
			TrafficType (str(atm|avb1722|avbRaw|ethernetVlan|fc|fcoe|frameRelay|hdlc|ipv4|ipv4ApplicationTraffic|ipv6|ipv6ApplicationTraffic|ppp|raw)): Helps to select the type of traffic endpoint to be configured.
			TransmitMode (str(interleaved|sequential)): The transmit mode for this traffic item
			TransportLdpPreference (str(one|two)): Transports LDP preference
			TransportRsvpTePreference (str(one|two)): Transports RSVP TE preference
			UseControlPlaneFrameSize (bool): 
			UseControlPlaneRate (bool): 

		Returns:
			self: This instance with all currently retrieved trafficItem data using find and the newly added trafficItem data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trafficItem data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AllowSelfDestined=None, BiDirectional=None, EgressEnabled=None, EnableDynamicMplsLabelValues=None, Enabled=None, Errors=None, FlowGroupCount=None, HasOpenFlow=None, HostsPerNetwork=None, InterAsBgpPreference=None, InterAsLdpPreference=None, MaxNumberOfVpnLabelStack=None, MergeDestinations=None, MulticastForwardingMode=None, Name=None, NumVlansForMulticastReplication=None, OrdinalNo=None, OriginatorType=None, RoundRobinPacketOrdering=None, RouteMesh=None, SrcDestMesh=None, State=None, Suspend=None, TrafficItemType=None, TrafficType=None, TransmitMode=None, TransportLdpPreference=None, TransportRsvpTePreference=None, UseControlPlaneFrameSize=None, UseControlPlaneRate=None, Warnings=None):
		"""Finds and retrieves trafficItem data from the server.

		All named parameters support regex and can be used to selectively retrieve trafficItem data from the server.
		By default the find method takes no parameters and will retrieve all trafficItem data from the server.

		Args:
			AllowSelfDestined (bool): If true, this helps to send traffic from routes on an Ixia port to other routes on the same Ixia port.
			BiDirectional (bool): If true, this enables traffic to be sent in forward and reverse destination.
			EgressEnabled (bool): Enables the egress.
			EnableDynamicMplsLabelValues (bool): Enables the dynamic MPLS label values.
			Enabled (bool): If true, this enables the selected traffic item.
			Errors (list(str)): Displays the errors.
			FlowGroupCount (number): Indicates the number of flow groups.
			HasOpenFlow (bool): Indicates whether or not this trafficItem has openflow.
			HostsPerNetwork (number): The number of emulated hosts for the traffic stream.
			InterAsBgpPreference (str(one|two)): Signifies the inter as BGP prefence
			InterAsLdpPreference (str(one|two)): Preferences inter as LDP
			MaxNumberOfVpnLabelStack (number): Signifies the maximum number of VPN label stack
			MergeDestinations (bool): If true, merges the traffic flow in the destination ranges.
			MulticastForwardingMode (str(loadBalancing|replication)): 
			Name (str): The name of the traffic item.
			NumVlansForMulticastReplication (number): Set the number of vlans for multicast replication
			OrdinalNo (number): Signifies the ordinal number
			OriginatorType (str(endUser|quickTest)): Indicates who created this trafficItem.
			RoundRobinPacketOrdering (bool): This option enables Round Robin Packet Ordering within endpoints across Rx ports.
			RouteMesh (str(fullMesh|oneToOne)): The traffic flow type between each pair of source route endpoint and destination route endpoint.
			SrcDestMesh (str(fullMesh|manyToMany|none|oneToOne)): Select the options to set the traffic mesh type between the Source Endpoint and Destination endpoint.
			State (str): (Read only) A read-only field which indicates the current state of the traffic item.
			Suspend (bool): Suspends all traffic on this stream.
			TrafficItemType (str(application|applicationLibrary|l2L3|quick)): Helps to configure and edit a traffic item that is sent across Ixia ports.
			TrafficType (str(atm|avb1722|avbRaw|ethernetVlan|fc|fcoe|frameRelay|hdlc|ipv4|ipv4ApplicationTraffic|ipv6|ipv6ApplicationTraffic|ppp|raw)): Helps to select the type of traffic endpoint to be configured.
			TransmitMode (str(interleaved|sequential)): The transmit mode for this traffic item
			TransportLdpPreference (str(one|two)): Transports LDP preference
			TransportRsvpTePreference (str(one|two)): Transports RSVP TE preference
			UseControlPlaneFrameSize (bool): 
			UseControlPlaneRate (bool): 
			Warnings (list(str)): Displays the warnings.

		Returns:
			self: This instance with matching trafficItem data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trafficItem data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trafficItem data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ConvertToRaw(self):
		"""Executes the convertToRaw operation on the server.

		Converts a non-raw traffic item to a raw traffic item.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ConvertToRaw', payload=locals(), response_object=None)

	def Duplicate(self, Arg2):
		"""Executes the duplicate operation on the server.

		Duplicates a specific traffic item.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem)): The method internally set Arg1 to the current href for this instance
			Arg2 (number): The number of times to duplicate the traffic item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Duplicate', payload=locals(), response_object=None)

	def DuplicateItems(self):
		"""Executes the duplicateItems operation on the server.

		Duplicates a list of traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('DuplicateItems', payload=locals(), response_object=None)

	def Generate(self):
		"""Executes the generate operation on the server.

		Generate traffic for specific traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Generate', payload=locals(), response_object=None)

	def Generate(self):
		"""Executes the generate operation on the server.

		Generate traffic for a specific traffic item.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Generate', payload=locals(), response_object=None)

	def ResolveAptixiaEndpoints(self):
		"""Executes the resolveAptixiaEndpoints operation on the server.

		Resolves /vport/protocolStack/. endpoints being used by a specific traffic item.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Returns:
			str: This exec returns a string containing the resolved endpoints.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResolveAptixiaEndpoints', payload=locals(), response_object=None)

	def StartDefaultLearning(self):
		"""Executes the startDefaultLearning operation on the server.

		Starts default learning for a list of traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartDefaultLearning', payload=locals(), response_object=None)

	def StartDefaultLearning(self):
		"""Executes the startDefaultLearning operation on the server.

		Starts default learning for a specific traffic item.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartDefaultLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg2, Arg3, Arg4):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.
			Arg5 (bool): Send gratuitous ARP frames.
			Arg6 (bool): Send MAC frames.
			Arg7 (bool): Send Fast Path frames.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartLearning', payload=locals(), response_object=None)

	def StartLearning(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7, Arg8):
		"""Executes the startLearning operation on the server.

		Sends learning frames.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (number): The framesize of the learning frame.
			Arg3 (number): The framecount of the learning frames.
			Arg4 (number): The frames per second of the learning frames.
			Arg5 (bool): Send gratuitous ARP frames.
			Arg6 (bool): Send MAC frames.
			Arg7 (bool): Send Fast Path frames.
			Arg8 (bool): Send full mesh.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartLearning', payload=locals(), response_object=None)

	def StartStatelessTraffic(self):
		"""Executes the startStatelessTraffic operation on the server.

		Start the traffic configuration for stateless traffic items only.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartStatelessTraffic', payload=locals(), response_object=None)

	def StartStatelessTrafficBlocking(self):
		"""Executes the startStatelessTrafficBlocking operation on the server.

		Start the traffic configuration for stateless traffic items only. This will block until traffic is fully started.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartStatelessTrafficBlocking', payload=locals(), response_object=None)

	def StopStatelessTraffic(self):
		"""Executes the stopStatelessTraffic operation on the server.

		Stop the stateless traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopStatelessTraffic', payload=locals(), response_object=None)

	def StopStatelessTrafficBlocking(self):
		"""Executes the stopStatelessTrafficBlocking operation on the server.

		Stop the traffic configuration for stateless traffic items only. This will block until traffic is fully stopped.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopStatelessTrafficBlocking', payload=locals(), response_object=None)
