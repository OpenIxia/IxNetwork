from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UniStatusLearnedInfo(Base):
	"""The UniStatusLearnedInfo class encapsulates a system managed uniStatusLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UniStatusLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'uniStatusLearnedInfo'

	def __init__(self, parent):
		super(UniStatusLearnedInfo, self).__init__(parent)

	@property
	def CbsMagnitude(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('cbsMagnitude')

	@property
	def CbsMultiplier(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('cbsMultiplier')

	@property
	def Cf(self):
		"""It signifies coupling flag.

		Returns:
			str
		"""
		return self._get_attribute('cf')

	@property
	def CirMagnitude(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('cirMagnitude')

	@property
	def CirMultiplier(self):
		"""It signifies two octet field.

		Returns:
			str
		"""
		return self._get_attribute('cirMultiplier')

	@property
	def Cm(self):
		"""It signifies color mode flag.

		Returns:
			str
		"""
		return self._get_attribute('cm')

	@property
	def EbsMagnitude(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('ebsMagnitude')

	@property
	def EbsMultiplier(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('ebsMultiplier')

	@property
	def EirMagnitude(self):
		"""It signifies one octet field.

		Returns:
			str
		"""
		return self._get_attribute('eirMagnitude')

	@property
	def EirMultiplier(self):
		"""It signifies two octet field.

		Returns:
			str
		"""
		return self._get_attribute('eirMultiplier')

	@property
	def EvcMapType(self):
		"""It signifies the type of EVC MAP type.

		Returns:
			str
		"""
		return self._get_attribute('evcMapType')

	@property
	def PerCos(self):
		"""It signifies per cos behavior of bandwidth profile.

		Returns:
			str
		"""
		return self._get_attribute('perCos')

	@property
	def UniId(self):
		"""It signifies the ID of user network interface.

		Returns:
			str
		"""
		return self._get_attribute('uniId')

	@property
	def UniIdLength(self):
		"""It signifies the length of the UNI ID value.

		Returns:
			number
		"""
		return self._get_attribute('uniIdLength')

	@property
	def UserPriorityBits000(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits000')

	@property
	def UserPriorityBits001(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits001')

	@property
	def UserPriorityBits010(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits010')

	@property
	def UserPriorityBits011(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits011')

	@property
	def UserPriorityBits100(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits100')

	@property
	def UserPriorityBits101(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits101')

	@property
	def UserPriorityBits110(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits110')

	@property
	def UserPriorityBits111(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1.

		Returns:
			str
		"""
		return self._get_attribute('userPriorityBits111')

	def find(self, CbsMagnitude=None, CbsMultiplier=None, Cf=None, CirMagnitude=None, CirMultiplier=None, Cm=None, EbsMagnitude=None, EbsMultiplier=None, EirMagnitude=None, EirMultiplier=None, EvcMapType=None, PerCos=None, UniId=None, UniIdLength=None, UserPriorityBits000=None, UserPriorityBits001=None, UserPriorityBits010=None, UserPriorityBits011=None, UserPriorityBits100=None, UserPriorityBits101=None, UserPriorityBits110=None, UserPriorityBits111=None):
		"""Finds and retrieves uniStatusLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve uniStatusLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all uniStatusLearnedInfo data from the server.

		Args:
			CbsMagnitude (str): It signifies one octet field.
			CbsMultiplier (str): It signifies one octet field.
			Cf (str): It signifies coupling flag.
			CirMagnitude (str): It signifies one octet field.
			CirMultiplier (str): It signifies two octet field.
			Cm (str): It signifies color mode flag.
			EbsMagnitude (str): It signifies one octet field.
			EbsMultiplier (str): It signifies one octet field.
			EirMagnitude (str): It signifies one octet field.
			EirMultiplier (str): It signifies two octet field.
			EvcMapType (str): It signifies the type of EVC MAP type.
			PerCos (str): It signifies per cos behavior of bandwidth profile.
			UniId (str): It signifies the ID of user network interface.
			UniIdLength (number): It signifies the length of the UNI ID value.
			UserPriorityBits000 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1.
			UserPriorityBits001 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1.
			UserPriorityBits010 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1.
			UserPriorityBits011 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1.
			UserPriorityBits100 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1.
			UserPriorityBits101 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1.
			UserPriorityBits110 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1.
			UserPriorityBits111 (str): If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1.

		Returns:
			self: This instance with matching uniStatusLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of uniStatusLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the uniStatusLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
