from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PeriodicOamDmLearnedInfo(Base):
	"""The PeriodicOamDmLearnedInfo class encapsulates a system managed periodicOamDmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PeriodicOamDmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'periodicOamDmLearnedInfo'

	def __init__(self, parent):
		super(PeriodicOamDmLearnedInfo, self).__init__(parent)

	@property
	def AverageDelayNanoSec(self):
		"""(read only) The learned average delay in nanoseconds.

		Returns:
			number
		"""
		return self._get_attribute('averageDelayNanoSec')

	@property
	def AverageDelaySec(self):
		"""(read only) The learned average delay in seconds.

		Returns:
			number
		"""
		return self._get_attribute('averageDelaySec')

	@property
	def AverageDelayVariationNanoSec(self):
		"""(read only) The learned most recent delay variation in nano seconds.

		Returns:
			number
		"""
		return self._get_attribute('averageDelayVariationNanoSec')

	@property
	def AverageDelayVariationSec(self):
		"""(read only) The learned most recent delay variation in seconds.

		Returns:
			number
		"""
		return self._get_attribute('averageDelayVariationSec')

	@property
	def CVlan(self):
		"""(read only) The learned C-VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def DmmCountSent(self):
		"""(read only) The learned number of DMMs sent.

		Returns:
			number
		"""
		return self._get_attribute('dmmCountSent')

	@property
	def DstMacAddress(self):
		"""(read only) The learned destination MAC address.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

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
	def OneDmReceivedCount(self):
		"""(read only) The learned number of DM received.

		Returns:
			number
		"""
		return self._get_attribute('oneDmReceivedCount')

	@property
	def RecentDelayNanoSec(self):
		"""(read only) The learned most recent delay measurement in nanoseconds.

		Returns:
			number
		"""
		return self._get_attribute('recentDelayNanoSec')

	@property
	def RecentDelaySec(self):
		"""(read only) The learned most recent delay measurement in seconds.

		Returns:
			number
		"""
		return self._get_attribute('recentDelaySec')

	@property
	def RecentDelayVariationNanoSec(self):
		"""(read only) The learned most recent delay variation in nano seconds.

		Returns:
			number
		"""
		return self._get_attribute('recentDelayVariationNanoSec')

	@property
	def RecentDelayVariationSec(self):
		"""(read only) The learned most recent delay variation in seconds.

		Returns:
			number
		"""
		return self._get_attribute('recentDelayVariationSec')

	@property
	def SVlan(self):
		"""(read only) The learned S-VLAN identifier.

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

	def find(self, AverageDelayNanoSec=None, AverageDelaySec=None, AverageDelayVariationNanoSec=None, AverageDelayVariationSec=None, CVlan=None, DmmCountSent=None, DstMacAddress=None, MdLevel=None, NoReplyCount=None, OneDmReceivedCount=None, RecentDelayNanoSec=None, RecentDelaySec=None, RecentDelayVariationNanoSec=None, RecentDelayVariationSec=None, SVlan=None, SrcMacAddress=None):
		"""Finds and retrieves periodicOamDmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve periodicOamDmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all periodicOamDmLearnedInfo data from the server.

		Args:
			AverageDelayNanoSec (number): (read only) The learned average delay in nanoseconds.
			AverageDelaySec (number): (read only) The learned average delay in seconds.
			AverageDelayVariationNanoSec (number): (read only) The learned most recent delay variation in nano seconds.
			AverageDelayVariationSec (number): (read only) The learned most recent delay variation in seconds.
			CVlan (str): (read only) The learned C-VLAN identifier.
			DmmCountSent (number): (read only) The learned number of DMMs sent.
			DstMacAddress (str): (read only) The learned destination MAC address.
			MdLevel (number): (read only) The learned MD level for the periodic OAM.
			NoReplyCount (number): (read only) The learned number of periodic OAM no replies.
			OneDmReceivedCount (number): (read only) The learned number of DM received.
			RecentDelayNanoSec (number): (read only) The learned most recent delay measurement in nanoseconds.
			RecentDelaySec (number): (read only) The learned most recent delay measurement in seconds.
			RecentDelayVariationNanoSec (number): (read only) The learned most recent delay variation in nano seconds.
			RecentDelayVariationSec (number): (read only) The learned most recent delay variation in seconds.
			SVlan (str): (read only) The learned S-VLAN identifier.
			SrcMacAddress (str): (read only) The learned source MAC address.

		Returns:
			self: This instance with matching periodicOamDmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of periodicOamDmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the periodicOamDmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
