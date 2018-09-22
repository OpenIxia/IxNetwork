from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EthernetTrafficEndPoint(Base):
	"""The EthernetTrafficEndPoint class encapsulates a user managed ethernetTrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetTrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ethernetTrafficEndPoint'

	def __init__(self, parent):
		super(EthernetTrafficEndPoint, self).__init__(parent)

	@property
	def ArpViaInterface(self):
		"""If selected, ARP request is conveyed through an Interface.

		Returns:
			bool
		"""
		return self._get_attribute('arpViaInterface')
	@ArpViaInterface.setter
	def ArpViaInterface(self, value):
		self._set_attribute('arpViaInterface', value)

	@property
	def CustomEtherHeaderLength(self):
		"""Specify the Custom Header length in bytes. The default length is 46 bytes.

		Returns:
			number
		"""
		return self._get_attribute('customEtherHeaderLength')
	@CustomEtherHeaderLength.setter
	def CustomEtherHeaderLength(self, value):
		self._set_attribute('customEtherHeaderLength', value)

	@property
	def CustomEtherHeaderValue(self):
		"""Specify the Custom Header value.

		Returns:
			str
		"""
		return self._get_attribute('customEtherHeaderValue')
	@CustomEtherHeaderValue.setter
	def CustomEtherHeaderValue(self, value):
		self._set_attribute('customEtherHeaderValue', value)

	@property
	def CustomEtherType(self):
		"""Specify the Custom Ether type.

		Returns:
			str
		"""
		return self._get_attribute('customEtherType')
	@CustomEtherType.setter
	def CustomEtherType(self, value):
		self._set_attribute('customEtherType', value)

	@property
	def EnableMacInMac(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableMacInMac')
	@EnableMacInMac.setter
	def EnableMacInMac(self, value):
		self._set_attribute('enableMacInMac', value)

	@property
	def EnableVlan(self):
		"""Select this check box to make VLAN available.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def GatewayMac(self):
		"""The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('gatewayMac')
	@GatewayMac.setter
	def GatewayMac(self, value):
		self._set_attribute('gatewayMac', value)

	@property
	def MacAddress(self):
		"""The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def Name(self):
		"""The name of the Traffic Source Endpoint.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PbbDestinamtionMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('pbbDestinamtionMac')
	@PbbDestinamtionMac.setter
	def PbbDestinamtionMac(self, value):
		self._set_attribute('pbbDestinamtionMac', value)

	@property
	def PbbEtherType(self):
		"""NOT DEFINED

		Returns:
			str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)
		"""
		return self._get_attribute('pbbEtherType')
	@PbbEtherType.setter
	def PbbEtherType(self, value):
		self._set_attribute('pbbEtherType', value)

	@property
	def PbbIsId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('pbbIsId')
	@PbbIsId.setter
	def PbbIsId(self, value):
		self._set_attribute('pbbIsId', value)

	@property
	def PbbSourceMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('pbbSourceMac')
	@PbbSourceMac.setter
	def PbbSourceMac(self, value):
		self._set_attribute('pbbSourceMac', value)

	@property
	def PbbVlanId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanId')
	@PbbVlanId.setter
	def PbbVlanId(self, value):
		self._set_attribute('pbbVlanId', value)

	@property
	def PbbVlanPcp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanPcp')
	@PbbVlanPcp.setter
	def PbbVlanPcp(self, value):
		self._set_attribute('pbbVlanPcp', value)

	@property
	def ProtocolInterface(self):
		"""NOT DEFINED

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def RangeSize(self):
		"""Specify the size of the Range.

		Returns:
			number
		"""
		return self._get_attribute('rangeSize')
	@RangeSize.setter
	def RangeSize(self, value):
		self._set_attribute('rangeSize', value)

	@property
	def VlanCount(self):
		"""Specify the VLAN count. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""Specify the VLAN ID (Outer and Inner).

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Specify the VLAN Priority (Outer and Inner).

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, EnableMacInMac=None, EnableVlan=None, GatewayMac=None, MacAddress=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new ethernetTrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			CustomEtherHeaderLength (number): Specify the Custom Header length in bytes. The default length is 46 bytes.
			CustomEtherHeaderValue (str): Specify the Custom Header value.
			CustomEtherType (str): Specify the Custom Ether type.
			EnableMacInMac (bool): NOT DEFINED
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Name (str): The name of the Traffic Source Endpoint.
			PbbDestinamtionMac (str): NOT DEFINED
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): NOT DEFINED
			PbbIsId (str): NOT DEFINED
			PbbSourceMac (str): NOT DEFINED
			PbbVlanId (str): NOT DEFINED
			PbbVlanPcp (str): NOT DEFINED
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the Range.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with all currently retrieved ethernetTrafficEndPoint data using find and the newly added ethernetTrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ethernetTrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, EnableMacInMac=None, EnableVlan=None, GatewayMac=None, MacAddress=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves ethernetTrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve ethernetTrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all ethernetTrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			CustomEtherHeaderLength (number): Specify the Custom Header length in bytes. The default length is 46 bytes.
			CustomEtherHeaderValue (str): Specify the Custom Header value.
			CustomEtherType (str): Specify the Custom Ether type.
			EnableMacInMac (bool): NOT DEFINED
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Name (str): The name of the Traffic Source Endpoint.
			PbbDestinamtionMac (str): NOT DEFINED
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): NOT DEFINED
			PbbIsId (str): NOT DEFINED
			PbbSourceMac (str): NOT DEFINED
			PbbVlanId (str): NOT DEFINED
			PbbVlanPcp (str): NOT DEFINED
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the Range.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with matching ethernetTrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ethernetTrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ethernetTrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
