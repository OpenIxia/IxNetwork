from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pattern(Base):
	"""The Pattern class encapsulates a user managed pattern node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pattern property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'pattern'

	def __init__(self, parent):
		super(Pattern, self).__init__(parent)

	@property
	def FlowLabel(self):
		"""This corresponds to the name or the label given to each flow.

		Returns:
			str
		"""
		return self._get_attribute('flowLabel')
	@FlowLabel.setter
	def FlowLabel(self, value):
		self._set_attribute('flowLabel', value)

	@property
	def RowCount(self):
		"""Displays the a particular row number in the view.

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	def add(self, FlowLabel=None):
		"""Adds a new pattern node on the server and retrieves it in this instance.

		Args:
			FlowLabel (str): This corresponds to the name or the label given to each flow.

		Returns:
			self: This instance with all currently retrieved pattern data using find and the newly added pattern data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the pattern data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, FlowLabel=None, RowCount=None):
		"""Finds and retrieves pattern data from the server.

		All named parameters support regex and can be used to selectively retrieve pattern data from the server.
		By default the find method takes no parameters and will retrieve all pattern data from the server.

		Args:
			FlowLabel (str): This corresponds to the name or the label given to each flow.
			RowCount (number): Displays the a particular row number in the view.

		Returns:
			self: This instance with matching pattern data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pattern data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pattern data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
