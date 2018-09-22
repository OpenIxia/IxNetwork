from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Nssa(Base):
	"""The Nssa class encapsulates a system managed nssa node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Nssa property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'nssa'

	def __init__(self, parent):
		super(Nssa, self).__init__(parent)

	@property
	def EBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('eBit')
	@EBit.setter
	def EBit(self, value):
		self._set_attribute('eBit', value)

	@property
	def ForwardingAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('forwardingAddress')
	@ForwardingAddress.setter
	def ForwardingAddress(self, value):
		self._set_attribute('forwardingAddress', value)

	@property
	def IncrementLinkStateIdBy(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incrementLinkStateIdBy')
	@IncrementLinkStateIdBy.setter
	def IncrementLinkStateIdBy(self, value):
		self._set_attribute('incrementLinkStateIdBy', value)

	@property
	def Metric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NetworkMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkMask')
	@NetworkMask.setter
	def NetworkMask(self, value):
		self._set_attribute('networkMask', value)

	@property
	def NumberOfLsa(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfLsa')
	@NumberOfLsa.setter
	def NumberOfLsa(self, value):
		self._set_attribute('numberOfLsa', value)

	@property
	def RouteTag(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	def find(self, EBit=None, ForwardingAddress=None, IncrementLinkStateIdBy=None, Metric=None, NetworkMask=None, NumberOfLsa=None, RouteTag=None):
		"""Finds and retrieves nssa data from the server.

		All named parameters support regex and can be used to selectively retrieve nssa data from the server.
		By default the find method takes no parameters and will retrieve all nssa data from the server.

		Args:
			EBit (bool): 
			ForwardingAddress (str): 
			IncrementLinkStateIdBy (str): 
			Metric (number): 
			NetworkMask (str): 
			NumberOfLsa (number): 
			RouteTag (str): 

		Returns:
			self: This instance with matching nssa data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of nssa data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the nssa data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
