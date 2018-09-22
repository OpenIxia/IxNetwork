from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CeVlanIdRange(Base):
	"""The CeVlanIdRange class encapsulates a user managed ceVlanIdRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CeVlanIdRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ceVlanIdRange'

	def __init__(self, parent):
		super(CeVlanIdRange, self).__init__(parent)

	@property
	def Count(self):
		"""It signifies the number of Vlan Ids configured for the EVC.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Enabled(self):
		"""If enabled, CE VLAN Id range is in effect for the EVC.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncrementStep(self):
		"""It shows the Increment Step of Vlan ID. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('incrementStep')
	@IncrementStep.setter
	def IncrementStep(self, value):
		self._set_attribute('incrementStep', value)

	@property
	def StartVlanId(self):
		"""The VLAN Id of first VLAN. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('startVlanId')
	@StartVlanId.setter
	def StartVlanId(self, value):
		self._set_attribute('startVlanId', value)

	def add(self, Count=None, Enabled=None, IncrementStep=None, StartVlanId=None):
		"""Adds a new ceVlanIdRange node on the server and retrieves it in this instance.

		Args:
			Count (number): It signifies the number of Vlan Ids configured for the EVC.
			Enabled (bool): If enabled, CE VLAN Id range is in effect for the EVC.
			IncrementStep (number): It shows the Increment Step of Vlan ID. Default is 1.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.

		Returns:
			self: This instance with all currently retrieved ceVlanIdRange data using find and the newly added ceVlanIdRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ceVlanIdRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Enabled=None, IncrementStep=None, StartVlanId=None):
		"""Finds and retrieves ceVlanIdRange data from the server.

		All named parameters support regex and can be used to selectively retrieve ceVlanIdRange data from the server.
		By default the find method takes no parameters and will retrieve all ceVlanIdRange data from the server.

		Args:
			Count (number): It signifies the number of Vlan Ids configured for the EVC.
			Enabled (bool): If enabled, CE VLAN Id range is in effect for the EVC.
			IncrementStep (number): It shows the Increment Step of Vlan ID. Default is 1.
			StartVlanId (number): The VLAN Id of first VLAN. Default is 1.

		Returns:
			self: This instance with matching ceVlanIdRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ceVlanIdRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ceVlanIdRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
