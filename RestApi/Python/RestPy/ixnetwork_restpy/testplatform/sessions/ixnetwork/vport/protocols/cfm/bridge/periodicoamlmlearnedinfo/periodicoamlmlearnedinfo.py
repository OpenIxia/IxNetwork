from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PeriodicOamLmLearnedInfo(Base):
	"""The PeriodicOamLmLearnedInfo class encapsulates a system managed periodicOamLmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PeriodicOamLmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'periodicOamLmLearnedInfo'

	def __init__(self, parent):
		super(PeriodicOamLmLearnedInfo, self).__init__(parent)

	@property
	def AvgFarEndLoss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('avgFarEndLoss')

	@property
	def AvgNearEndLoss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('avgNearEndLoss')

	@property
	def BVlan(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('bVlan')

	@property
	def CVlan(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def CcmReceivedCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ccmReceivedCount')

	@property
	def CcmSentCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ccmSentCount')

	@property
	def CurrentFarEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('currentFarEndLoss')

	@property
	def CurrentFarEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('currentFarEndLossRatio')

	@property
	def CurrentNearEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('currentNearEndLoss')

	@property
	def CurrentNearEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('currentNearEndLossRatio')

	@property
	def DestinationMacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationMacAddress')

	@property
	def LmmSentCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('lmmSentCount')

	@property
	def MaxFarEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxFarEndLoss')

	@property
	def MaxFarEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('maxFarEndLossRatio')

	@property
	def MaxNearEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxNearEndLoss')

	@property
	def MaxNearEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('maxNearEndLossRatio')

	@property
	def MdLevel(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def MinFarEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('minFarEndLoss')

	@property
	def MinFarEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('minFarEndLossRatio')

	@property
	def MinNearEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('minNearEndLoss')

	@property
	def MinNearEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('minNearEndLossRatio')

	@property
	def NoReplyCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('noReplyCount')

	@property
	def SVlan(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SourceMacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sourceMacAddress')

	@property
	def SourceMepId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sourceMepId')

	def find(self, AvgFarEndLoss=None, AvgNearEndLoss=None, BVlan=None, CVlan=None, CcmReceivedCount=None, CcmSentCount=None, CurrentFarEndLoss=None, CurrentFarEndLossRatio=None, CurrentNearEndLoss=None, CurrentNearEndLossRatio=None, DestinationMacAddress=None, LmmSentCount=None, MaxFarEndLoss=None, MaxFarEndLossRatio=None, MaxNearEndLoss=None, MaxNearEndLossRatio=None, MdLevel=None, MinFarEndLoss=None, MinFarEndLossRatio=None, MinNearEndLoss=None, MinNearEndLossRatio=None, NoReplyCount=None, SVlan=None, SourceMacAddress=None, SourceMepId=None):
		"""Finds and retrieves periodicOamLmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve periodicOamLmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all periodicOamLmLearnedInfo data from the server.

		Args:
			AvgFarEndLoss (str): NOT DEFINED
			AvgNearEndLoss (str): NOT DEFINED
			BVlan (str): NOT DEFINED
			CVlan (str): NOT DEFINED
			CcmReceivedCount (number): NOT DEFINED
			CcmSentCount (number): NOT DEFINED
			CurrentFarEndLoss (number): NOT DEFINED
			CurrentFarEndLossRatio (str): NOT DEFINED
			CurrentNearEndLoss (number): NOT DEFINED
			CurrentNearEndLossRatio (str): NOT DEFINED
			DestinationMacAddress (str): NOT DEFINED
			LmmSentCount (number): NOT DEFINED
			MaxFarEndLoss (number): NOT DEFINED
			MaxFarEndLossRatio (str): NOT DEFINED
			MaxNearEndLoss (number): NOT DEFINED
			MaxNearEndLossRatio (str): NOT DEFINED
			MdLevel (number): NOT DEFINED
			MinFarEndLoss (number): NOT DEFINED
			MinFarEndLossRatio (str): NOT DEFINED
			MinNearEndLoss (number): NOT DEFINED
			MinNearEndLossRatio (str): NOT DEFINED
			NoReplyCount (number): NOT DEFINED
			SVlan (str): NOT DEFINED
			SourceMacAddress (str): NOT DEFINED
			SourceMepId (number): NOT DEFINED

		Returns:
			self: This instance with matching periodicOamLmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of periodicOamLmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the periodicOamLmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
