from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdVpls(Base):
	"""The AdVpls class encapsulates a system managed adVpls node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdVpls property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'adVpls'

	def __init__(self, parent):
		super(AdVpls, self).__init__(parent)

	@property
	def NeighborAddress(self):
		"""(Read Only) The descriptive identifier for the BGP neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighborAddress')

	@property
	def NextHopAddress(self):
		"""(Read Only) A 4-octet IP address which indicates the next hop.

		Returns:
			str
		"""
		return self._get_attribute('nextHopAddress')

	@property
	def RemotePeAddress(self):
		"""(Read Only) The descriptive identifier for the remote PE.

		Returns:
			str
		"""
		return self._get_attribute('remotePeAddress')

	@property
	def RemoteVplsId(self):
		"""(Read Only) The remote VPLS ID indicated by an IP or AS.

		Returns:
			str
		"""
		return self._get_attribute('remoteVplsId')

	@property
	def RemoteVsiId(self):
		"""(Read Only) The remote VSI Id indicated by 4 bytes unsigned number.

		Returns:
			number
		"""
		return self._get_attribute('remoteVsiId')

	@property
	def RouteDistinguisher(self):
		"""(Read Only) The route distinguisher indicated by the IP or AS number.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def RouteTarget(self):
		"""(Read Only) The route target indicated by the IP or AS number.

		Returns:
			str
		"""
		return self._get_attribute('routeTarget')

	@property
	def SupportedLocally(self):
		"""(Read Only) The boolean value indicating whether it is supported locally.

		Returns:
			bool
		"""
		return self._get_attribute('supportedLocally')

	def find(self, NeighborAddress=None, NextHopAddress=None, RemotePeAddress=None, RemoteVplsId=None, RemoteVsiId=None, RouteDistinguisher=None, RouteTarget=None, SupportedLocally=None):
		"""Finds and retrieves adVpls data from the server.

		All named parameters support regex and can be used to selectively retrieve adVpls data from the server.
		By default the find method takes no parameters and will retrieve all adVpls data from the server.

		Args:
			NeighborAddress (str): (Read Only) The descriptive identifier for the BGP neighbor.
			NextHopAddress (str): (Read Only) A 4-octet IP address which indicates the next hop.
			RemotePeAddress (str): (Read Only) The descriptive identifier for the remote PE.
			RemoteVplsId (str): (Read Only) The remote VPLS ID indicated by an IP or AS.
			RemoteVsiId (number): (Read Only) The remote VSI Id indicated by 4 bytes unsigned number.
			RouteDistinguisher (str): (Read Only) The route distinguisher indicated by the IP or AS number.
			RouteTarget (str): (Read Only) The route target indicated by the IP or AS number.
			SupportedLocally (bool): (Read Only) The boolean value indicating whether it is supported locally.

		Returns:
			self: This instance with matching adVpls data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of adVpls data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the adVpls data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
