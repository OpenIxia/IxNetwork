from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PeriodicOamLtLearnedInfo(Base):
	"""The PeriodicOamLtLearnedInfo class encapsulates a system managed periodicOamLtLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PeriodicOamLtLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'periodicOamLtLearnedInfo'

	def __init__(self, parent):
		super(PeriodicOamLtLearnedInfo, self).__init__(parent)

	@property
	def LtLearnedHop(self):
		"""An instance of the LtLearnedHop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamltlearnedinfo.ltlearnedhop.ltlearnedhop.LtLearnedHop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamltlearnedinfo.ltlearnedhop.ltlearnedhop import LtLearnedHop
		return LtLearnedHop(self)

	@property
	def AverageHopCount(self):
		"""(read only) The learned average hop count.

		Returns:
			number
		"""
		return self._get_attribute('averageHopCount')

	@property
	def CVlan(self):
		"""(read only) The learned C-VLAN identifier. (CFM only)

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def CompleteReplyCount(self):
		"""(read only) The learned number of complete replies.

		Returns:
			number
		"""
		return self._get_attribute('completeReplyCount')

	@property
	def DstMacAddress(self):
		"""(read only) The learned destination MAC address.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def LtmSentCount(self):
		"""(read only) The learned number of Link Trace messages sent.

		Returns:
			number
		"""
		return self._get_attribute('ltmSentCount')

	@property
	def MdLevel(self):
		"""(read only) The learned MD level.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def NoReplyCount(self):
		"""(read only) The learned number of no replies.

		Returns:
			number
		"""
		return self._get_attribute('noReplyCount')

	@property
	def PartialReplyCount(self):
		"""(read only) The learned number of partial replies.

		Returns:
			number
		"""
		return self._get_attribute('partialReplyCount')

	@property
	def RecentHopCount(self):
		"""(read only) The learned recent hop count.

		Returns:
			number
		"""
		return self._get_attribute('recentHopCount')

	@property
	def RecentHops(self):
		"""(read only) The learned recent hops.

		Returns:
			str
		"""
		return self._get_attribute('recentHops')

	@property
	def RecentReplyStatus(self):
		"""(read only) The learned recent replies.

		Returns:
			str
		"""
		return self._get_attribute('recentReplyStatus')

	@property
	def SVlan(self):
		"""(read only) The learned S-VLAN identifier. (CFM only)

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SrcMacAddress(self):
		"""(read only) The learned source MAC address.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	def find(self, AverageHopCount=None, CVlan=None, CompleteReplyCount=None, DstMacAddress=None, LtmSentCount=None, MdLevel=None, NoReplyCount=None, PartialReplyCount=None, RecentHopCount=None, RecentHops=None, RecentReplyStatus=None, SVlan=None, SrcMacAddress=None):
		"""Finds and retrieves periodicOamLtLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve periodicOamLtLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all periodicOamLtLearnedInfo data from the server.

		Args:
			AverageHopCount (number): (read only) The learned average hop count.
			CVlan (str): (read only) The learned C-VLAN identifier. (CFM only)
			CompleteReplyCount (number): (read only) The learned number of complete replies.
			DstMacAddress (str): (read only) The learned destination MAC address.
			LtmSentCount (number): (read only) The learned number of Link Trace messages sent.
			MdLevel (number): (read only) The learned MD level.
			NoReplyCount (number): (read only) The learned number of no replies.
			PartialReplyCount (number): (read only) The learned number of partial replies.
			RecentHopCount (number): (read only) The learned recent hop count.
			RecentHops (str): (read only) The learned recent hops.
			RecentReplyStatus (str): (read only) The learned recent replies.
			SVlan (str): (read only) The learned S-VLAN identifier. (CFM only)
			SrcMacAddress (str): (read only) The learned source MAC address.

		Returns:
			self: This instance with matching periodicOamLtLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of periodicOamLtLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the periodicOamLtLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
