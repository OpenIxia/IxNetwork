from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dhcpv4server(Base):
	"""The Dhcpv4server class encapsulates a required dhcpv4server node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcpv4server property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpv4server'

	def __init__(self, parent):
		super(Dhcpv4server, self).__init__(parent)

	@property
	def ReconfigureRate(self):
		"""An instance of the ReconfigureRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.reconfigurerate.reconfigurerate.ReconfigureRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.reconfigurerate.reconfigurerate import ReconfigureRate
		return ReconfigureRate(self)._select()

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
	def ForceRenewFactor(self):
		"""Force Renew timeout factor

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('forceRenewFactor')

	@property
	def ForceRenewMaxRc(self):
		"""Force Renew Attempts

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('forceRenewMaxRc')

	@property
	def InitForceRenewTimeout(self):
		"""Force Renew timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initForceRenewTimeout')

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
	def OfferTimeout(self):
		"""Offer timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('offerTimeout')

	@property
	def PingCheck(self):
		"""When enabled, the DHCP Server will not assign IP addresses that areresponding to ICMP echo requests (PING) within a certain time period.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pingCheck')

	@property
	def PingTimeout(self):
		"""The number of seconds the DHCP Server will wait for anICMP Echo response before assigning the address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pingTimeout')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')
