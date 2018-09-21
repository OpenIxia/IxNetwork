from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LossLearnedInfo(Base):
	"""The LossLearnedInfo class encapsulates a system managed lossLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LossLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lossLearnedInfo'

	def __init__(self, parent):
		super(LossLearnedInfo, self).__init__(parent)

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
	def DestinationMacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationMacAddress')

	@property
	def FarEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('farEndLoss')

	@property
	def FarEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('farEndLossRatio')

	@property
	def LmrReceived(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('lmrReceived')

	@property
	def MdLevel(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def NearEndLoss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('nearEndLoss')

	@property
	def NearEndLossRatio(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('nearEndLossRatio')

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

	def find(self, BVlan=None, CVlan=None, DestinationMacAddress=None, FarEndLoss=None, FarEndLossRatio=None, LmrReceived=None, MdLevel=None, NearEndLoss=None, NearEndLossRatio=None, SVlan=None, SourceMacAddress=None, SourceMepId=None):
		"""Finds and retrieves lossLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lossLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lossLearnedInfo data from the server.

		Args:
			BVlan (str): NOT DEFINED
			CVlan (str): NOT DEFINED
			DestinationMacAddress (str): NOT DEFINED
			FarEndLoss (number): NOT DEFINED
			FarEndLossRatio (str): NOT DEFINED
			LmrReceived (bool): NOT DEFINED
			MdLevel (number): NOT DEFINED
			NearEndLoss (number): NOT DEFINED
			NearEndLossRatio (str): NOT DEFINED
			SVlan (str): NOT DEFINED
			SourceMacAddress (str): NOT DEFINED
			SourceMepId (number): NOT DEFINED

		Returns:
			self: This instance with matching lossLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lossLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lossLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
