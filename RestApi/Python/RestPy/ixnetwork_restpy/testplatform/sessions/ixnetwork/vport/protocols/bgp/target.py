from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Target(Base):
	"""The Target class encapsulates a required target node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Target property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'target'

	def __init__(self, parent):
		super(Target, self).__init__(parent)

	@property
	def TargetList(self):
		"""Configures a target attribute to be associated with advertised L3 VPN route ranges.

		Returns:
			list(dict(arg1:str[as|ip|asNumber2],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('targetList')
	@TargetList.setter
	def TargetList(self, value):
		self._set_attribute('targetList', value)

	@property
	def TargetListEx(self):
		"""Configures a list of export targets to be associated with advertised L3 VPN route ranges.

		Returns:
			list(dict(arg1:str[as|ip|asNumber2],arg2:number,arg3:str,arg4:number,arg5:number,arg6:number,arg7:str))
		"""
		return self._get_attribute('targetListEx')
	@TargetListEx.setter
	def TargetListEx(self, value):
		self._set_attribute('targetListEx', value)
