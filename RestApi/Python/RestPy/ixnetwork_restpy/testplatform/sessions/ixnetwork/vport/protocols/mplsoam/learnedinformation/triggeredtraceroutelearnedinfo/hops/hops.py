from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Hops(Base):
	"""The Hops class encapsulates a system managed hops node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Hops property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'hops'

	def __init__(self, parent):
		super(Hops, self).__init__(parent)

	@property
	def ReturnCode(self):
		"""This signifies the return code to be specified in the trace route hop.

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubCode(self):
		"""This signifies the return sub-code to be specified in the trace route hop.

		Returns:
			number
		"""
		return self._get_attribute('returnSubCode')

	@property
	def SrcIp(self):
		"""This signifies the source IP address.

		Returns:
			str
		"""
		return self._get_attribute('srcIp')

	@property
	def Ttl(self):
		"""This signifies the MPLS time to live value.

		Returns:
			number
		"""
		return self._get_attribute('ttl')

	def find(self, ReturnCode=None, ReturnSubCode=None, SrcIp=None, Ttl=None):
		"""Finds and retrieves hops data from the server.

		All named parameters support regex and can be used to selectively retrieve hops data from the server.
		By default the find method takes no parameters and will retrieve all hops data from the server.

		Args:
			ReturnCode (str): This signifies the return code to be specified in the trace route hop.
			ReturnSubCode (number): This signifies the return sub-code to be specified in the trace route hop.
			SrcIp (str): This signifies the source IP address.
			Ttl (number): This signifies the MPLS time to live value.

		Returns:
			self: This instance with matching hops data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of hops data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the hops data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
