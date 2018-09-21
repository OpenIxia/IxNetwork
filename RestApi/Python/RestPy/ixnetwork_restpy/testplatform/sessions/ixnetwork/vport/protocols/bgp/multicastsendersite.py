from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MulticastSenderSite(Base):
	"""The MulticastSenderSite class encapsulates a user managed multicastSenderSite node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastSenderSite property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastSenderSite'

	def __init__(self, parent):
		super(MulticastSenderSite, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def AddressFamilyType(self):
		"""Indicates the IPv4/IPv6 interface id of the router.

		Returns:
			str(addressFamilyIpv4|addressFamilyIpv6)
		"""
		return self._get_attribute('addressFamilyType')
	@AddressFamilyType.setter
	def AddressFamilyType(self, value):
		self._set_attribute('addressFamilyType', value)

	@property
	def Enabled(self):
		"""Enables or disables use of the multicast Sender site.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GroupAddressCount(self):
		"""The number of group addresses to be included in the Register message.

		Returns:
			number
		"""
		return self._get_attribute('groupAddressCount')
	@GroupAddressCount.setter
	def GroupAddressCount(self, value):
		self._set_attribute('groupAddressCount', value)

	@property
	def GroupMaskWidth(self):
		"""The number of bits in the network mask used with the Group Address.

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')
	@GroupMaskWidth.setter
	def GroupMaskWidth(self, value):
		self._set_attribute('groupMaskWidth', value)

	@property
	def IncludeIpv6ExplicitNullLabel(self):
		"""If true, allows to include Explicit NULL label (2) in I-PMSI IPv6 PE-to-CE Traffic.

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv6ExplicitNullLabel')
	@IncludeIpv6ExplicitNullLabel.setter
	def IncludeIpv6ExplicitNullLabel(self, value):
		self._set_attribute('includeIpv6ExplicitNullLabel', value)

	@property
	def MplsAssignedUpstreamLabel(self):
		"""This helps to assign unique upstream assigned label for each flow. This is applicable only if Use Upstream Assigned Label is true.

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamLabel')
	@MplsAssignedUpstreamLabel.setter
	def MplsAssignedUpstreamLabel(self, value):
		self._set_attribute('mplsAssignedUpstreamLabel', value)

	@property
	def MplsAssignedUpstreamLabelStep(self):
		"""S-PMSI A-D route is sent with this Upstream Label. This is applicable only if Use Upstream Assigned Label is true.

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamLabelStep')
	@MplsAssignedUpstreamLabelStep.setter
	def MplsAssignedUpstreamLabelStep(self, value):
		self._set_attribute('mplsAssignedUpstreamLabelStep', value)

	@property
	def SPmsiRsvpP2mpId(self):
		"""The P2MP Id represented in IP address format.

		Returns:
			str
		"""
		return self._get_attribute('sPmsiRsvpP2mpId')
	@SPmsiRsvpP2mpId.setter
	def SPmsiRsvpP2mpId(self, value):
		self._set_attribute('sPmsiRsvpP2mpId', value)

	@property
	def SPmsiRsvpP2mpIdAsNumber(self):
		"""The P2MP Id represented in integer format.

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpP2mpIdAsNumber')
	@SPmsiRsvpP2mpIdAsNumber.setter
	def SPmsiRsvpP2mpIdAsNumber(self, value):
		self._set_attribute('sPmsiRsvpP2mpIdAsNumber', value)

	@property
	def SPmsiRsvpP2mpIdStep(self):
		"""Indicates the P2MP ID. This accepts only integer values.

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpP2mpIdStep')
	@SPmsiRsvpP2mpIdStep.setter
	def SPmsiRsvpP2mpIdStep(self, value):
		self._set_attribute('sPmsiRsvpP2mpIdStep', value)

	@property
	def SPmsiRsvpTunnelCount(self):
		"""The total count of the S-PMSI RSVP Tunnel Count.

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelCount')
	@SPmsiRsvpTunnelCount.setter
	def SPmsiRsvpTunnelCount(self, value):
		self._set_attribute('sPmsiRsvpTunnelCount', value)

	@property
	def SPmsiRsvpTunnelId(self):
		"""The first Tunnel ID value in the range of Tunnel IDs.

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelId')
	@SPmsiRsvpTunnelId.setter
	def SPmsiRsvpTunnelId(self, value):
		self._set_attribute('sPmsiRsvpTunnelId', value)

	@property
	def SPmsiRsvpTunnelIdStep(self):
		"""Indicates the P2MP ID. This accepts only integer values.

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelIdStep')
	@SPmsiRsvpTunnelIdStep.setter
	def SPmsiRsvpTunnelIdStep(self, value):
		self._set_attribute('sPmsiRsvpTunnelIdStep', value)

	@property
	def SPmsiTrafficGroupId(self):
		"""Creates traffic using MPLS Labels of S-PMSI Tunnel and S-PMSI Upstream Assigned Label.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('sPmsiTrafficGroupId')
	@SPmsiTrafficGroupId.setter
	def SPmsiTrafficGroupId(self, value):
		self._set_attribute('sPmsiTrafficGroupId', value)

	@property
	def SPmsiTunnelCount(self):
		"""Signifies the SPMSI tunnel count

		Returns:
			number
		"""
		return self._get_attribute('sPmsiTunnelCount')
	@SPmsiTunnelCount.setter
	def SPmsiTunnelCount(self, value):
		self._set_attribute('sPmsiTunnelCount', value)

	@property
	def SendTriggeredSourceActiveAdRoute(self):
		"""If true, allows to send the Source Active A-D Route after receiving Source Tree Join C-Multicast route.

		Returns:
			bool
		"""
		return self._get_attribute('sendTriggeredSourceActiveAdRoute')
	@SendTriggeredSourceActiveAdRoute.setter
	def SendTriggeredSourceActiveAdRoute(self, value):
		self._set_attribute('sendTriggeredSourceActiveAdRoute', value)

	@property
	def SetLeafInformationRequiredBit(self):
		"""his is used to send S-PMSI A-D Route with Leaf Information Required bit Set.

		Returns:
			bool
		"""
		return self._get_attribute('setLeafInformationRequiredBit')
	@SetLeafInformationRequiredBit.setter
	def SetLeafInformationRequiredBit(self, value):
		self._set_attribute('setLeafInformationRequiredBit', value)

	@property
	def SourceAddressCount(self):
		"""The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values of the Source Address and the Source Mask Width.

		Returns:
			number
		"""
		return self._get_attribute('sourceAddressCount')
	@SourceAddressCount.setter
	def SourceAddressCount(self, value):
		self._set_attribute('sourceAddressCount', value)

	@property
	def SourceGroupMapping(self):
		"""Indicates the source group mapping.

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def SourceMaskWidth(self):
		"""The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.

		Returns:
			number
		"""
		return self._get_attribute('sourceMaskWidth')
	@SourceMaskWidth.setter
	def SourceMaskWidth(self, value):
		self._set_attribute('sourceMaskWidth', value)

	@property
	def StartGroupAddress(self):
		"""The first IPv4 or IPv6 Multicast group address in the range of group addresses included in this Register message.

		Returns:
			str
		"""
		return self._get_attribute('startGroupAddress')
	@StartGroupAddress.setter
	def StartGroupAddress(self, value):
		self._set_attribute('startGroupAddress', value)

	@property
	def StartSourceAddress(self):
		"""The first IPv4 or IPv6 source address to be included in this Register message.

		Returns:
			str
		"""
		return self._get_attribute('startSourceAddress')
	@StartSourceAddress.setter
	def StartSourceAddress(self, value):
		self._set_attribute('startSourceAddress', value)

	@property
	def TuunelType(self):
		"""the tunnel type.

		Returns:
			str()
		"""
		return self._get_attribute('tuunelType')
	@TuunelType.setter
	def TuunelType(self, value):
		self._set_attribute('tuunelType', value)

	@property
	def UseUpstreamAssignedLabel(self):
		"""Indicates whether upstream label as configured be used or not. If this field is false, then MPLS Assigned Upstream Label and MPLS Assigned Upstream Label Step fields are disabled.

		Returns:
			bool
		"""
		return self._get_attribute('useUpstreamAssignedLabel')
	@UseUpstreamAssignedLabel.setter
	def UseUpstreamAssignedLabel(self, value):
		self._set_attribute('useUpstreamAssignedLabel', value)

	def add(self, AddressFamilyType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, IncludeIpv6ExplicitNullLabel=None, MplsAssignedUpstreamLabel=None, MplsAssignedUpstreamLabelStep=None, SPmsiRsvpP2mpId=None, SPmsiRsvpP2mpIdAsNumber=None, SPmsiRsvpP2mpIdStep=None, SPmsiRsvpTunnelCount=None, SPmsiRsvpTunnelId=None, SPmsiRsvpTunnelIdStep=None, SPmsiTrafficGroupId=None, SPmsiTunnelCount=None, SendTriggeredSourceActiveAdRoute=None, SetLeafInformationRequiredBit=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, TuunelType=None, UseUpstreamAssignedLabel=None):
		"""Adds a new multicastSenderSite node on the server and retrieves it in this instance.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): Indicates the IPv4/IPv6 interface id of the router.
			Enabled (bool): Enables or disables use of the multicast Sender site.
			GroupAddressCount (number): The number of group addresses to be included in the Register message.
			GroupMaskWidth (number): The number of bits in the network mask used with the Group Address.
			IncludeIpv6ExplicitNullLabel (bool): If true, allows to include Explicit NULL label (2) in I-PMSI IPv6 PE-to-CE Traffic.
			MplsAssignedUpstreamLabel (number): This helps to assign unique upstream assigned label for each flow. This is applicable only if Use Upstream Assigned Label is true.
			MplsAssignedUpstreamLabelStep (number): S-PMSI A-D route is sent with this Upstream Label. This is applicable only if Use Upstream Assigned Label is true.
			SPmsiRsvpP2mpId (str): The P2MP Id represented in IP address format.
			SPmsiRsvpP2mpIdAsNumber (number): The P2MP Id represented in integer format.
			SPmsiRsvpP2mpIdStep (number): Indicates the P2MP ID. This accepts only integer values.
			SPmsiRsvpTunnelCount (number): The total count of the S-PMSI RSVP Tunnel Count.
			SPmsiRsvpTunnelId (number): The first Tunnel ID value in the range of Tunnel IDs.
			SPmsiRsvpTunnelIdStep (number): Indicates the P2MP ID. This accepts only integer values.
			SPmsiTrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Creates traffic using MPLS Labels of S-PMSI Tunnel and S-PMSI Upstream Assigned Label.
			SPmsiTunnelCount (number): Signifies the SPMSI tunnel count
			SendTriggeredSourceActiveAdRoute (bool): If true, allows to send the Source Active A-D Route after receiving Source Tree Join C-Multicast route.
			SetLeafInformationRequiredBit (bool): his is used to send S-PMSI A-D Route with Leaf Information Required bit Set.
			SourceAddressCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values of the Source Address and the Source Mask Width.
			SourceGroupMapping (str(fullyMeshed|oneToOne)): Indicates the source group mapping.
			SourceMaskWidth (number): The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.
			StartGroupAddress (str): The first IPv4 or IPv6 Multicast group address in the range of group addresses included in this Register message.
			StartSourceAddress (str): The first IPv4 or IPv6 source address to be included in this Register message.
			TuunelType (str()): the tunnel type.
			UseUpstreamAssignedLabel (bool): Indicates whether upstream label as configured be used or not. If this field is false, then MPLS Assigned Upstream Label and MPLS Assigned Upstream Label Step fields are disabled.

		Returns:
			self: This instance with all currently retrieved multicastSenderSite data using find and the newly added multicastSenderSite data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastSenderSite data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddressFamilyType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, IncludeIpv6ExplicitNullLabel=None, MplsAssignedUpstreamLabel=None, MplsAssignedUpstreamLabelStep=None, SPmsiRsvpP2mpId=None, SPmsiRsvpP2mpIdAsNumber=None, SPmsiRsvpP2mpIdStep=None, SPmsiRsvpTunnelCount=None, SPmsiRsvpTunnelId=None, SPmsiRsvpTunnelIdStep=None, SPmsiTrafficGroupId=None, SPmsiTunnelCount=None, SendTriggeredSourceActiveAdRoute=None, SetLeafInformationRequiredBit=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, TuunelType=None, UseUpstreamAssignedLabel=None):
		"""Finds and retrieves multicastSenderSite data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastSenderSite data from the server.
		By default the find method takes no parameters and will retrieve all multicastSenderSite data from the server.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): Indicates the IPv4/IPv6 interface id of the router.
			Enabled (bool): Enables or disables use of the multicast Sender site.
			GroupAddressCount (number): The number of group addresses to be included in the Register message.
			GroupMaskWidth (number): The number of bits in the network mask used with the Group Address.
			IncludeIpv6ExplicitNullLabel (bool): If true, allows to include Explicit NULL label (2) in I-PMSI IPv6 PE-to-CE Traffic.
			MplsAssignedUpstreamLabel (number): This helps to assign unique upstream assigned label for each flow. This is applicable only if Use Upstream Assigned Label is true.
			MplsAssignedUpstreamLabelStep (number): S-PMSI A-D route is sent with this Upstream Label. This is applicable only if Use Upstream Assigned Label is true.
			SPmsiRsvpP2mpId (str): The P2MP Id represented in IP address format.
			SPmsiRsvpP2mpIdAsNumber (number): The P2MP Id represented in integer format.
			SPmsiRsvpP2mpIdStep (number): Indicates the P2MP ID. This accepts only integer values.
			SPmsiRsvpTunnelCount (number): The total count of the S-PMSI RSVP Tunnel Count.
			SPmsiRsvpTunnelId (number): The first Tunnel ID value in the range of Tunnel IDs.
			SPmsiRsvpTunnelIdStep (number): Indicates the P2MP ID. This accepts only integer values.
			SPmsiTrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Creates traffic using MPLS Labels of S-PMSI Tunnel and S-PMSI Upstream Assigned Label.
			SPmsiTunnelCount (number): Signifies the SPMSI tunnel count
			SendTriggeredSourceActiveAdRoute (bool): If true, allows to send the Source Active A-D Route after receiving Source Tree Join C-Multicast route.
			SetLeafInformationRequiredBit (bool): his is used to send S-PMSI A-D Route with Leaf Information Required bit Set.
			SourceAddressCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values of the Source Address and the Source Mask Width.
			SourceGroupMapping (str(fullyMeshed|oneToOne)): Indicates the source group mapping.
			SourceMaskWidth (number): The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.
			StartGroupAddress (str): The first IPv4 or IPv6 Multicast group address in the range of group addresses included in this Register message.
			StartSourceAddress (str): The first IPv4 or IPv6 source address to be included in this Register message.
			TuunelType (str()): the tunnel type.
			UseUpstreamAssignedLabel (bool): Indicates whether upstream label as configured be used or not. If this field is false, then MPLS Assigned Upstream Label and MPLS Assigned Upstream Label Step fields are disabled.

		Returns:
			self: This instance with matching multicastSenderSite data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastSenderSite data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastSenderSite data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SwitchToSpmsi(self):
		"""Executes the switchToSpmsi operation on the server.

		This exec switches the tunnel to sPMSI.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=multicastSenderSite)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SwitchToSpmsi', payload=locals(), response_object=None)
