from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EvpnEthernetAd(Base):
	"""The EvpnEthernetAd class encapsulates a system managed evpnEthernetAd node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EvpnEthernetAd property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'evpnEthernetAd'

	def __init__(self, parent):
		super(EvpnEthernetAd, self).__init__(parent)

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
		"""(Read Only) Ethernet Segment ID.

		Returns:
			str
		"""
		return self._get_attribute('esi')

	@property
	def Neighbor(self):
		"""(Read Only) Neighbor IP.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	def find(self, Esi=None, Neighbor=None):
		"""Finds and retrieves evpnEthernetAd data from the server.

		All named parameters support regex and can be used to selectively retrieve evpnEthernetAd data from the server.
		By default the find method takes no parameters and will retrieve all evpnEthernetAd data from the server.

		Args:
			Esi (str): (Read Only) Ethernet Segment ID.
			Neighbor (str): (Read Only) Neighbor IP.

		Returns:
			self: This instance with matching evpnEthernetAd data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evpnEthernetAd data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evpnEthernetAd data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
