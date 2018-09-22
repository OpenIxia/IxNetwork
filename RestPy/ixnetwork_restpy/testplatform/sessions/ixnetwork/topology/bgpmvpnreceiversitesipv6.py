from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpMVpnReceiverSitesIpv6(Base):
	"""The BgpMVpnReceiverSitesIpv6 class encapsulates a user managed bgpMVpnReceiverSitesIpv6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpMVpnReceiverSitesIpv6 property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bgpMVpnReceiverSitesIpv6'

	def __init__(self, parent):
		super(BgpMVpnReceiverSitesIpv6, self).__init__(parent)

	@property
	def CMacProperties(self):
		"""An instance of the CMacProperties class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return CMacProperties(self)

	@property
	def EvpnIPv4PrefixRange(self):
		"""An instance of the EvpnIPv4PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return EvpnIPv4PrefixRange(self)

	@property
	def EvpnIPv6PrefixRange(self):
		"""An instance of the EvpnIPv6PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return EvpnIPv6PrefixRange(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def BFRId(self):
		"""BFR-Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRId')

	@property
	def BFRIpv4Prefix(self):
		"""BFR IPv4 Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRIpv4Prefix')

	@property
	def BFRIpv6Prefix(self):
		"""BFR IPv6 Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRIpv6Prefix')

	@property
	def BFRPrefixType(self):
		"""BFR Prefix Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRPrefixType')

	@property
	def SubDomainId(self):
		"""Sub-Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('SubDomainId')

	@property
	def UseAutoSubDomainId(self):
		"""Use Auto Sub-Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('UseAutoSubDomainId')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def CMulticastRouteType(self):
		"""C-Multicast Route Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cMulticastRouteType')

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
	def DownstreamLabel(self):
		"""Downstream Assigned Label in Leaf A-D route when tunnel type is Ingress Replication

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('downstreamLabel')

	@property
	def GroupAddressCount(self):
		"""Group Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressCount')

	@property
	def GroupMaskWidth(self):
		"""Group Mask Width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupMaskWidth')

	@property
	def IncludeBierPtainLeafAd(self):
		"""Include Bier PTA in Leaf A-D

		Returns:
			bool
		"""
		return self._get_attribute('includeBierPtainLeafAd')
	@IncludeBierPtainLeafAd.setter
	def IncludeBierPtainLeafAd(self, value):
		self._set_attribute('includeBierPtainLeafAd', value)

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
	def SendTriggeredMulticastRoute(self):
		"""Send Triggered Multicast Route

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendTriggeredMulticastRoute')

	@property
	def SourceAddressCount(self):
		"""Source Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressCount')

	@property
	def SourceGroupMapping(self):
		"""Source Group Mapping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceGroupMapping')

	@property
	def SourceMaskWidth(self):
		"""Source Mask Width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceMaskWidth')

	@property
	def StartGroupAddressIpv6(self):
		"""Start Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressIpv6')

	@property
	def StartSourceAddressIpv6(self):
		"""Start Source Address IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSourceAddressIpv6')

	@property
	def StartSourceOrCrpAddressIpv6(self):
		"""C-RP Address IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSourceOrCrpAddressIpv6')

	@property
	def SupportLeafADRoutesSending(self):
		"""Support Leaf A-D Routes Sending

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportLeafADRoutesSending')

	@property
	def WildCardLeafAdForBierPta(self):
		"""Wildcard Leaf A-D For Bier PTA

		Returns:
			bool
		"""
		return self._get_attribute('wildCardLeafAdForBierPta')
	@WildCardLeafAdForBierPta.setter
	def WildCardLeafAdForBierPta(self, value):
		self._set_attribute('wildCardLeafAdForBierPta', value)

	def add(self, IncludeBierPtainLeafAd=None, Name=None, WildCardLeafAdForBierPta=None):
		"""Adds a new bgpMVpnReceiverSitesIpv6 node on the server and retrieves it in this instance.

		Args:
			IncludeBierPtainLeafAd (bool): Include Bier PTA in Leaf A-D
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			WildCardLeafAdForBierPta (bool): Wildcard Leaf A-D For Bier PTA

		Returns:
			self: This instance with all currently retrieved bgpMVpnReceiverSitesIpv6 data using find and the newly added bgpMVpnReceiverSitesIpv6 data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bgpMVpnReceiverSitesIpv6 data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, DescriptiveName=None, IncludeBierPtainLeafAd=None, Name=None, WildCardLeafAdForBierPta=None):
		"""Finds and retrieves bgpMVpnReceiverSitesIpv6 data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpMVpnReceiverSitesIpv6 data from the server.
		By default the find method takes no parameters and will retrieve all bgpMVpnReceiverSitesIpv6 data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			IncludeBierPtainLeafAd (bool): Include Bier PTA in Leaf A-D
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			WildCardLeafAdForBierPta (bool): Wildcard Leaf A-D For Bier PTA

		Returns:
			self: This instance with matching bgpMVpnReceiverSitesIpv6 data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpMVpnReceiverSitesIpv6 data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpMVpnReceiverSitesIpv6 data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
