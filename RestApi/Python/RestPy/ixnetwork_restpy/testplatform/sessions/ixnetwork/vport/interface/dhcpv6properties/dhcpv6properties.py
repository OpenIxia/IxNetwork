from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DhcpV6Properties(Base):
	"""The DhcpV6Properties class encapsulates a required dhcpV6Properties node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV6Properties property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV6Properties'

	def __init__(self, parent):
		super(DhcpV6Properties, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables the DHCPv6 client feature. DHCPv6 negotiation will be started and an IPv6 address learned from the DHCPv6 server will be assigned automatically to the protocol interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IaId(self):
		"""The unique identifier value for the Identity Association (IA).

		Returns:
			number
		"""
		return self._get_attribute('iaId')
	@IaId.setter
	def IaId(self, value):
		self._set_attribute('iaId', value)

	@property
	def IaType(self):
		"""The Identity Association (IA) Type.

		Returns:
			str(permanent|temporary|prefixDelegation)
		"""
		return self._get_attribute('iaType')
	@IaType.setter
	def IaType(self, value):
		self._set_attribute('iaType', value)

	@property
	def RenewTimer(self):
		"""The user-specified value and the lease timer (from the DHCP Server) are compared. The lowest value is used as the release/renew timer. After this time period has elapsed, the address will be renewed.

		Returns:
			number
		"""
		return self._get_attribute('renewTimer')
	@RenewTimer.setter
	def RenewTimer(self, value):
		self._set_attribute('renewTimer', value)

	@property
	def RequestRate(self):
		"""The user-specified maximum number of Request messages that can be sent per second from the client to the DHCPv6 server, requesting an IPv6 address. A value of zero (0) indicates that there will be no rate control, that is, requests will be sent as quickly as possible.

		Returns:
			number
		"""
		return self._get_attribute('requestRate')
	@RequestRate.setter
	def RequestRate(self, value):
		self._set_attribute('requestRate', value)

	@property
	def Tlvs(self):
		"""DHCP TLVs (type length value) for custom DHCP options.

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlvs')
	@Tlvs.setter
	def Tlvs(self, value):
		self._set_attribute('tlvs', value)
