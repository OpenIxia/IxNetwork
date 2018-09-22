from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BwProfile(Base):
	"""The BwProfile class encapsulates a user managed bwProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BwProfile property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bwProfile'

	def __init__(self, parent):
		super(BwProfile, self).__init__(parent)

	@property
	def CbsMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('cbsMagnitude')
	@CbsMagnitude.setter
	def CbsMagnitude(self, value):
		self._set_attribute('cbsMagnitude', value)

	@property
	def CbsMultiplier(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('cbsMultiplier')
	@CbsMultiplier.setter
	def CbsMultiplier(self, value):
		self._set_attribute('cbsMultiplier', value)

	@property
	def Cf(self):
		"""If enabled, Coupling Flag is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('cf')
	@Cf.setter
	def Cf(self, value):
		self._set_attribute('cf', value)

	@property
	def CirMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('cirMagnitude')
	@CirMagnitude.setter
	def CirMagnitude(self, value):
		self._set_attribute('cirMagnitude', value)

	@property
	def CirMultiplier(self):
		"""It signifies two octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('cirMultiplier')
	@CirMultiplier.setter
	def CirMultiplier(self, value):
		self._set_attribute('cirMultiplier', value)

	@property
	def Cm(self):
		"""If enabled, Colored Mode Flag is 1. Default is false.

		Returns:
			bool
		"""
		return self._get_attribute('cm')
	@Cm.setter
	def Cm(self, value):
		self._set_attribute('cm', value)

	@property
	def EbsMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('ebsMagnitude')
	@EbsMagnitude.setter
	def EbsMagnitude(self, value):
		self._set_attribute('ebsMagnitude', value)

	@property
	def EbsMultiplier(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('ebsMultiplier')
	@EbsMultiplier.setter
	def EbsMultiplier(self, value):
		self._set_attribute('ebsMultiplier', value)

	@property
	def EirMagnitude(self):
		"""It signifies one octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('eirMagnitude')
	@EirMagnitude.setter
	def EirMagnitude(self, value):
		self._set_attribute('eirMagnitude', value)

	@property
	def EirMultiplier(self):
		"""It signifies two octet field. Default is 1.

		Returns:
			number
		"""
		return self._get_attribute('eirMultiplier')
	@EirMultiplier.setter
	def EirMultiplier(self, value):
		self._set_attribute('eirMultiplier', value)

	@property
	def Enabled(self):
		"""If enabled, bandwidth profile is in effect for the EVC.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PerCos(self):
		"""If enabled, Per CoS Flag shows user_priority bit values as significant and the value is set to 1. If the value is set to 0, the user_priority bit values as ignored and not processed. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('perCos')
	@PerCos.setter
	def PerCos(self, value):
		self._set_attribute('perCos', value)

	@property
	def UserPriorityBits000(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits000')
	@UserPriorityBits000.setter
	def UserPriorityBits000(self, value):
		self._set_attribute('userPriorityBits000', value)

	@property
	def UserPriorityBits001(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits001')
	@UserPriorityBits001.setter
	def UserPriorityBits001(self, value):
		self._set_attribute('userPriorityBits001', value)

	@property
	def UserPriorityBits010(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits010')
	@UserPriorityBits010.setter
	def UserPriorityBits010(self, value):
		self._set_attribute('userPriorityBits010', value)

	@property
	def UserPriorityBits011(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits011')
	@UserPriorityBits011.setter
	def UserPriorityBits011(self, value):
		self._set_attribute('userPriorityBits011', value)

	@property
	def UserPriorityBits100(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits100')
	@UserPriorityBits100.setter
	def UserPriorityBits100(self, value):
		self._set_attribute('userPriorityBits100', value)

	@property
	def UserPriorityBits101(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits101')
	@UserPriorityBits101.setter
	def UserPriorityBits101(self, value):
		self._set_attribute('userPriorityBits101', value)

	@property
	def UserPriorityBits110(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits110')
	@UserPriorityBits110.setter
	def UserPriorityBits110(self, value):
		self._set_attribute('userPriorityBits110', value)

	@property
	def UserPriorityBits111(self):
		"""If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1. Default is 0.

		Returns:
			bool
		"""
		return self._get_attribute('userPriorityBits111')
	@UserPriorityBits111.setter
	def UserPriorityBits111(self, value):
		self._set_attribute('userPriorityBits111', value)

	def add(self, CbsMagnitude=None, CbsMultiplier=None, Cf=None, CirMagnitude=None, CirMultiplier=None, Cm=None, EbsMagnitude=None, EbsMultiplier=None, EirMagnitude=None, EirMultiplier=None, Enabled=None, PerCos=None, UserPriorityBits000=None, UserPriorityBits001=None, UserPriorityBits010=None, UserPriorityBits011=None, UserPriorityBits100=None, UserPriorityBits101=None, UserPriorityBits110=None, UserPriorityBits111=None):
		"""Adds a new bwProfile node on the server and retrieves it in this instance.

		Args:
			CbsMagnitude (number): It signifies one octet field. Default is 1.
			CbsMultiplier (number): It signifies one octet field. Default is 1.
			Cf (bool): If enabled, Coupling Flag is set to 1. Default is 0.
			CirMagnitude (number): It signifies one octet field. Default is 1.
			CirMultiplier (number): It signifies two octet field. Default is 1.
			Cm (bool): If enabled, Colored Mode Flag is 1. Default is false.
			EbsMagnitude (number): It signifies one octet field. Default is 1.
			EbsMultiplier (number): It signifies one octet field. Default is 1.
			EirMagnitude (number): It signifies one octet field. Default is 1.
			EirMultiplier (number): It signifies two octet field. Default is 1.
			Enabled (bool): If enabled, bandwidth profile is in effect for the EVC.
			PerCos (bool): If enabled, Per CoS Flag shows user_priority bit values as significant and the value is set to 1. If the value is set to 0, the user_priority bit values as ignored and not processed. Default is 0.
			UserPriorityBits000 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1. Default is 0.
			UserPriorityBits001 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1. Default is 0.
			UserPriorityBits010 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1. Default is 0.
			UserPriorityBits011 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1. Default is 0.
			UserPriorityBits100 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1. Default is 0.
			UserPriorityBits101 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1. Default is 0.
			UserPriorityBits110 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1. Default is 0.
			UserPriorityBits111 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1. Default is 0.

		Returns:
			self: This instance with all currently retrieved bwProfile data using find and the newly added bwProfile data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bwProfile data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CbsMagnitude=None, CbsMultiplier=None, Cf=None, CirMagnitude=None, CirMultiplier=None, Cm=None, EbsMagnitude=None, EbsMultiplier=None, EirMagnitude=None, EirMultiplier=None, Enabled=None, PerCos=None, UserPriorityBits000=None, UserPriorityBits001=None, UserPriorityBits010=None, UserPriorityBits011=None, UserPriorityBits100=None, UserPriorityBits101=None, UserPriorityBits110=None, UserPriorityBits111=None):
		"""Finds and retrieves bwProfile data from the server.

		All named parameters support regex and can be used to selectively retrieve bwProfile data from the server.
		By default the find method takes no parameters and will retrieve all bwProfile data from the server.

		Args:
			CbsMagnitude (number): It signifies one octet field. Default is 1.
			CbsMultiplier (number): It signifies one octet field. Default is 1.
			Cf (bool): If enabled, Coupling Flag is set to 1. Default is 0.
			CirMagnitude (number): It signifies one octet field. Default is 1.
			CirMultiplier (number): It signifies two octet field. Default is 1.
			Cm (bool): If enabled, Colored Mode Flag is 1. Default is false.
			EbsMagnitude (number): It signifies one octet field. Default is 1.
			EbsMultiplier (number): It signifies one octet field. Default is 1.
			EirMagnitude (number): It signifies one octet field. Default is 1.
			EirMultiplier (number): It signifies two octet field. Default is 1.
			Enabled (bool): If enabled, bandwidth profile is in effect for the EVC.
			PerCos (bool): If enabled, Per CoS Flag shows user_priority bit values as significant and the value is set to 1. If the value is set to 0, the user_priority bit values as ignored and not processed. Default is 0.
			UserPriorityBits000 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 000 and the value is set to 1. Default is 0.
			UserPriorityBits001 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 001 and the value is set to 1. Default is 0.
			UserPriorityBits010 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 010 and the value is set to 1. Default is 0.
			UserPriorityBits011 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 011 and the value is set to 1. Default is 0.
			UserPriorityBits100 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 100 and the value is set to 1. Default is 0.
			UserPriorityBits101 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 101 and the value is set to 1. Default is 0.
			UserPriorityBits110 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 110 and the value is set to 1. Default is 0.
			UserPriorityBits111 (bool): If enabled, Bandwidth Profile applies to frames with user_priority as 111 and the value is set to 1. Default is 0.

		Returns:
			self: This instance with matching bwProfile data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bwProfile data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bwProfile data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
