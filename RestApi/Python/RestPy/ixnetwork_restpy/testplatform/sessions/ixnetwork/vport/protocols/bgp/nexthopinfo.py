from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NextHopInfo(Base):
	"""The NextHopInfo class encapsulates a system managed nextHopInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NextHopInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'nextHopInfo'

	def __init__(self, parent):
		super(NextHopInfo, self).__init__(parent)

	@property
	def RdInfo(self):
		"""An instance of the RdInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.rdinfo.RdInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.rdinfo import RdInfo
		return RdInfo(self)

	@property
	def NextHop(self):
		"""(Read Only) Next Hop IP.

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	def find(self, NextHop=None):
		"""Finds and retrieves nextHopInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve nextHopInfo data from the server.
		By default the find method takes no parameters and will retrieve all nextHopInfo data from the server.

		Args:
			NextHop (str): (Read Only) Next Hop IP.

		Returns:
			self: This instance with matching nextHopInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of nextHopInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the nextHopInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
