from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyMulticastMacRange(Base):
	"""The CustomTopologyMulticastMacRange class encapsulates a user managed customTopologyMulticastMacRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyMulticastMacRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyMulticastMacRange'

	def __init__(self, parent):
		super(CustomTopologyMulticastMacRange, self).__init__(parent)

	@property
	def IncludeMacGroup(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeMacGroup')
	@IncludeMacGroup.setter
	def IncludeMacGroup(self, value):
		self._set_attribute('includeMacGroup', value)

	@property
	def IntraGroupUnicastMacIncrement(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastMacIncrement')
	@IntraGroupUnicastMacIncrement.setter
	def IntraGroupUnicastMacIncrement(self, value):
		self._set_attribute('intraGroupUnicastMacIncrement', value)

	@property
	def MulticastAddressNodeStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('multicastAddressNodeStep')
	@MulticastAddressNodeStep.setter
	def MulticastAddressNodeStep(self, value):
		self._set_attribute('multicastAddressNodeStep', value)

	@property
	def MulticastMacCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('multicastMacCount')
	@MulticastMacCount.setter
	def MulticastMacCount(self, value):
		self._set_attribute('multicastMacCount', value)

	@property
	def MulticastMacStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('multicastMacStep')
	@MulticastMacStep.setter
	def MulticastMacStep(self, value):
		self._set_attribute('multicastMacStep', value)

	@property
	def NumberOfUnicastSourceMacsPerMulticast(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numberOfUnicastSourceMacsPerMulticast')
	@NumberOfUnicastSourceMacsPerMulticast.setter
	def NumberOfUnicastSourceMacsPerMulticast(self, value):
		self._set_attribute('numberOfUnicastSourceMacsPerMulticast', value)

	@property
	def SourceGroupMapping(self):
		"""NOT DEFINED

		Returns:
			str(fully-Meshed|one-To-One|manual-Mapping)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def StartMulticastMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startMulticastMac')
	@StartMulticastMac.setter
	def StartMulticastMac(self, value):
		self._set_attribute('startMulticastMac', value)

	@property
	def StartUnicastSourceMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceMac')
	@StartUnicastSourceMac.setter
	def StartUnicastSourceMac(self, value):
		self._set_attribute('startUnicastSourceMac', value)

	@property
	def UnicastAddressNodeStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('unicastAddressNodeStep')
	@UnicastAddressNodeStep.setter
	def UnicastAddressNodeStep(self, value):
		self._set_attribute('unicastAddressNodeStep', value)

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

	def add(self, IncludeMacGroup=None, IntraGroupUnicastMacIncrement=None, MulticastAddressNodeStep=None, MulticastMacCount=None, MulticastMacStep=None, NumberOfUnicastSourceMacsPerMulticast=None, SourceGroupMapping=None, StartMulticastMac=None, StartUnicastSourceMac=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Adds a new customTopologyMulticastMacRange node on the server and retrieves it in this instance.

		Args:
			IncludeMacGroup (bool): NOT DEFINED
			IntraGroupUnicastMacIncrement (str): NOT DEFINED
			MulticastAddressNodeStep (str): NOT DEFINED
			MulticastMacCount (number): NOT DEFINED
			MulticastMacStep (str): NOT DEFINED
			NumberOfUnicastSourceMacsPerMulticast (number): NOT DEFINED
			SourceGroupMapping (str(fully-Meshed|one-To-One|manual-Mapping)): NOT DEFINED
			StartMulticastMac (str): NOT DEFINED
			StartUnicastSourceMac (str): NOT DEFINED
			UnicastAddressNodeStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyMulticastMacRange data using find and the newly added customTopologyMulticastMacRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyMulticastMacRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeMacGroup=None, IntraGroupUnicastMacIncrement=None, MulticastAddressNodeStep=None, MulticastMacCount=None, MulticastMacStep=None, NumberOfUnicastSourceMacsPerMulticast=None, SourceGroupMapping=None, StartMulticastMac=None, StartUnicastSourceMac=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Finds and retrieves customTopologyMulticastMacRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyMulticastMacRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyMulticastMacRange data from the server.

		Args:
			IncludeMacGroup (bool): NOT DEFINED
			IntraGroupUnicastMacIncrement (str): NOT DEFINED
			MulticastAddressNodeStep (str): NOT DEFINED
			MulticastMacCount (number): NOT DEFINED
			MulticastMacStep (str): NOT DEFINED
			NumberOfUnicastSourceMacsPerMulticast (number): NOT DEFINED
			SourceGroupMapping (str(fully-Meshed|one-To-One|manual-Mapping)): NOT DEFINED
			StartMulticastMac (str): NOT DEFINED
			StartUnicastSourceMac (str): NOT DEFINED
			UnicastAddressNodeStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyMulticastMacRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyMulticastMacRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyMulticastMacRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
