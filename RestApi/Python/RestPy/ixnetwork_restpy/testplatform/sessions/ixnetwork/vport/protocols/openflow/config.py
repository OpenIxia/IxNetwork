from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Config(Base):
	"""The Config class encapsulates a required config node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Config property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'config'

	def __init__(self, parent):
		super(Config, self).__init__(parent)

	@property
	def NoFlood(self):
		"""Indicates that the port is not included when flooding.

		Returns:
			bool
		"""
		return self._get_attribute('noFlood')
	@NoFlood.setter
	def NoFlood(self, value):
		self._set_attribute('noFlood', value)

	@property
	def NoForward(self):
		"""Indicates that the port drop all packets forwarded to it.

		Returns:
			bool
		"""
		return self._get_attribute('noForward')
	@NoForward.setter
	def NoForward(self, value):
		self._set_attribute('noForward', value)

	@property
	def NoPacketIn(self):
		"""Indicates that the port does not send packet-in messages.

		Returns:
			bool
		"""
		return self._get_attribute('noPacketIn')
	@NoPacketIn.setter
	def NoPacketIn(self, value):
		self._set_attribute('noPacketIn', value)

	@property
	def NoReceive(self):
		"""Indicates that the port drops all packets except 802.1D spanning tree packets.

		Returns:
			bool
		"""
		return self._get_attribute('noReceive')
	@NoReceive.setter
	def NoReceive(self, value):
		self._set_attribute('noReceive', value)

	@property
	def NoReceiveStp(self):
		"""Indicates that the port drops received 802.1D STP packets.

		Returns:
			bool
		"""
		return self._get_attribute('noReceiveStp')
	@NoReceiveStp.setter
	def NoReceiveStp(self, value):
		self._set_attribute('noReceiveStp', value)

	@property
	def NoStp(self):
		"""Indicates that 802.1D spanning tree on port is disable.

		Returns:
			bool
		"""
		return self._get_attribute('noStp')
	@NoStp.setter
	def NoStp(self, value):
		self._set_attribute('noStp', value)

	@property
	def PortDown(self):
		"""Indicates that the port is administratively down.

		Returns:
			bool
		"""
		return self._get_attribute('portDown')
	@PortDown.setter
	def PortDown(self, value):
		self._set_attribute('portDown', value)
