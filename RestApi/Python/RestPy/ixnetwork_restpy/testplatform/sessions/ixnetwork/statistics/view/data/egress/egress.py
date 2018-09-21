from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Egress(Base):
	"""The Egress class encapsulates a system managed egress node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Egress property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'egress'

	def __init__(self, parent):
		super(Egress, self).__init__(parent)

	@property
	def FlowCondition(self):
		"""An instance of the FlowCondition class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition.FlowCondition)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition import FlowCondition
		return FlowCondition(self)

	@property
	def CommitEgressPage(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('commitEgressPage')
	@CommitEgressPage.setter
	def CommitEgressPage(self, value):
		self._set_attribute('commitEgressPage', value)

	@property
	def CurrentPage(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentPage')
	@CurrentPage.setter
	def CurrentPage(self, value):
		self._set_attribute('currentPage', value)

	@property
	def RowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def TotalPages(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalPages')

	def find(self, CommitEgressPage=None, CurrentPage=None, RowCount=None, TotalPages=None):
		"""Finds and retrieves egress data from the server.

		All named parameters support regex and can be used to selectively retrieve egress data from the server.
		By default the find method takes no parameters and will retrieve all egress data from the server.

		Args:
			CommitEgressPage (bool): 
			CurrentPage (number): 
			RowCount (number): 
			TotalPages (number): 

		Returns:
			self: This instance with matching egress data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of egress data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the egress data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
