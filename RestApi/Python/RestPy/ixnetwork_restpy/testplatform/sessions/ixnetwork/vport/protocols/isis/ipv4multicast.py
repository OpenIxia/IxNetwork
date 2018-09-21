from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4Multicast(Base):
	"""The Ipv4Multicast class encapsulates a system managed ipv4Multicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4Multicast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4Multicast'

	def __init__(self, parent):
		super(Ipv4Multicast, self).__init__(parent)

	@property
	def Ipv4UnicastItem(self):
		"""An instance of the Ipv4UnicastItem class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4unicastitem.Ipv4UnicastItem)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4unicastitem import Ipv4UnicastItem
		return Ipv4UnicastItem(self)

	@property
	def Age(self):
		"""This indicates the age in time, in seconds, since it was last refreshed.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def HostName(self):
		"""The host name as retrieved from the related packets.

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def Ipv4MulticastGroupAddress(self):
		"""This indicates the IPv4 Multicast Group Address in the Group Record.

		Returns:
			str
		"""
		return self._get_attribute('ipv4MulticastGroupAddress')

	@property
	def LspId(self):
		"""This indicates the LSP identification number.

		Returns:
			str
		"""
		return self._get_attribute('lspId')

	@property
	def SequenceNumber(self):
		"""This indicates the sequence number of the LSP containing the route.

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def VlanId(self):
		"""This indicates the VLAN ID in the Group Record.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	def find(self, Age=None, HostName=None, Ipv4MulticastGroupAddress=None, LspId=None, SequenceNumber=None, VlanId=None):
		"""Finds and retrieves ipv4Multicast data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4Multicast data from the server.
		By default the find method takes no parameters and will retrieve all ipv4Multicast data from the server.

		Args:
			Age (number): This indicates the age in time, in seconds, since it was last refreshed.
			HostName (str): The host name as retrieved from the related packets.
			Ipv4MulticastGroupAddress (str): This indicates the IPv4 Multicast Group Address in the Group Record.
			LspId (str): This indicates the LSP identification number.
			SequenceNumber (number): This indicates the sequence number of the LSP containing the route.
			VlanId (number): This indicates the VLAN ID in the Group Record.

		Returns:
			self: This instance with matching ipv4Multicast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4Multicast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4Multicast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
