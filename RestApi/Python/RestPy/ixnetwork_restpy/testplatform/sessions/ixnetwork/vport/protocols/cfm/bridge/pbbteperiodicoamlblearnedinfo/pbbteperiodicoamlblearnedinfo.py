from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbTePeriodicOamLbLearnedInfo(Base):
	"""The PbbTePeriodicOamLbLearnedInfo class encapsulates a system managed pbbTePeriodicOamLbLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbTePeriodicOamLbLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pbbTePeriodicOamLbLearnedInfo'

	def __init__(self, parent):
		super(PbbTePeriodicOamLbLearnedInfo, self).__init__(parent)

	@property
	def AverageRtt(self):
		"""(read only) The learned average periodic OAM Round-Trip-Time.

		Returns:
			number
		"""
		return self._get_attribute('averageRtt')

	@property
	def BVlan(self):
		"""(read only) The learned periodic OAM B-VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The learned periodic OAM destination MAC address.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def LbmSentCount(self):
		"""(read only) The learned number of periodic OAM loopback messages sent.

		Returns:
			number
		"""
		return self._get_attribute('lbmSentCount')

	@property
	def MdLevel(self):
		"""(read only) The learned MD level for the periodic OAM.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def NoReplyCount(self):
		"""(read only) The learned number of periodic OAM no replies.

		Returns:
			number
		"""
		return self._get_attribute('noReplyCount')

	@property
	def RecentReachability(self):
		"""(read only) Indicates the status of the Ping.

		Returns:
			bool
		"""
		return self._get_attribute('recentReachability')

	@property
	def RecentRtt(self):
		"""(read only) Indicates the status of the round-trip-time

		Returns:
			number
		"""
		return self._get_attribute('recentRtt')

	@property
	def SrcMacAddress(self):
		"""(read only) The learned periodic OAM source MAC address.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	def find(self, AverageRtt=None, BVlan=None, DstMacAddress=None, LbmSentCount=None, MdLevel=None, NoReplyCount=None, RecentReachability=None, RecentRtt=None, SrcMacAddress=None):
		"""Finds and retrieves pbbTePeriodicOamLbLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbTePeriodicOamLbLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pbbTePeriodicOamLbLearnedInfo data from the server.

		Args:
			AverageRtt (number): (read only) The learned average periodic OAM Round-Trip-Time.
			BVlan (str): (read only) The learned periodic OAM B-VLAN identifier.
			DstMacAddress (str): (read only) The learned periodic OAM destination MAC address.
			LbmSentCount (number): (read only) The learned number of periodic OAM loopback messages sent.
			MdLevel (number): (read only) The learned MD level for the periodic OAM.
			NoReplyCount (number): (read only) The learned number of periodic OAM no replies.
			RecentReachability (bool): (read only) Indicates the status of the Ping.
			RecentRtt (number): (read only) Indicates the status of the round-trip-time
			SrcMacAddress (str): (read only) The learned periodic OAM source MAC address.

		Returns:
			self: This instance with matching pbbTePeriodicOamLbLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbTePeriodicOamLbLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbTePeriodicOamLbLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
