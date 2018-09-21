from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MulticastReceiverSite(Base):
	"""The MulticastReceiverSite class encapsulates a user managed multicastReceiverSite node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastReceiverSite property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastReceiverSite'

	def __init__(self, parent):
		super(MulticastReceiverSite, self).__init__(parent)

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
	def CMcastRouteType(self):
		"""The C-Multicast Route Type.

		Returns:
			str(sourceTreeJoin|sharedTreeJoin)
		"""
		return self._get_attribute('cMcastRouteType')
	@CMcastRouteType.setter
	def CMcastRouteType(self, value):
		self._set_attribute('cMcastRouteType', value)

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
	def SendTriggeredCmulticastRoute(self):
		"""This helps to send Source Tree Join C-Multicast route after receiving Source Active A-D route. This is also required by Shared Tree Join C-Multicast route to send Source Tree Join after receiving Source Active A-D Route.

		Returns:
			bool
		"""
		return self._get_attribute('sendTriggeredCmulticastRoute')
	@SendTriggeredCmulticastRoute.setter
	def SendTriggeredCmulticastRoute(self, value):
		self._set_attribute('sendTriggeredCmulticastRoute', value)

	@property
	def SourceAddressCount(self):
		"""The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. the default value is 0.

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
		"""The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.

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
		"""The first IPv4 or IPv6 source address to be included in this Register message.(IPv4 Multicast addresses are not valid for sources.).

		Returns:
			str
		"""
		return self._get_attribute('startSourceAddress')
	@StartSourceAddress.setter
	def StartSourceAddress(self, value):
		self._set_attribute('startSourceAddress', value)

	@property
	def SupportLeafAdRoutesSending(self):
		"""If true, helps IXIA to send Leaf A-D Route on receiving a S-PMSI A-D Route with the Leaf Information Required flag set. If false, IXIA shall not send the Leaf A-D Route even if such Update message is received.

		Returns:
			bool
		"""
		return self._get_attribute('supportLeafAdRoutesSending')
	@SupportLeafAdRoutesSending.setter
	def SupportLeafAdRoutesSending(self, value):
		self._set_attribute('supportLeafAdRoutesSending', value)

	def add(self, AddressFamilyType=None, CMcastRouteType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, SendTriggeredCmulticastRoute=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, SupportLeafAdRoutesSending=None):
		"""Adds a new multicastReceiverSite node on the server and retrieves it in this instance.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): Indicates the IPv4/IPv6 interface id of the router.
			CMcastRouteType (str(sourceTreeJoin|sharedTreeJoin)): The C-Multicast Route Type.
			Enabled (bool): Enables or disables use of the multicast Sender site.
			GroupAddressCount (number): The number of group addresses to be included in the Register message.
			GroupMaskWidth (number): The number of bits in the network mask used with the Group Address.
			SendTriggeredCmulticastRoute (bool): This helps to send Source Tree Join C-Multicast route after receiving Source Active A-D route. This is also required by Shared Tree Join C-Multicast route to send Source Tree Join after receiving Source Active A-D Route.
			SourceAddressCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. the default value is 0.
			SourceGroupMapping (str(fullyMeshed|oneToOne)): Indicates the source group mapping.
			SourceMaskWidth (number): The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.
			StartGroupAddress (str): The first IPv4 or IPv6 Multicast group address in the range of group addresses included in this Register message.
			StartSourceAddress (str): The first IPv4 or IPv6 source address to be included in this Register message.(IPv4 Multicast addresses are not valid for sources.).
			SupportLeafAdRoutesSending (bool): If true, helps IXIA to send Leaf A-D Route on receiving a S-PMSI A-D Route with the Leaf Information Required flag set. If false, IXIA shall not send the Leaf A-D Route even if such Update message is received.

		Returns:
			self: This instance with all currently retrieved multicastReceiverSite data using find and the newly added multicastReceiverSite data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastReceiverSite data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddressFamilyType=None, CMcastRouteType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, SendTriggeredCmulticastRoute=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, SupportLeafAdRoutesSending=None):
		"""Finds and retrieves multicastReceiverSite data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastReceiverSite data from the server.
		By default the find method takes no parameters and will retrieve all multicastReceiverSite data from the server.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): Indicates the IPv4/IPv6 interface id of the router.
			CMcastRouteType (str(sourceTreeJoin|sharedTreeJoin)): The C-Multicast Route Type.
			Enabled (bool): Enables or disables use of the multicast Sender site.
			GroupAddressCount (number): The number of group addresses to be included in the Register message.
			GroupMaskWidth (number): The number of bits in the network mask used with the Group Address.
			SendTriggeredCmulticastRoute (bool): This helps to send Source Tree Join C-Multicast route after receiving Source Active A-D route. This is also required by Shared Tree Join C-Multicast route to send Source Tree Join after receiving Source Active A-D Route.
			SourceAddressCount (number): The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. the default value is 0.
			SourceGroupMapping (str(fullyMeshed|oneToOne)): Indicates the source group mapping.
			SourceMaskWidth (number): The number of bits in the mask applied to the Source Address. (The masked bits in the Source Address form the address prefix.)The default value is 32. The valid range is 1 to 128, depending on address family type.Used for (S,G) Type and (S,G, rpt) only.
			StartGroupAddress (str): The first IPv4 or IPv6 Multicast group address in the range of group addresses included in this Register message.
			StartSourceAddress (str): The first IPv4 or IPv6 source address to be included in this Register message.(IPv4 Multicast addresses are not valid for sources.).
			SupportLeafAdRoutesSending (bool): If true, helps IXIA to send Leaf A-D Route on receiving a S-PMSI A-D Route with the Leaf Information Required flag set. If false, IXIA shall not send the Leaf A-D Route even if such Update message is received.

		Returns:
			self: This instance with matching multicastReceiverSite data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastReceiverSite data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastReceiverSite data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
