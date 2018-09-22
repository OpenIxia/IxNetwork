from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ReqFecRange(Base):
	"""The ReqFecRange class encapsulates a user managed reqFecRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ReqFecRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'reqFecRange'

	def __init__(self, parent):
		super(ReqFecRange, self).__init__(parent)

	@property
	def EnableHopCount(self):
		"""Enables the hops along the path of the LSP.

		Returns:
			bool
		"""
		return self._get_attribute('enableHopCount')
	@EnableHopCount.setter
	def EnableHopCount(self, value):
		self._set_attribute('enableHopCount', value)

	@property
	def EnableStateTimer(self):
		"""Enable the Stale Request Timer.

		Returns:
			bool
		"""
		return self._get_attribute('enableStateTimer')
	@EnableStateTimer.setter
	def EnableStateTimer(self, value):
		self._set_attribute('enableStateTimer', value)

	@property
	def Enabled(self):
		"""Enables the use of this request FEC range for the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstNetwork(self):
		"""The first FEC network address in the range (in IP address format).

		Returns:
			str
		"""
		return self._get_attribute('firstNetwork')
	@FirstNetwork.setter
	def FirstNetwork(self, value):
		self._set_attribute('firstNetwork', value)

	@property
	def HopCount(self):
		"""The number of hops along the path of the LSP.

		Returns:
			number
		"""
		return self._get_attribute('hopCount')
	@HopCount.setter
	def HopCount(self, value):
		self._set_attribute('hopCount', value)

	@property
	def MaskWidth(self):
		"""The number of bits in the FEC mask applied to the FEC network address. The masked bits in the first network address form the FEC address prefix.

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def NextHopPeer(self):
		"""The IPv4 address of the LDP Peer that is the next hop router on this path. (0.0.0.0 indicates that requests will be sent to all of this router's peers that are in Downstream on Demand mode.)

		Returns:
			str
		"""
		return self._get_attribute('nextHopPeer')
	@NextHopPeer.setter
	def NextHopPeer(self, value):
		self._set_attribute('nextHopPeer', value)

	@property
	def NumberOfRoutes(self):
		"""The number of routes configured for this LDP requesting FEC range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def StaleReqTime(self):
		"""The Stale Request Time value. Value range is 1 to 65.535 seconds. (default = 300)

		Returns:
			number
		"""
		return self._get_attribute('staleReqTime')
	@StaleReqTime.setter
	def StaleReqTime(self, value):
		self._set_attribute('staleReqTime', value)

	def add(self, EnableHopCount=None, EnableStateTimer=None, Enabled=None, FirstNetwork=None, HopCount=None, MaskWidth=None, NextHopPeer=None, NumberOfRoutes=None, StaleReqTime=None):
		"""Adds a new reqFecRange node on the server and retrieves it in this instance.

		Args:
			EnableHopCount (bool): Enables the hops along the path of the LSP.
			EnableStateTimer (bool): Enable the Stale Request Timer.
			Enabled (bool): Enables the use of this request FEC range for the simulated router.
			FirstNetwork (str): The first FEC network address in the range (in IP address format).
			HopCount (number): The number of hops along the path of the LSP.
			MaskWidth (number): The number of bits in the FEC mask applied to the FEC network address. The masked bits in the first network address form the FEC address prefix.
			NextHopPeer (str): The IPv4 address of the LDP Peer that is the next hop router on this path. (0.0.0.0 indicates that requests will be sent to all of this router's peers that are in Downstream on Demand mode.)
			NumberOfRoutes (number): The number of routes configured for this LDP requesting FEC range.
			StaleReqTime (number): The Stale Request Time value. Value range is 1 to 65.535 seconds. (default = 300)

		Returns:
			self: This instance with all currently retrieved reqFecRange data using find and the newly added reqFecRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the reqFecRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableHopCount=None, EnableStateTimer=None, Enabled=None, FirstNetwork=None, HopCount=None, MaskWidth=None, NextHopPeer=None, NumberOfRoutes=None, StaleReqTime=None):
		"""Finds and retrieves reqFecRange data from the server.

		All named parameters support regex and can be used to selectively retrieve reqFecRange data from the server.
		By default the find method takes no parameters and will retrieve all reqFecRange data from the server.

		Args:
			EnableHopCount (bool): Enables the hops along the path of the LSP.
			EnableStateTimer (bool): Enable the Stale Request Timer.
			Enabled (bool): Enables the use of this request FEC range for the simulated router.
			FirstNetwork (str): The first FEC network address in the range (in IP address format).
			HopCount (number): The number of hops along the path of the LSP.
			MaskWidth (number): The number of bits in the FEC mask applied to the FEC network address. The masked bits in the first network address form the FEC address prefix.
			NextHopPeer (str): The IPv4 address of the LDP Peer that is the next hop router on this path. (0.0.0.0 indicates that requests will be sent to all of this router's peers that are in Downstream on Demand mode.)
			NumberOfRoutes (number): The number of routes configured for this LDP requesting FEC range.
			StaleReqTime (number): The Stale Request Time value. Value range is 1 to 65.535 seconds. (default = 300)

		Returns:
			self: This instance with matching reqFecRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of reqFecRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the reqFecRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
