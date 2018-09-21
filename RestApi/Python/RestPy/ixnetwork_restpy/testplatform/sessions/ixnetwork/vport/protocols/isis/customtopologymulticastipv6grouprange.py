from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyMulticastIpv6GroupRange(Base):
	"""The CustomTopologyMulticastIpv6GroupRange class encapsulates a user managed customTopologyMulticastIpv6GroupRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyMulticastIpv6GroupRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyMulticastIpv6GroupRange'

	def __init__(self, parent):
		super(CustomTopologyMulticastIpv6GroupRange, self).__init__(parent)

	@property
	def IncludeIpv6Groups(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv6Groups')
	@IncludeIpv6Groups.setter
	def IncludeIpv6Groups(self, value):
		self._set_attribute('includeIpv6Groups', value)

	@property
	def IntergroupUnicastIpv6Increment(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('intergroupUnicastIpv6Increment')
	@IntergroupUnicastIpv6Increment.setter
	def IntergroupUnicastIpv6Increment(self, value):
		self._set_attribute('intergroupUnicastIpv6Increment', value)

	@property
	def IntraGroupUnicastIpv6Increment(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastIpv6Increment')
	@IntraGroupUnicastIpv6Increment.setter
	def IntraGroupUnicastIpv6Increment(self, value):
		self._set_attribute('intraGroupUnicastIpv6Increment', value)

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
	def MulticastIpv6Count(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('multicastIpv6Count')
	@MulticastIpv6Count.setter
	def MulticastIpv6Count(self, value):
		self._set_attribute('multicastIpv6Count', value)

	@property
	def MulticastIpv6Step(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('multicastIpv6Step')
	@MulticastIpv6Step.setter
	def MulticastIpv6Step(self, value):
		self._set_attribute('multicastIpv6Step', value)

	@property
	def NumberOfUnicastSourceIpv6MacsPerMulticastIpv6(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numberOfUnicastSourceIpv6MacsPerMulticastIpv6')
	@NumberOfUnicastSourceIpv6MacsPerMulticastIpv6.setter
	def NumberOfUnicastSourceIpv6MacsPerMulticastIpv6(self, value):
		self._set_attribute('numberOfUnicastSourceIpv6MacsPerMulticastIpv6', value)

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
	def StartMulticastIpv6(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startMulticastIpv6')
	@StartMulticastIpv6.setter
	def StartMulticastIpv6(self, value):
		self._set_attribute('startMulticastIpv6', value)

	@property
	def StartUnicastSourceIpv6(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceIpv6')
	@StartUnicastSourceIpv6.setter
	def StartUnicastSourceIpv6(self, value):
		self._set_attribute('startUnicastSourceIpv6', value)

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

	def add(self, IncludeIpv6Groups=None, IntergroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NumberOfUnicastSourceIpv6MacsPerMulticastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Adds a new customTopologyMulticastIpv6GroupRange node on the server and retrieves it in this instance.

		Args:
			IncludeIpv6Groups (bool): NOT DEFINED
			IntergroupUnicastIpv6Increment (str): NOT DEFINED
			IntraGroupUnicastIpv6Increment (str): NOT DEFINED
			MulticastAddressNodeStep (str): NOT DEFINED
			MulticastIpv6Count (number): NOT DEFINED
			MulticastIpv6Step (str): NOT DEFINED
			NumberOfUnicastSourceIpv6MacsPerMulticastIpv6 (number): NOT DEFINED
			SourceGroupMapping (str(fully-Meshed|one-To-One|manual-Mapping)): NOT DEFINED
			StartMulticastIpv6 (str): NOT DEFINED
			StartUnicastSourceIpv6 (str): NOT DEFINED
			UnicastAddressNodeStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyMulticastIpv6GroupRange data using find and the newly added customTopologyMulticastIpv6GroupRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyMulticastIpv6GroupRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeIpv6Groups=None, IntergroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NumberOfUnicastSourceIpv6MacsPerMulticastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Finds and retrieves customTopologyMulticastIpv6GroupRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyMulticastIpv6GroupRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyMulticastIpv6GroupRange data from the server.

		Args:
			IncludeIpv6Groups (bool): NOT DEFINED
			IntergroupUnicastIpv6Increment (str): NOT DEFINED
			IntraGroupUnicastIpv6Increment (str): NOT DEFINED
			MulticastAddressNodeStep (str): NOT DEFINED
			MulticastIpv6Count (number): NOT DEFINED
			MulticastIpv6Step (str): NOT DEFINED
			NumberOfUnicastSourceIpv6MacsPerMulticastIpv6 (number): NOT DEFINED
			SourceGroupMapping (str(fully-Meshed|one-To-One|manual-Mapping)): NOT DEFINED
			StartMulticastIpv6 (str): NOT DEFINED
			StartUnicastSourceIpv6 (str): NOT DEFINED
			UnicastAddressNodeStep (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyMulticastIpv6GroupRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyMulticastIpv6GroupRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyMulticastIpv6GroupRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
