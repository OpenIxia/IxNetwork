from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbTeLbLearnedInfo(Base):
	"""The PbbTeLbLearnedInfo class encapsulates a system managed pbbTeLbLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTeLbLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTeLbLearnedInfo'

	def __init__(self, parent):
		super(PbbTeLbLearnedInfo, self).__init__(parent)

	@property
	def BVlan(self):
		"""(read only) The VLAN identifier for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The destination MAC address for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def MdLevel(self):
		"""(read only) The MD level for the loopback message.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def Reachability(self):
		"""(read only) If true, the Ping message was received and responded to.

		Returns:
			bool
		"""
		return self._get_attribute('reachability')

	@property
	def Rtt(self):
		"""(read only) The round trip time for the PBB-TE loopback message.

		Returns:
			number
		"""
		return self._get_attribute('rtt')

	@property
	def SrcMacAddress(self):
		"""(read only) The source MAC address for the loopback message.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def TransactionId(self):
		"""(read only) The transaction identifier sent with the loopback message.

		Returns:
			number
		"""
		return self._get_attribute('transactionId')

	def find(self, BVlan=None, DstMacAddress=None, MdLevel=None, Reachability=None, Rtt=None, SrcMacAddress=None, TransactionId=None):
		"""Finds and retrieves pbbTeLbLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTeLbLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTeLbLearnedInfo data from the server.

		Args:
			BVlan (str): (read only) The VLAN identifier for the loopback message.
			DstMacAddress (str): (read only) The destination MAC address for the loopback message.
			MdLevel (number): (read only) The MD level for the loopback message.
			Reachability (bool): (read only) If true, the Ping message was received and responded to.
			Rtt (number): (read only) The round trip time for the PBB-TE loopback message.
			SrcMacAddress (str): (read only) The source MAC address for the loopback message.
			TransactionId (number): (read only) The transaction identifier sent with the loopback message.

		Returns:
			self: This instance with matching pbbTeLbLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTeLbLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTeLbLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
