from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RdInfo(Base):
	"""The RdInfo class encapsulates a system managed rdInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RdInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rdInfo'

	def __init__(self, parent):
		super(RdInfo, self).__init__(parent)

	@property
	def EthernetTagInfo(self):
		"""An instance of the EthernetTagInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ethernettaginfo.EthernetTagInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ethernettaginfo import EthernetTagInfo
		return EthernetTagInfo(self)

	@property
	def Rd(self):
		"""RD value in X:Y format.

		Returns:
			str
		"""
		return self._get_attribute('rd')

	def find(self, Rd=None):
		"""Finds and retrieves rdInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve rdInfo data from the server.
		By default the find method takes no parameters and will retrieve all rdInfo data from the server.

		Args:
			Rd (str): RD value in X:Y format.

		Returns:
			self: This instance with matching rdInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rdInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rdInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
