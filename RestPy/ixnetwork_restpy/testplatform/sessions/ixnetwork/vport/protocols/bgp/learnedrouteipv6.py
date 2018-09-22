from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedRouteIpv6(Base):
	"""The LearnedRouteIpv6 class encapsulates a system managed learnedRouteIpv6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedRouteIpv6 property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedRouteIpv6'

	def __init__(self, parent):
		super(LearnedRouteIpv6, self).__init__(parent)

	@property
	def AsPath(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def BlockOffset(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('blockOffset')

	@property
	def BlockSize(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('blockSize')

	@property
	def ControlWordEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('controlWordEnabled')

	@property
	def IpPrefix(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LabelBase(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('labelBase')

	@property
	def LocalPreference(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MaxLabel(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxLabel')

	@property
	def MultiExitDiscriminator(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def Neighbor(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def NextHop(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	@property
	def OriginType(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('originType')

	@property
	def PrefixLength(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')

	@property
	def RouteDistinguisher(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def SeqDeliveryEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('seqDeliveryEnabled')

	@property
	def SiteId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('siteId')

	def find(self, AsPath=None, BlockOffset=None, BlockSize=None, ControlWordEnabled=None, IpPrefix=None, LabelBase=None, LocalPreference=None, MaxLabel=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None, RouteDistinguisher=None, SeqDeliveryEnabled=None, SiteId=None):
		"""Finds and retrieves learnedRouteIpv6 data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedRouteIpv6 data from the server.
		By default the find method takes no parameters and will retrieve all learnedRouteIpv6 data from the server.

		Args:
			AsPath (str): NOT DEFINED
			BlockOffset (number): NOT DEFINED
			BlockSize (number): NOT DEFINED
			ControlWordEnabled (bool): NOT DEFINED
			IpPrefix (str): NOT DEFINED
			LabelBase (number): NOT DEFINED
			LocalPreference (number): NOT DEFINED
			MaxLabel (number): NOT DEFINED
			MultiExitDiscriminator (number): NOT DEFINED
			Neighbor (str): NOT DEFINED
			NextHop (str): NOT DEFINED
			OriginType (str): NOT DEFINED
			PrefixLength (number): NOT DEFINED
			RouteDistinguisher (str): NOT DEFINED
			SeqDeliveryEnabled (bool): NOT DEFINED
			SiteId (number): NOT DEFINED

		Returns:
			self: This instance with matching learnedRouteIpv6 data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedRouteIpv6 data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedRouteIpv6 data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
