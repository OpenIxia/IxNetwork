from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SupportedActions(Base):
	"""The SupportedActions class encapsulates a required supportedActions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SupportedActions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'supportedActions'

	def __init__(self, parent):
		super(SupportedActions, self).__init__(parent)

	@property
	def Enqueue(self):
		"""Indicates that the supported action of the switch includes Output to queue.

		Returns:
			bool
		"""
		return self._get_attribute('enqueue')
	@Enqueue.setter
	def Enqueue(self, value):
		self._set_attribute('enqueue', value)

	@property
	def EthernetDestination(self):
		"""Indicates that the supported action of the switch includes setting Ethernet destination address.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""Indicates that the supported action of the switch includes setting Ethernet source address.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def IpDscp(self):
		"""Indicates that the supported action of the switch includes setting IP ToS, DSCP field, 6 bits.

		Returns:
			bool
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def Ipv4Destination(self):
		"""Indicates that the supported action of the switch includes setting IP destination address.

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""Indicates that the supported action of the switch includes setting IP source address.

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Output(self):
		"""Indicates that the supported action of the switch includes Output to switch port.

		Returns:
			bool
		"""
		return self._get_attribute('output')
	@Output.setter
	def Output(self, value):
		self._set_attribute('output', value)

	@property
	def StripVlanHeader(self):
		"""Indicates that the supported action of the switch includes stripping the 802.1q header.

		Returns:
			bool
		"""
		return self._get_attribute('stripVlanHeader')
	@StripVlanHeader.setter
	def StripVlanHeader(self, value):
		self._set_attribute('stripVlanHeader', value)

	@property
	def TransportDestination(self):
		"""Indicates that the supported action of the switch includes setting TCP/UDP destination port.

		Returns:
			bool
		"""
		return self._get_attribute('transportDestination')
	@TransportDestination.setter
	def TransportDestination(self, value):
		self._set_attribute('transportDestination', value)

	@property
	def TransportSource(self):
		"""Indicates that the supported action of the switch includes setting TCP/UDP source port.

		Returns:
			bool
		"""
		return self._get_attribute('transportSource')
	@TransportSource.setter
	def TransportSource(self, value):
		self._set_attribute('transportSource', value)

	@property
	def VlanId(self):
		"""Indicates that the supported action of the switch includes setting the 802.1q VLAN id.

		Returns:
			bool
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Indicates that the supported action of the switch includes setting the 802.1q priority.

		Returns:
			bool
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
