from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchPortQueues(Base):
	"""The SwitchPortQueues class encapsulates a user managed switchPortQueues node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchPortQueues property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'switchPortQueues'

	def __init__(self, parent):
		super(SwitchPortQueues, self).__init__(parent)

	@property
	def QueueProperty(self):
		"""An instance of the QueueProperty class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.queueproperty.QueueProperty)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.queueproperty import QueueProperty
		return QueueProperty(self)._select()

	@property
	def MinRate(self):
		"""Indicates the minimum-rate, in 1/10 of a percent, applicable when queue property is OFPQT_MIN.

		Returns:
			str
		"""
		return self._get_attribute('minRate')
	@MinRate.setter
	def MinRate(self, value):
		self._set_attribute('minRate', value)

	@property
	def NumberOfQueues(self):
		"""Specifies the number of entries in the queue range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfQueues')
	@NumberOfQueues.setter
	def NumberOfQueues(self, value):
		self._set_attribute('numberOfQueues', value)

	@property
	def QueueId(self):
		"""Indicates the ID for the specific queue.

		Returns:
			str
		"""
		return self._get_attribute('queueId')
	@QueueId.setter
	def QueueId(self, value):
		self._set_attribute('queueId', value)

	def add(self, MinRate=None, NumberOfQueues=None, QueueId=None):
		"""Adds a new switchPortQueues node on the server and retrieves it in this instance.

		Args:
			MinRate (str): Indicates the minimum-rate, in 1/10 of a percent, applicable when queue property is OFPQT_MIN.
			NumberOfQueues (number): Specifies the number of entries in the queue range.
			QueueId (str): Indicates the ID for the specific queue.

		Returns:
			self: This instance with all currently retrieved switchPortQueues data using find and the newly added switchPortQueues data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the switchPortQueues data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, MinRate=None, NumberOfQueues=None, QueueId=None):
		"""Finds and retrieves switchPortQueues data from the server.

		All named parameters support regex and can be used to selectively retrieve switchPortQueues data from the server.
		By default the find method takes no parameters and will retrieve all switchPortQueues data from the server.

		Args:
			MinRate (str): Indicates the minimum-rate, in 1/10 of a percent, applicable when queue property is OFPQT_MIN.
			NumberOfQueues (number): Specifies the number of entries in the queue range.
			QueueId (str): Indicates the ID for the specific queue.

		Returns:
			self: This instance with matching switchPortQueues data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchPortQueues data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchPortQueues data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
