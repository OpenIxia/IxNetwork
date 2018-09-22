from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EvpnMulticast(Base):
	"""The EvpnMulticast class encapsulates a system managed evpnMulticast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EvpnMulticast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'evpnMulticast'

	def __init__(self, parent):
		super(EvpnMulticast, self).__init__(parent)

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
	def Neighbor(self):
		"""(Read Only) Neighbr IP.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def OriginatorsIp(self):
		"""(Read Only) Learned Originator's IP.

		Returns:
			str
		"""
		return self._get_attribute('originatorsIp')

	def find(self, Neighbor=None, OriginatorsIp=None):
		"""Finds and retrieves evpnMulticast data from the server.

		All named parameters support regex and can be used to selectively retrieve evpnMulticast data from the server.
		By default the find method takes no parameters and will retrieve all evpnMulticast data from the server.

		Args:
			Neighbor (str): (Read Only) Neighbr IP.
			OriginatorsIp (str): (Read Only) Learned Originator's IP.

		Returns:
			self: This instance with matching evpnMulticast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evpnMulticast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evpnMulticast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
