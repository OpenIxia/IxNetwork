from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EvcStatusLearnedInfo(Base):
	"""The EvcStatusLearnedInfo class encapsulates a system managed evcStatusLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EvcStatusLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'evcStatusLearnedInfo'

	def __init__(self, parent):
		super(EvcStatusLearnedInfo, self).__init__(parent)

	@property
	def CbsMagnitude(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('cbsMagnitude')

	@property
	def CbsMultiplier(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('cbsMultiplier')

	@property
	def Cf(self):
		"""If enabled, Coupling Flag is 1. Default is false.

		Returns:
			str
		"""
		return self._get_attribute('cf')

	@property
	def CirMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('cirMagnitude')

	@property
	def CirMultiplier(self):
		"""It signifies two octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('cirMultiplier')

	@property
	def Cm(self):
		"""If enabled, Colored Mode Flag is 1. Default is false.

		Returns:
			str
		"""
		return self._get_attribute('cm')

	@property
	def DefaultEvc(self):
		"""It signifies the default EVC.

		Returns:
			str
		"""
		return self._get_attribute('defaultEvc')

	@property
	def EbsMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('ebsMagnitude')

	@property
	def EbsMultiplier(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('ebsMultiplier')

	@property
	def EirMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('eirMagnitude')

	@property
	def EirMultiplier(self):
		"""It signifies two octet field. Default is 1.

		Returns:
			str
		"""
		return self._get_attribute('eirMultiplier')

	@property
	def EvcId(self):
		"""It signifies the ID of the Ethernet Virtual Connection.

		Returns:
			str
		"""
		return self._get_attribute('evcId')

	@property
	def EvcIdLength(self):
		"""It signifies the length of the EVC ID.

		Returns:
			str
		"""
		return self._get_attribute('evcIdLength')

	@property
	def EvcType(self):
		"""It signifies the type of EVC.

		Returns:
			str
		"""
		return self._get_attribute('evcType')

	@property
	def PerCos(self):
		"""If enabled, Per CoS Flag shows user_priority bit values as significant and the value is set to 1. If the value is set to 0, the user_priority bit values as ignored and not processed. Default is 0

		Returns:
			str
		"""
		return self._get_attribute('perCos')

	@property
	def ReferenceId(self):
		"""It signifies the EVC reference Id.

		Returns:
			str
		"""
		return self._get_attribute('referenceId')

	@property
	def StatusType(self):
		"""It signifies the EVC status.

		Returns:
			str
		"""
		return self._get_attribute('statusType')

	@property
	def UntaggedPriorityTag(self):
		"""It signifies the priority tag of the untagged value.

		Returns:
			str
		"""
		return self._get_attribute('untaggedPriorityTag')

	@property
	def UserPriorityBits000(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits000')

	@property
	def UserPriorityBits001(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits001')

	@property
	def UserPriorityBits010(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits010')

	@property
	def UserPriorityBits011(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits011')

	@property
	def UserPriorityBits100(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits100')

	@property
	def UserPriorityBits101(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits101')

	@property
	def UserPriorityBits110(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits110')

	@property
	def UserPriorityBits111(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1. Default is 0.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits111')

	@property
	def VlanId(self):
		"""It signifies the ID of the virtual local area network.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	def find(self, CbsMagnitude=None, CbsMultiplier=None, Cf=None, CirMagnitude=None, CirMultiplier=None, Cm=None, DefaultEvc=None, EbsMagnitude=None, EbsMultiplier=None, EirMagnitude=None, EirMultiplier=None, EvcId=None, EvcIdLength=None, EvcType=None, PerCos=None, ReferenceId=None, StatusType=None, UntaggedPriorityTag=None, UserPriorityBits000=None, UserPriorityBits001=None, UserPriorityBits010=None, UserPriorityBits011=None, UserPriorityBits100=None, UserPriorityBits101=None, UserPriorityBits110=None, UserPriorityBits111=None, VlanId=None):
		"""Finds and retrieves evcStatusLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve evcStatusLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all evcStatusLearnedInfo data from the server.

		Args:
			CbsMagnitude (str): It signifies one octet field.
			CbsMultiplier (str): It signifies one octet field. Default is 1.
			Cf (str): If enabled, Coupling Flag is 1. Default is false.
			CirMagnitude (str): It signifies one octet field. Default is 1.
			CirMultiplier (str): It signifies two octet field. Default is 1.
			Cm (str): If enabled, Colored Mode Flag is 1. Default is false.
			DefaultEvc (str): It signifies the default EVC.
			EbsMagnitude (str): It signifies one octet field. Default is 1.
			EbsMultiplier (str): It signifies one octet field. Default is 1.
			EirMagnitude (str): It signifies one octet field. Default is 1.
			EirMultiplier (str): It signifies two octet field. Default is 1.
			EvcId (str): It signifies the ID of the Ethernet Virtual Connection.
			EvcIdLength (str): It signifies the length of the EVC ID.
			EvcType (str): It signifies the type of EVC.
			PerCos (str): If enabled, Per CoS Flag shows user_priority bit values as significant and the value is set to 1. If the value is set to 0, the user_priority bit values as ignored and not processed. Default is 0
			ReferenceId (str): It signifies the EVC reference Id.
			StatusType (str): It signifies the EVC status.
			UntaggedPriorityTag (str): It signifies the priority tag of the untagged value.
			UserPriorityBits000 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1. Default is 0.
			UserPriorityBits001 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1. Default is 0.
			UserPriorityBits010 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1. Default is 0.
			UserPriorityBits011 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1. Default is 0.
			UserPriorityBits100 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1. Default is 0.
			UserPriorityBits101 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1. Default is 0.
			UserPriorityBits110 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1. Default is 0.
			UserPriorityBits111 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1. Default is 0.
			VlanId (str): It signifies the ID of the virtual local area network.

		Returns:
			self: This instance with matching evcStatusLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evcStatusLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evcStatusLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
