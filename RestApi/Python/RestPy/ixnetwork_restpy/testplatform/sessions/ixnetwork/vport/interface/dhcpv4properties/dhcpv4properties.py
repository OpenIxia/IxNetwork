from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DhcpV4Properties(Base):
	"""The DhcpV4Properties class encapsulates a required dhcpV4Properties node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV4Properties property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV4Properties'

	def __init__(self, parent):
		super(DhcpV4Properties, self).__init__(parent)

	@property
	def ClientId(self):
		"""The user may optionally assign an identifier for the Client. This value must be unique on the subnet where the DHCP Client is located.

		Returns:
			str
		"""
		return self._get_attribute('clientId')
	@ClientId.setter
	def ClientId(self, value):
		self._set_attribute('clientId', value)

	@property
	def Enabled(self):
		"""If enabled, DHCP negotiation will be started and an IPv4 address learned from the DHCP server will be assigned automatically to the protocol interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RenewTimer(self):
		"""The renew timer value specified by the DHCPv4 server.

		Returns:
			number
		"""
		return self._get_attribute('renewTimer')
	@RenewTimer.setter
	def RenewTimer(self, value):
		self._set_attribute('renewTimer', value)

	@property
	def RequestRate(self):
		"""(For rate control) The user-specified maximum number of Request messages that can be sent per second from the client to the DHCP server, requesting an IPv4 address. A value of zero (0) indicates that there will be no rate control, i.e., Requests will be sent as quickly as possible.

		Returns:
			number
		"""
		return self._get_attribute('requestRate')
	@RequestRate.setter
	def RequestRate(self, value):
		self._set_attribute('requestRate', value)

	@property
	def ServerId(self):
		"""This IPv4 address value is used to identify the DHCP Server and as a destination address from the client.

		Returns:
			str
		"""
		return self._get_attribute('serverId')
	@ServerId.setter
	def ServerId(self, value):
		self._set_attribute('serverId', value)

	@property
	def Tlvs(self):
		"""The type length value for DHCP.

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlvs')
	@Tlvs.setter
	def Tlvs(self, value):
		self._set_attribute('tlvs', value)

	@property
	def VendorId(self):
		"""The optional, user-assigned Vendor ID (vendor class identifier).

		Returns:
			str
		"""
		return self._get_attribute('vendorId')
	@VendorId.setter
	def VendorId(self, value):
		self._set_attribute('vendorId', value)
