from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dhcpv6client(Base):
	"""The Dhcpv6client class encapsulates a required dhcpv6client node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcpv6client property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpv6client'

	def __init__(self, parent):
		super(Dhcpv6client, self).__init__(parent)

	@property
	def SessionLifetime(self):
		"""An instance of the SessionLifetime class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.sessionlifetime.sessionlifetime.SessionLifetime)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.sessionlifetime.sessionlifetime import SessionLifetime
		return SessionLifetime(self)._select()

	@property
	def StartRate(self):
		"""An instance of the StartRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.startrate.startrate.StartRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.startrate.startrate import StartRate
		return StartRate(self)._select()

	@property
	def StopRate(self):
		"""An instance of the StopRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.stoprate.stoprate.StopRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.stoprate.stoprate import StopRate
		return StopRate(self)._select()

	@property
	def TlvEditor(self):
		"""An instance of the TlvEditor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor.TlvEditor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlveditor import TlvEditor
		return TlvEditor(self)

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
	def Dhcp6EchoIAInfo(self):
		"""If set, the DHCPv6 client will request the exact address as advertised by server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6EchoIAInfo')

	@property
	def Dhcp6InfoReqMaxRc(self):
		"""RFC 3315 Info Request Attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6InfoReqMaxRc')

	@property
	def Dhcp6InfoReqMaxRt(self):
		"""RFC 3315 Max Information-request timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6InfoReqMaxRt')

	@property
	def Dhcp6InfoReqTimeout(self):
		"""RFC 3315 Initial Information-request timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6InfoReqTimeout')

	@property
	def Dhcp6NsGw(self):
		"""If enabled, DHCP clients NS to find their Gateway MAC Addresses.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6NsGw')

	@property
	def Dhcp6RebMaxRt(self):
		"""RFC 3315 Max Rebind timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RebMaxRt')

	@property
	def Dhcp6RebTimeout(self):
		"""RFC 3315 Initial Rebind timeout seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RebTimeout')

	@property
	def Dhcp6RelMaxRc(self):
		"""RFC 3315 Release attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RelMaxRc')

	@property
	def Dhcp6RelTimeout(self):
		"""RFC 3315 Initial Release timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RelTimeout')

	@property
	def Dhcp6RenMaxRt(self):
		"""RFC 3315 Max Renew timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RenMaxRt')

	@property
	def Dhcp6RenTimeout(self):
		"""RFC 3315 Initial Renew timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6RenTimeout')

	@property
	def Dhcp6ReqMaxRc(self):
		"""RFC 3315 Max Request retry attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6ReqMaxRc')

	@property
	def Dhcp6ReqMaxRt(self):
		"""RFC 3315 Max Request timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6ReqMaxRt')

	@property
	def Dhcp6ReqTimeout(self):
		"""RFC 3315 Initial Request timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6ReqTimeout')

	@property
	def Dhcp6SolMaxRc(self):
		"""RFC 3315 Max Solicit retry attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6SolMaxRc')

	@property
	def Dhcp6SolMaxRt(self):
		"""RFC 3315 Max Solicit timeout value in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6SolMaxRt')

	@property
	def Dhcp6SolTimeout(self):
		"""RFC 3315 Initial Solicit timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dhcp6SolTimeout')

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
	def RenewOnLinkUp(self):
		"""Indicate to renew the active DHCP sessions after link status goes down and up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('renewOnLinkUp')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def SkipReleaseOnStop(self):
		"""If enabled, the client does not send a DHCPRELEASE packet when the Stop command is given.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('skipReleaseOnStop')
