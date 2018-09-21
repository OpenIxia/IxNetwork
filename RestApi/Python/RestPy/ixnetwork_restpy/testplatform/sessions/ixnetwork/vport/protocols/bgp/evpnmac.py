from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EvpnMac(Base):
	"""The EvpnMac class encapsulates a system managed evpnMac node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EvpnMac property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'evpnMac'

	def __init__(self, parent):
		super(EvpnMac, self).__init__(parent)

	@property
	def NextHopInfo(self):
		"""An instance of the NextHopInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.nexthopinfo.NextHopInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.nexthopinfo import NextHopInfo
		return NextHopInfo(self)

	@property
	def Esi(self):
		"""(Read Only) Ethernet Segment Identifier.

		Returns:
			str
		"""
		return self._get_attribute('esi')

	@property
	def MacAddress(self):
		"""(Read Only) The C-MAC or the B-MAC address learned.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')

	@property
	def MacPrefixLen(self):
		"""(Read Only) Prefix length of the learned C-MAC or B-MAC.

		Returns:
			str
		"""
		return self._get_attribute('macPrefixLen')

	@property
	def Neighbor(self):
		"""(Read Only) The neighbor IP.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	def find(self, Esi=None, MacAddress=None, MacPrefixLen=None, Neighbor=None):
		"""Finds and retrieves evpnMac data from the server.

		All named parameters support regex and can be used to selectively retrieve evpnMac data from the server.
		By default the find method takes no parameters and will retrieve all evpnMac data from the server.

		Args:
			Esi (str): (Read Only) Ethernet Segment Identifier.
			MacAddress (str): (Read Only) The C-MAC or the B-MAC address learned.
			MacPrefixLen (str): (Read Only) Prefix length of the learned C-MAC or B-MAC.
			Neighbor (str): (Read Only) The neighbor IP.

		Returns:
			self: This instance with matching evpnMac data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evpnMac data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evpnMac data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
