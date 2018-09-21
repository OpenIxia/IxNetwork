from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DhcpV6DiscoveredInfo(Base):
	"""The DhcpV6DiscoveredInfo class encapsulates a required dhcpV6DiscoveredInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV6DiscoveredInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV6DiscoveredInfo'

	def __init__(self, parent):
		super(DhcpV6DiscoveredInfo, self).__init__(parent)

	@property
	def IaRebindTime(self):
		"""(Read Only) The rebind timer value (in seconds) specified by the DHCPv6 Server.

		Returns:
			number
		"""
		return self._get_attribute('iaRebindTime')

	@property
	def IaRenewTime(self):
		"""(Read Only) The renew timer value (in seconds) specified by the DHCPv6 Server.

		Returns:
			number
		"""
		return self._get_attribute('iaRenewTime')

	@property
	def Ipv6Address(self):
		"""(Read Only) A learned/allocated IPv6 address for this interface.

		Returns:
			list(str)
		"""
		return self._get_attribute('ipv6Address')

	@property
	def IsDhcpV6LearnedInfoRefreshed(self):
		"""(Read Only) When true, the DHCPv6 discovered information is refreshed automatically.

		Returns:
			bool
		"""
		return self._get_attribute('isDhcpV6LearnedInfoRefreshed')

	@property
	def ProtocolInterface(self):
		"""(Read Only) An Ixia protocol interface that is negotiating with the DHCPv6 Server.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')

	@property
	def Tlvs(self):
		"""(Read Only) The identifier or 'tag' for this DHCPv6 option. The DHCPv6 option value field may contain data for configuration parameter information.

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlvs')
