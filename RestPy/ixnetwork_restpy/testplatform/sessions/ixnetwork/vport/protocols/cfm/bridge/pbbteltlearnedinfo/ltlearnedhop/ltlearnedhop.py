from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LtLearnedHop(Base):
	"""The LtLearnedHop class encapsulates a system managed ltLearnedHop node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LtLearnedHop property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ltLearnedHop'

	def __init__(self, parent):
		super(LtLearnedHop, self).__init__(parent)

	@property
	def EgressMac(self):
		"""(read only) The link trace message egress MAC address.

		Returns:
			str
		"""
		return self._get_attribute('egressMac')

	@property
	def IngressMac(self):
		"""(read only) The link trace message ingress MAC address.

		Returns:
			str
		"""
		return self._get_attribute('ingressMac')

	@property
	def ReplyTtl(self):
		"""(read only) The time-to-live value of the link trace hop information, in milliseconds.

		Returns:
			number
		"""
		return self._get_attribute('replyTtl')

	@property
	def Self(self):
		"""(read only) If true, the next hop is the origin of the message.

		Returns:
			bool
		"""
		return self._get_attribute('self')

	def find(self, EgressMac=None, IngressMac=None, ReplyTtl=None, Self=None):
		"""Finds and retrieves ltLearnedHop data from the server.

		All named parameters support regex and can be used to selectively retrieve ltLearnedHop data from the server.
		By default the find method takes no parameters and will retrieve all ltLearnedHop data from the server.

		Args:
			EgressMac (str): (read only) The link trace message egress MAC address.
			IngressMac (str): (read only) The link trace message ingress MAC address.
			ReplyTtl (number): (read only) The time-to-live value of the link trace hop information, in milliseconds.
			Self (bool): (read only) If true, the next hop is the origin of the message.

		Returns:
			self: This instance with matching ltLearnedHop data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ltLearnedHop data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ltLearnedHop data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
