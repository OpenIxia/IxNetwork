from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TunnelLeafRange(Base):
	"""The TunnelLeafRange class encapsulates a user managed tunnelLeafRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TunnelLeafRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'tunnelLeafRange'

	def __init__(self, parent):
		super(TunnelLeafRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables the RSVP-TE Tunnel Tail Range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IpCount(self):
		"""The number of IPv4 addresses in the range of Tunnel Tail addresses.

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IpStart(self):
		"""The first IPv4 address in the range of Tunnel Tail addresses to be associated with the Ixia-emulated RSVP-TE router.

		Returns:
			str
		"""
		return self._get_attribute('ipStart')
	@IpStart.setter
	def IpStart(self, value):
		self._set_attribute('ipStart', value)

	@property
	def SubLspDown(self):
		"""This can be true only for Tail Ranges of type 'Egress'. If enabled and a sub-lsp to the tail is up, it is torn-down by sending a Resv Tear to the ingress. From this point onwards, any Path sent to this Tail is dropped silently, thereby simulating that the sub-lsps terminating on the endpoints in this Tail Range is down.

		Returns:
			bool
		"""
		return self._get_attribute('subLspDown')
	@SubLspDown.setter
	def SubLspDown(self, value):
		self._set_attribute('subLspDown', value)

	def add(self, Enabled=None, IpCount=None, IpStart=None, SubLspDown=None):
		"""Adds a new tunnelLeafRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, enables the RSVP-TE Tunnel Tail Range.
			IpCount (number): The number of IPv4 addresses in the range of Tunnel Tail addresses.
			IpStart (str): The first IPv4 address in the range of Tunnel Tail addresses to be associated with the Ixia-emulated RSVP-TE router.
			SubLspDown (bool): This can be true only for Tail Ranges of type 'Egress'. If enabled and a sub-lsp to the tail is up, it is torn-down by sending a Resv Tear to the ingress. From this point onwards, any Path sent to this Tail is dropped silently, thereby simulating that the sub-lsps terminating on the endpoints in this Tail Range is down.

		Returns:
			self: This instance with all currently retrieved tunnelLeafRange data using find and the newly added tunnelLeafRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the tunnelLeafRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, IpCount=None, IpStart=None, SubLspDown=None):
		"""Finds and retrieves tunnelLeafRange data from the server.

		All named parameters support regex and can be used to selectively retrieve tunnelLeafRange data from the server.
		By default the find method takes no parameters and will retrieve all tunnelLeafRange data from the server.

		Args:
			Enabled (bool): If true, enables the RSVP-TE Tunnel Tail Range.
			IpCount (number): The number of IPv4 addresses in the range of Tunnel Tail addresses.
			IpStart (str): The first IPv4 address in the range of Tunnel Tail addresses to be associated with the Ixia-emulated RSVP-TE router.
			SubLspDown (bool): This can be true only for Tail Ranges of type 'Egress'. If enabled and a sub-lsp to the tail is up, it is torn-down by sending a Resv Tear to the ingress. From this point onwards, any Path sent to this Tail is dropped silently, thereby simulating that the sub-lsps terminating on the endpoints in this Tail Range is down.

		Returns:
			self: This instance with matching tunnelLeafRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tunnelLeafRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tunnelLeafRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
