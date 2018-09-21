from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedRoute(Base):
	"""The LearnedRoute class encapsulates a system managed learnedRoute node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedRoute property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedRoute'

	def __init__(self, parent):
		super(LearnedRoute, self).__init__(parent)

	@property
	def AsPath(self):
		"""Indicates the local IP address of the BGP router.

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def BlockOffset(self):
		"""The Label Block Offset (VBO) is the value used to help define this specific label block uniquely-as a subset of all of the possible labels.

		Returns:
			number
		"""
		return self._get_attribute('blockOffset')

	@property
	def BlockSize(self):
		"""The size of the label block, in bytes.

		Returns:
			number
		"""
		return self._get_attribute('blockSize')

	@property
	def ControlWordEnabled(self):
		"""Indicates if the label uses a control word.

		Returns:
			bool
		"""
		return self._get_attribute('controlWordEnabled')

	@property
	def IpPrefix(self):
		"""The route IP address prefix.

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LabelBase(self):
		"""The first label in the learned information.

		Returns:
			number
		"""
		return self._get_attribute('labelBase')

	@property
	def LocalPreference(self):
		"""Indicates the value of the local preference attribute.

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MaxLabel(self):
		"""The last label to use.

		Returns:
			number
		"""
		return self._get_attribute('maxLabel')

	@property
	def MultiExitDiscriminator(self):
		"""A metric field of the route file.

		Returns:
			number
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def Neighbor(self):
		"""The local IP address for this Ixia-emulated BGP neighbor/peer.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def NextHop(self):
		"""The next hop on the path to the destination network in the learned route.

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	@property
	def OriginType(self):
		"""An indication of where the route entry originated.

		Returns:
			str
		"""
		return self._get_attribute('originType')

	@property
	def PrefixLength(self):
		"""The prefix length of the route.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')

	@property
	def RouteDistinguisher(self):
		"""The route distinguisher for the route, for use with IPv4 and IPv6 MPLS VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def SeqDeliveryEnabled(self):
		"""Indicates if sequencial delivery is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('seqDeliveryEnabled')

	@property
	def SiteId(self):
		"""The site ID.

		Returns:
			number
		"""
		return self._get_attribute('siteId')

	def find(self, AsPath=None, BlockOffset=None, BlockSize=None, ControlWordEnabled=None, IpPrefix=None, LabelBase=None, LocalPreference=None, MaxLabel=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None, RouteDistinguisher=None, SeqDeliveryEnabled=None, SiteId=None):
		"""Finds and retrieves learnedRoute data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedRoute data from the server.
		By default the find method takes no parameters and will retrieve all learnedRoute data from the server.

		Args:
			AsPath (str): Indicates the local IP address of the BGP router.
			BlockOffset (number): The Label Block Offset (VBO) is the value used to help define this specific label block uniquely-as a subset of all of the possible labels.
			BlockSize (number): The size of the label block, in bytes.
			ControlWordEnabled (bool): Indicates if the label uses a control word.
			IpPrefix (str): The route IP address prefix.
			LabelBase (number): The first label in the learned information.
			LocalPreference (number): Indicates the value of the local preference attribute.
			MaxLabel (number): The last label to use.
			MultiExitDiscriminator (number): A metric field of the route file.
			Neighbor (str): The local IP address for this Ixia-emulated BGP neighbor/peer.
			NextHop (str): The next hop on the path to the destination network in the learned route.
			OriginType (str): An indication of where the route entry originated.
			PrefixLength (number): The prefix length of the route.
			RouteDistinguisher (str): The route distinguisher for the route, for use with IPv4 and IPv6 MPLS VPN address types.
			SeqDeliveryEnabled (bool): Indicates if sequencial delivery is enabled.
			SiteId (number): The site ID.

		Returns:
			self: This instance with matching learnedRoute data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedRoute data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedRoute data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
