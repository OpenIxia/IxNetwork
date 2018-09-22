from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ImportTarget(Base):
	"""The ImportTarget class encapsulates a required importTarget node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ImportTarget property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'importTarget'

	def __init__(self, parent):
		super(ImportTarget, self).__init__(parent)

	@property
	def ImportTargetList(self):
		"""Configures a target attribute to be associated with advertised L3 VPN route ranges.

		Returns:
			list(dict(arg1:str[as|ip|asNumber2],arg2:number,arg3:str,arg4:number))
		"""
		return self._get_attribute('importTargetList')
	@ImportTargetList.setter
	def ImportTargetList(self, value):
		self._set_attribute('importTargetList', value)

	@property
	def ImportTargetListEx(self):
		"""Configures a list of export targets to be associated with advertised L3 VPN routeranges.

		Returns:
			list(dict(arg1:str[as|ip|asNumber2],arg2:number,arg3:str,arg4:number,arg5:number,arg6:number,arg7:str))
		"""
		return self._get_attribute('importTargetListEx')
	@ImportTargetListEx.setter
	def ImportTargetListEx(self, value):
		self._set_attribute('importTargetListEx', value)
