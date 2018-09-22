from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class WriteActionMissType(Base):
	"""The WriteActionMissType class encapsulates a required writeActionMissType node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the WriteActionMissType property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'writeActionMissType'

	def __init__(self, parent):
		super(WriteActionMissType, self).__init__(parent)

	@property
	def CopyTtlIn(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('copyTtlIn')
	@CopyTtlIn.setter
	def CopyTtlIn(self, value):
		self._set_attribute('copyTtlIn', value)

	@property
	def CopyTtlOut(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('copyTtlOut')
	@CopyTtlOut.setter
	def CopyTtlOut(self, value):
		self._set_attribute('copyTtlOut', value)

	@property
	def DecrementMplsTtl(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('decrementMplsTtl')
	@DecrementMplsTtl.setter
	def DecrementMplsTtl(self, value):
		self._set_attribute('decrementMplsTtl', value)

	@property
	def DecrementNetworkTtl(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('decrementNetworkTtl')
	@DecrementNetworkTtl.setter
	def DecrementNetworkTtl(self, value):
		self._set_attribute('decrementNetworkTtl', value)

	@property
	def Experimenter(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def Group(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('group')
	@Group.setter
	def Group(self, value):
		self._set_attribute('group', value)

	@property
	def Output(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('output')
	@Output.setter
	def Output(self, value):
		self._set_attribute('output', value)

	@property
	def PopMpls(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('popMpls')
	@PopMpls.setter
	def PopMpls(self, value):
		self._set_attribute('popMpls', value)

	@property
	def PopPbb(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('popPbb')
	@PopPbb.setter
	def PopPbb(self, value):
		self._set_attribute('popPbb', value)

	@property
	def PopVlan(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('popVlan')
	@PopVlan.setter
	def PopVlan(self, value):
		self._set_attribute('popVlan', value)

	@property
	def PushMpls(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('pushMpls')
	@PushMpls.setter
	def PushMpls(self, value):
		self._set_attribute('pushMpls', value)

	@property
	def PushPbb(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('pushPbb')
	@PushPbb.setter
	def PushPbb(self, value):
		self._set_attribute('pushPbb', value)

	@property
	def PushVlan(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('pushVlan')
	@PushVlan.setter
	def PushVlan(self, value):
		self._set_attribute('pushVlan', value)

	@property
	def SetField(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('setField')
	@SetField.setter
	def SetField(self, value):
		self._set_attribute('setField', value)

	@property
	def SetMplsTtl(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('setMplsTtl')
	@SetMplsTtl.setter
	def SetMplsTtl(self, value):
		self._set_attribute('setMplsTtl', value)

	@property
	def SetNetworkTtl(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('setNetworkTtl')
	@SetNetworkTtl.setter
	def SetNetworkTtl(self, value):
		self._set_attribute('setNetworkTtl', value)

	@property
	def SetQueue(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('setQueue')
	@SetQueue.setter
	def SetQueue(self, value):
		self._set_attribute('setQueue', value)
