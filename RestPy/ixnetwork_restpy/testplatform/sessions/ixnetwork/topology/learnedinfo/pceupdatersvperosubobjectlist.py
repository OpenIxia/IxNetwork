from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceUpdateRsvpEroSubObjectList(Base):
	"""The PceUpdateRsvpEroSubObjectList class encapsulates a system managed pceUpdateRsvpEroSubObjectList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceUpdateRsvpEroSubObjectList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceUpdateRsvpEroSubObjectList'

	def __init__(self, parent):
		super(PceUpdateRsvpEroSubObjectList, self).__init__(parent)

	@property
	def ActiveThisEro(self):
		"""Controls whether the ERO sub-object will be sent in the PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeThisEro')

	@property
	def AsNumber(self):
		"""AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber')

	@property
	def Ipv4Prefix(self):
		"""IPv4 Prefix is specified as an IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Prefix')

	@property
	def Ipv6Prefix(self):
		"""IPv6 Prefix is specified as an IPv6 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Prefix')

	@property
	def LooseHop(self):
		"""Indicates if user wants to represent a loose-hop sub object in the LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('looseHop')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def SubObjectType(self):
		"""Using the Sub Object Type control user can configure which sub object needs to be included from the following options: Not Applicable IPv4 Prefix IPv6 Prefix AS Number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	def find(self):
		"""Finds and retrieves pceUpdateRsvpEroSubObjectList data from the server.

		All named parameters support regex and can be used to selectively retrieve pceUpdateRsvpEroSubObjectList data from the server.
		By default the find method takes no parameters and will retrieve all pceUpdateRsvpEroSubObjectList data from the server.

		Returns:
			self: This instance with matching pceUpdateRsvpEroSubObjectList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceUpdateRsvpEroSubObjectList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceUpdateRsvpEroSubObjectList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
