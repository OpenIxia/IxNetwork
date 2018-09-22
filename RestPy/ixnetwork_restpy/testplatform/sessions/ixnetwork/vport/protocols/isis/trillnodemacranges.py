from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrillNodeMacRanges(Base):
	"""The TrillNodeMacRanges class encapsulates a user managed trillNodeMacRanges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillNodeMacRanges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trillNodeMacRanges'

	def __init__(self, parent):
		super(TrillNodeMacRanges, self).__init__(parent)

	@property
	def Count(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def EnableMacRanges(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableMacRanges')
	@EnableMacRanges.setter
	def EnableMacRanges(self, value):
		self._set_attribute('enableMacRanges', value)

	@property
	def InterNodeMacStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('interNodeMacStep')
	@InterNodeMacStep.setter
	def InterNodeMacStep(self, value):
		self._set_attribute('interNodeMacStep', value)

	@property
	def StartUnicastMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startUnicastMac')
	@StartUnicastMac.setter
	def StartUnicastMac(self, value):
		self._set_attribute('startUnicastMac', value)

	@property
	def TopologyId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('topologyId')

	@property
	def UnicastMacStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('unicastMacStep')
	@UnicastMacStep.setter
	def UnicastMacStep(self, value):
		self._set_attribute('unicastMacStep', value)

	@property
	def VlanId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	def add(self, Count=None, EnableMacRanges=None, InterNodeMacStep=None, StartUnicastMac=None, UnicastMacStep=None, VlanId=None):
		"""Adds a new trillNodeMacRanges node on the server and retrieves it in this instance.

		Args:
			Count (number): NOT DEFINED
			EnableMacRanges (bool): NOT DEFINED
			InterNodeMacStep (str): NOT DEFINED
			StartUnicastMac (str): NOT DEFINED
			UnicastMacStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved trillNodeMacRanges data using find and the newly added trillNodeMacRanges data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trillNodeMacRanges data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, EnableMacRanges=None, InterNodeMacStep=None, StartUnicastMac=None, TopologyId=None, UnicastMacStep=None, VlanId=None):
		"""Finds and retrieves trillNodeMacRanges data from the server.

		All named parameters support regex and can be used to selectively retrieve trillNodeMacRanges data from the server.
		By default the find method takes no parameters and will retrieve all trillNodeMacRanges data from the server.

		Args:
			Count (number): NOT DEFINED
			EnableMacRanges (bool): NOT DEFINED
			InterNodeMacStep (str): NOT DEFINED
			StartUnicastMac (str): NOT DEFINED
			TopologyId (number): NOT DEFINED
			UnicastMacStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with matching trillNodeMacRanges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trillNodeMacRanges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trillNodeMacRanges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
