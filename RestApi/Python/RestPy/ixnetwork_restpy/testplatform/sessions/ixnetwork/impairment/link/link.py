from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Link(Base):
	"""The Link class encapsulates a system managed link node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Link property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'link'

	def __init__(self, parent):
		super(Link, self).__init__(parent)

	@property
	def LosLof(self):
		"""An instance of the LosLof class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.link.loslof.loslof.LosLof)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.link.loslof.loslof import LosLof
		return LosLof(self)._select()

	@property
	def ForwardingInterruption(self):
		"""Emulate a link fault. Drop all packets received.

		Returns:
			bool
		"""
		return self._get_attribute('forwardingInterruption')
	@ForwardingInterruption.setter
	def ForwardingInterruption(self, value):
		self._set_attribute('forwardingInterruption', value)

	@property
	def Name(self):
		"""The name of the link: receiving port -> transmitting port.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def RxPortName(self):
		"""The name of the receiving port.

		Returns:
			str
		"""
		return self._get_attribute('rxPortName')

	@property
	def TxPortName(self):
		"""The name of the transmitting port.

		Returns:
			str
		"""
		return self._get_attribute('txPortName')

	def find(self, ForwardingInterruption=None, Name=None, RxPortName=None, TxPortName=None):
		"""Finds and retrieves link data from the server.

		All named parameters support regex and can be used to selectively retrieve link data from the server.
		By default the find method takes no parameters and will retrieve all link data from the server.

		Args:
			ForwardingInterruption (bool): Emulate a link fault. Drop all packets received.
			Name (str): The name of the link: receiving port -> transmitting port.
			RxPortName (str): The name of the receiving port.
			TxPortName (str): The name of the transmitting port.

		Returns:
			self: This instance with matching link data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of link data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the link data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
