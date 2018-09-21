from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CMacMappedIp(Base):
	"""The CMacMappedIp class encapsulates a user managed cMacMappedIp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CMacMappedIp property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'cMacMappedIp'

	def __init__(self, parent):
		super(CMacMappedIp, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true then this IP is associated with the B-MAC of the ethernet segment. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IpAddress(self):
		"""IP address value is given here depending on the IP Type. Default value is all zero.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpStep(self):
		"""If IP address is associated with a MAC range (C-MAC Range) then this step value is used to make the IP addresses for all C-MAC of that range unique. For example if C-MAC range has no of C-MAC 3 and IP address associated with this mac range is 1.1.1.1 with step 2 then IP addresses for 3 MACs of the mac range will be 1.1.1.1, 1.1.1.3 and 1.1.1.5. Default value is 1. This is used only in EVPN mode.

		Returns:
			number
		"""
		return self._get_attribute('ipStep')
	@IpStep.setter
	def IpStep(self, value):
		self._set_attribute('ipStep', value)

	@property
	def IpType(self):
		"""Drop down of {IPv4, IPv6}. If IPv4 is selected then IPv4 address is used. If IPv6 is selected then IPv6 address is used. Default value is IPv4.

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	def add(self, Enabled=None, IpAddress=None, IpStep=None, IpType=None):
		"""Adds a new cMacMappedIp node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true then this IP is associated with the B-MAC of the ethernet segment. Default value is false.
			IpAddress (str): IP address value is given here depending on the IP Type. Default value is all zero.
			IpStep (number): If IP address is associated with a MAC range (C-MAC Range) then this step value is used to make the IP addresses for all C-MAC of that range unique. For example if C-MAC range has no of C-MAC 3 and IP address associated with this mac range is 1.1.1.1 with step 2 then IP addresses for 3 MACs of the mac range will be 1.1.1.1, 1.1.1.3 and 1.1.1.5. Default value is 1. This is used only in EVPN mode.
			IpType (str(ipv4|ipv6)): Drop down of {IPv4, IPv6}. If IPv4 is selected then IPv4 address is used. If IPv6 is selected then IPv6 address is used. Default value is IPv4.

		Returns:
			self: This instance with all currently retrieved cMacMappedIp data using find and the newly added cMacMappedIp data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the cMacMappedIp data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, IpAddress=None, IpStep=None, IpType=None):
		"""Finds and retrieves cMacMappedIp data from the server.

		All named parameters support regex and can be used to selectively retrieve cMacMappedIp data from the server.
		By default the find method takes no parameters and will retrieve all cMacMappedIp data from the server.

		Args:
			Enabled (bool): If true then this IP is associated with the B-MAC of the ethernet segment. Default value is false.
			IpAddress (str): IP address value is given here depending on the IP Type. Default value is all zero.
			IpStep (number): If IP address is associated with a MAC range (C-MAC Range) then this step value is used to make the IP addresses for all C-MAC of that range unique. For example if C-MAC range has no of C-MAC 3 and IP address associated with this mac range is 1.1.1.1 with step 2 then IP addresses for 3 MACs of the mac range will be 1.1.1.1, 1.1.1.3 and 1.1.1.5. Default value is 1. This is used only in EVPN mode.
			IpType (str(ipv4|ipv6)): Drop down of {IPv4, IPv6}. If IPv4 is selected then IPv4 address is used. If IPv6 is selected then IPv6 address is used. Default value is IPv4.

		Returns:
			self: This instance with matching cMacMappedIp data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of cMacMappedIp data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the cMacMappedIp data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
