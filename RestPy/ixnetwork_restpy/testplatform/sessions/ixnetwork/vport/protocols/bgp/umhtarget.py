from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UmhTarget(Base):
	"""The UmhTarget class encapsulates a required umhTarget node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UmhTarget property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'umhTarget'

	def __init__(self, parent):
		super(UmhTarget, self).__init__(parent)

	@property
	def TargetList(self):
		"""Configures a route target to be exported while advertising UMH routes

		Returns:
			list(dict(arg1:str[asNumber2|as|ip],arg2:number,arg3:str,arg4:number,arg5:number,arg6:number,arg7:str))
		"""
		return self._get_attribute('targetList')
	@TargetList.setter
	def TargetList(self, value):
		self._set_attribute('targetList', value)
