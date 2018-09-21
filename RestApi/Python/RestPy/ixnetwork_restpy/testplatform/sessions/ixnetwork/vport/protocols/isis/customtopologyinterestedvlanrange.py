from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyInterestedVlanRange(Base):
	"""The CustomTopologyInterestedVlanRange class encapsulates a user managed customTopologyInterestedVlanRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyInterestedVlanRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyInterestedVlanRange'

	def __init__(self, parent):
		super(CustomTopologyInterestedVlanRange, self).__init__(parent)

	@property
	def IncludeInterestedVlan(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInterestedVlan')
	@IncludeInterestedVlan.setter
	def IncludeInterestedVlan(self, value):
		self._set_attribute('includeInterestedVlan', value)

	@property
	def InterNodeVlanStep(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('interNodeVlanStep')
	@InterNodeVlanStep.setter
	def InterNodeVlanStep(self, value):
		self._set_attribute('interNodeVlanStep', value)

	@property
	def M4BitEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('m4BitEnabled')
	@M4BitEnabled.setter
	def M4BitEnabled(self, value):
		self._set_attribute('m4BitEnabled', value)

	@property
	def M6BitEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('m6BitEnabled')
	@M6BitEnabled.setter
	def M6BitEnabled(self, value):
		self._set_attribute('m6BitEnabled', value)

	@property
	def NumberOfSpanningTreeRoots(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numberOfSpanningTreeRoots')
	@NumberOfSpanningTreeRoots.setter
	def NumberOfSpanningTreeRoots(self, value):
		self._set_attribute('numberOfSpanningTreeRoots', value)

	@property
	def StartSpanningTreeRootBridgeId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startSpanningTreeRootBridgeId')
	@StartSpanningTreeRootBridgeId.setter
	def StartSpanningTreeRootBridgeId(self, value):
		self._set_attribute('startSpanningTreeRootBridgeId', value)

	@property
	def StartVlanId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('startVlanId')
	@StartVlanId.setter
	def StartVlanId(self, value):
		self._set_attribute('startVlanId', value)

	@property
	def VlanCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanIdStep(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanIdStep')
	@VlanIdStep.setter
	def VlanIdStep(self, value):
		self._set_attribute('vlanIdStep', value)

	def add(self, IncludeInterestedVlan=None, InterNodeVlanStep=None, M4BitEnabled=None, M6BitEnabled=None, NumberOfSpanningTreeRoots=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanCount=None, VlanIdStep=None):
		"""Adds a new customTopologyInterestedVlanRange node on the server and retrieves it in this instance.

		Args:
			IncludeInterestedVlan (bool): NOT DEFINED
			InterNodeVlanStep (number): NOT DEFINED
			M4BitEnabled (bool): NOT DEFINED
			M6BitEnabled (bool): NOT DEFINED
			NumberOfSpanningTreeRoots (number): NOT DEFINED
			StartSpanningTreeRootBridgeId (str): NOT DEFINED
			StartVlanId (number): NOT DEFINED
			VlanCount (number): NOT DEFINED
			VlanIdStep (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyInterestedVlanRange data using find and the newly added customTopologyInterestedVlanRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyInterestedVlanRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeInterestedVlan=None, InterNodeVlanStep=None, M4BitEnabled=None, M6BitEnabled=None, NumberOfSpanningTreeRoots=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanCount=None, VlanIdStep=None):
		"""Finds and retrieves customTopologyInterestedVlanRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyInterestedVlanRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyInterestedVlanRange data from the server.

		Args:
			IncludeInterestedVlan (bool): NOT DEFINED
			InterNodeVlanStep (number): NOT DEFINED
			M4BitEnabled (bool): NOT DEFINED
			M6BitEnabled (bool): NOT DEFINED
			NumberOfSpanningTreeRoots (number): NOT DEFINED
			StartSpanningTreeRootBridgeId (str): NOT DEFINED
			StartVlanId (number): NOT DEFINED
			VlanCount (number): NOT DEFINED
			VlanIdStep (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyInterestedVlanRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyInterestedVlanRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyInterestedVlanRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
