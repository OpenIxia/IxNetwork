from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""The Field class encapsulates a system managed field node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Field property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def __id__(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('__id__')

	@property
	def ActiveFieldChoice(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('activeFieldChoice')
	@ActiveFieldChoice.setter
	def ActiveFieldChoice(self, value):
		self._set_attribute('activeFieldChoice', value)

	@property
	def Auto(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('auto')
	@Auto.setter
	def Auto(self, value):
		self._set_attribute('auto', value)

	@property
	def CountValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('countValue')
	@CountValue.setter
	def CountValue(self, value):
		self._set_attribute('countValue', value)

	@property
	def DefaultValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('defaultValue')

	@property
	def DisplayName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def EnumValues(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('enumValues')

	@property
	def FieldChoice(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fieldChoice')

	@property
	def FieldTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldTypeId')

	@property
	def FieldValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldValue')
	@FieldValue.setter
	def FieldValue(self, value):
		self._set_attribute('fieldValue', value)

	@property
	def FixedBits(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fixedBits')
	@FixedBits.setter
	def FixedBits(self, value):
		self._set_attribute('fixedBits', value)

	@property
	def FullMesh(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fullMesh')
	@FullMesh.setter
	def FullMesh(self, value):
		self._set_attribute('fullMesh', value)

	@property
	def Length(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Level(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('level')

	@property
	def MaxValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxValue')
	@MaxValue.setter
	def MaxValue(self, value):
		self._set_attribute('maxValue', value)

	@property
	def MinValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minValue')
	@MinValue.setter
	def MinValue(self, value):
		self._set_attribute('minValue', value)

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Offset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('offset')

	@property
	def OffsetFromRoot(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('offsetFromRoot')

	@property
	def OnTheFlyMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('onTheFlyMask')
	@OnTheFlyMask.setter
	def OnTheFlyMask(self, value):
		self._set_attribute('onTheFlyMask', value)

	@property
	def Optional(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('optional')

	@property
	def OptionalEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('optionalEnabled')
	@OptionalEnabled.setter
	def OptionalEnabled(self, value):
		self._set_attribute('optionalEnabled', value)

	@property
	def RandomMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('randomMask')
	@RandomMask.setter
	def RandomMask(self, value):
		self._set_attribute('randomMask', value)

	@property
	def RateVaried(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rateVaried')

	@property
	def ReadOnly(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('readOnly')

	@property
	def RequiresUdf(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('requiresUdf')

	@property
	def Seed(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('seed')
	@Seed.setter
	def Seed(self, value):
		self._set_attribute('seed', value)

	@property
	def SingleValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	@property
	def StartValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def StepValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('stepValue')
	@StepValue.setter
	def StepValue(self, value):
		self._set_attribute('stepValue', value)

	@property
	def SupportsNonRepeatableRandom(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsNonRepeatableRandom')

	@property
	def SupportsOnTheFlyMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsOnTheFlyMask')

	@property
	def TrackingEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('trackingEnabled')
	@TrackingEnabled.setter
	def TrackingEnabled(self, value):
		self._set_attribute('trackingEnabled', value)

	@property
	def ValueFormat(self):
		"""

		Returns:
			str(aTM|bool|debug|decimal|decimalFixed2|decimalSigned8|fCID|float|floatEng|hex|hex8WithColons|hex8WithSpaces|iPv4|iPv6|mAC|mACMAC|mACSiteId|mACVLAN|mACVLANSiteId|string|unknown|varLenHex)
		"""
		return self._get_attribute('valueFormat')

	@property
	def ValueList(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('valueList')
	@ValueList.setter
	def ValueList(self, value):
		self._set_attribute('valueList', value)

	@property
	def ValueType(self):
		"""

		Returns:
			str(decrement|increment|nonRepeatableRandom|random|repeatableRandomRange|singleValue|valueList)
		"""
		return self._get_attribute('valueType')
	@ValueType.setter
	def ValueType(self, value):
		self._set_attribute('valueType', value)

	def find(self, __id__=None, ActiveFieldChoice=None, Auto=None, CountValue=None, DefaultValue=None, DisplayName=None, EnumValues=None, FieldChoice=None, FieldTypeId=None, FieldValue=None, FixedBits=None, FullMesh=None, Length=None, Level=None, MaxValue=None, MinValue=None, Name=None, Offset=None, OffsetFromRoot=None, OnTheFlyMask=None, Optional=None, OptionalEnabled=None, RandomMask=None, RateVaried=None, ReadOnly=None, RequiresUdf=None, Seed=None, SingleValue=None, StartValue=None, StepValue=None, SupportsNonRepeatableRandom=None, SupportsOnTheFlyMask=None, TrackingEnabled=None, ValueFormat=None, ValueList=None, ValueType=None):
		"""Finds and retrieves field data from the server.

		All named parameters support regex and can be used to selectively retrieve field data from the server.
		By default the find method takes no parameters and will retrieve all field data from the server.

		Args:
			__id__ (str): 
			ActiveFieldChoice (bool): 
			Auto (bool): 
			CountValue (str): 
			DefaultValue (str): 
			DisplayName (str): 
			EnumValues (list(str)): 
			FieldChoice (bool): 
			FieldTypeId (str): 
			FieldValue (str): 
			FixedBits (str): 
			FullMesh (bool): 
			Length (number): 
			Level (bool): 
			MaxValue (str): 
			MinValue (str): 
			Name (str): 
			Offset (number): 
			OffsetFromRoot (number): 
			OnTheFlyMask (str): 
			Optional (bool): 
			OptionalEnabled (bool): 
			RandomMask (str): 
			RateVaried (bool): 
			ReadOnly (bool): 
			RequiresUdf (bool): 
			Seed (str): 
			SingleValue (str): 
			StartValue (str): 
			StepValue (str): 
			SupportsNonRepeatableRandom (bool): 
			SupportsOnTheFlyMask (bool): 
			TrackingEnabled (bool): 
			ValueFormat (str(aTM|bool|debug|decimal|decimalFixed2|decimalSigned8|fCID|float|floatEng|hex|hex8WithColons|hex8WithSpaces|iPv4|iPv6|mAC|mACMAC|mACSiteId|mACVLAN|mACVLANSiteId|string|unknown|varLenHex)): 
			ValueList (list(str)): 
			ValueType (str(decrement|increment|nonRepeatableRandom|random|repeatableRandomRange|singleValue|valueList)): 

		Returns:
			self: This instance with matching field data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of field data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the field data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddLevel(self):
		"""Executes the addLevel operation on the server.

		Add a level to the current field.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=field)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: The new level that has been added.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddLevel', payload=locals(), response_object=None)

	def RemoveLevel(self):
		"""Executes the removeLevel operation on the server.

		Remove a level.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=field)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveLevel', payload=locals(), response_object=None)
