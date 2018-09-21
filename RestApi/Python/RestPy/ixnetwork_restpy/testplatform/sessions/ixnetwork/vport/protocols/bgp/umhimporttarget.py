from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UmhImportTarget(Base):
	"""The UmhImportTarget class encapsulates a required umhImportTarget node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UmhImportTarget property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'umhImportTarget'

	def __init__(self, parent):
		super(UmhImportTarget, self).__init__(parent)

	@property
	def ImportTargetList(self):
		"""Configures import route target in case of UMH routes

		Returns:
			list(dict(arg1:str[as|asNumber2|ip],arg2:number,arg3:str,arg4:number,arg5:number,arg6:number,arg7:str))
		"""
		return self._get_attribute('importTargetList')
	@ImportTargetList.setter
	def ImportTargetList(self, value):
		self._set_attribute('importTargetList', value)
