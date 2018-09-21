from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchGroupFeature(Base):
	"""The SwitchGroupFeature class encapsulates a system managed switchGroupFeature node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchGroupFeature property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchGroupFeature'

	def __init__(self, parent):
		super(SwitchGroupFeature, self).__init__(parent)

	@property
	def ApplyGroup(self):
		"""If selected, table supports Apply Group capability.

		Returns:
			bool
		"""
		return self._get_attribute('applyGroup')
	@ApplyGroup.setter
	def ApplyGroup(self, value):
		self._set_attribute('applyGroup', value)

	@property
	def CopyTtlIn(self):
		"""If selected, table supports Copy TTL In capability.

		Returns:
			bool
		"""
		return self._get_attribute('copyTtlIn')
	@CopyTtlIn.setter
	def CopyTtlIn(self, value):
		self._set_attribute('copyTtlIn', value)

	@property
	def CopyTtlOut(self):
		"""If selected, table supports Copy TTL capability.

		Returns:
			bool
		"""
		return self._get_attribute('copyTtlOut')
	@CopyTtlOut.setter
	def CopyTtlOut(self, value):
		self._set_attribute('copyTtlOut', value)

	@property
	def DecrementMplsTtl(self):
		"""If selected, table supports Decrement MPLS TTL capability.

		Returns:
			bool
		"""
		return self._get_attribute('decrementMplsTtl')
	@DecrementMplsTtl.setter
	def DecrementMplsTtl(self, value):
		self._set_attribute('decrementMplsTtl', value)

	@property
	def DecrementNetworkTtl(self):
		"""If selected, table supports Decrement Network TTL capability.

		Returns:
			bool
		"""
		return self._get_attribute('decrementNetworkTtl')
	@DecrementNetworkTtl.setter
	def DecrementNetworkTtl(self, value):
		self._set_attribute('decrementNetworkTtl', value)

	@property
	def GroupType(self):
		"""The type of group. (This type is selected in the Switches window.)

		Returns:
			str(allGroup|selectGroup|indirectGroup|fastFailoverGroup)
		"""
		return self._get_attribute('groupType')

	@property
	def MaxNoOfGroups(self):
		"""Specify the maximum number of groups supported per switch group type.

		Returns:
			number
		"""
		return self._get_attribute('maxNoOfGroups')
	@MaxNoOfGroups.setter
	def MaxNoOfGroups(self, value):
		self._set_attribute('maxNoOfGroups', value)

	@property
	def Output(self):
		"""If selected, table supports Output capability.

		Returns:
			bool
		"""
		return self._get_attribute('output')
	@Output.setter
	def Output(self, value):
		self._set_attribute('output', value)

	@property
	def PopMpls(self):
		"""If selected, table supports Pop MPLS capability.

		Returns:
			bool
		"""
		return self._get_attribute('popMpls')
	@PopMpls.setter
	def PopMpls(self, value):
		self._set_attribute('popMpls', value)

	@property
	def PopPbb(self):
		"""If selected, table supports Experimenter capability.

		Returns:
			bool
		"""
		return self._get_attribute('popPbb')
	@PopPbb.setter
	def PopPbb(self, value):
		self._set_attribute('popPbb', value)

	@property
	def PopVlan(self):
		"""If selected, table supports Pop VLAN capability.

		Returns:
			bool
		"""
		return self._get_attribute('popVlan')
	@PopVlan.setter
	def PopVlan(self, value):
		self._set_attribute('popVlan', value)

	@property
	def PushMpls(self):
		"""If selected, table supports Push MPLS capability.

		Returns:
			bool
		"""
		return self._get_attribute('pushMpls')
	@PushMpls.setter
	def PushMpls(self, value):
		self._set_attribute('pushMpls', value)

	@property
	def PushPbb(self):
		"""If selected, table supports Push PBB capability.

		Returns:
			bool
		"""
		return self._get_attribute('pushPbb')
	@PushPbb.setter
	def PushPbb(self, value):
		self._set_attribute('pushPbb', value)

	@property
	def PushVlan(self):
		"""If selected, table supports Push VLAN capability.

		Returns:
			bool
		"""
		return self._get_attribute('pushVlan')
	@PushVlan.setter
	def PushVlan(self, value):
		self._set_attribute('pushVlan', value)

	@property
	def SetField(self):
		"""If selected, table supports Set Field capability.

		Returns:
			bool
		"""
		return self._get_attribute('setField')
	@SetField.setter
	def SetField(self, value):
		self._set_attribute('setField', value)

	@property
	def SetMplsTtl(self):
		"""If selected, table supports Set MPLS TTL capability.

		Returns:
			bool
		"""
		return self._get_attribute('setMplsTtl')
	@SetMplsTtl.setter
	def SetMplsTtl(self, value):
		self._set_attribute('setMplsTtl', value)

	@property
	def SetNetworkTtl(self):
		"""If selected, table supports Set Network TTL capability.

		Returns:
			bool
		"""
		return self._get_attribute('setNetworkTtl')
	@SetNetworkTtl.setter
	def SetNetworkTtl(self, value):
		self._set_attribute('setNetworkTtl', value)

	@property
	def SetQueue(self):
		"""If selected, table supports Set Queue capability.

		Returns:
			bool
		"""
		return self._get_attribute('setQueue')
	@SetQueue.setter
	def SetQueue(self, value):
		self._set_attribute('setQueue', value)

	def find(self, ApplyGroup=None, CopyTtlIn=None, CopyTtlOut=None, DecrementMplsTtl=None, DecrementNetworkTtl=None, GroupType=None, MaxNoOfGroups=None, Output=None, PopMpls=None, PopPbb=None, PopVlan=None, PushMpls=None, PushPbb=None, PushVlan=None, SetField=None, SetMplsTtl=None, SetNetworkTtl=None, SetQueue=None):
		"""Finds and retrieves switchGroupFeature data from the server.

		All named parameters support regex and can be used to selectively retrieve switchGroupFeature data from the server.
		By default the find method takes no parameters and will retrieve all switchGroupFeature data from the server.

		Args:
			ApplyGroup (bool): If selected, table supports Apply Group capability.
			CopyTtlIn (bool): If selected, table supports Copy TTL In capability.
			CopyTtlOut (bool): If selected, table supports Copy TTL capability.
			DecrementMplsTtl (bool): If selected, table supports Decrement MPLS TTL capability.
			DecrementNetworkTtl (bool): If selected, table supports Decrement Network TTL capability.
			GroupType (str(allGroup|selectGroup|indirectGroup|fastFailoverGroup)): The type of group. (This type is selected in the Switches window.)
			MaxNoOfGroups (number): Specify the maximum number of groups supported per switch group type.
			Output (bool): If selected, table supports Output capability.
			PopMpls (bool): If selected, table supports Pop MPLS capability.
			PopPbb (bool): If selected, table supports Experimenter capability.
			PopVlan (bool): If selected, table supports Pop VLAN capability.
			PushMpls (bool): If selected, table supports Push MPLS capability.
			PushPbb (bool): If selected, table supports Push PBB capability.
			PushVlan (bool): If selected, table supports Push VLAN capability.
			SetField (bool): If selected, table supports Set Field capability.
			SetMplsTtl (bool): If selected, table supports Set MPLS TTL capability.
			SetNetworkTtl (bool): If selected, table supports Set Network TTL capability.
			SetQueue (bool): If selected, table supports Set Queue capability.

		Returns:
			self: This instance with matching switchGroupFeature data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchGroupFeature data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchGroupFeature data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
