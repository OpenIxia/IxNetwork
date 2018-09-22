from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Prefix(Base):
	"""The Prefix class encapsulates a required prefix node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Prefix property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'prefix'

	def __init__(self, parent):
		super(Prefix, self).__init__(parent)

	@property
	def Prefix(self):
		"""Controls the prefix attributes that are filtered on.

		Returns:
			list(dict(arg1:str,arg2:bool,arg3:number,arg4:number))
		"""
		return self._get_attribute('prefix')
	@Prefix.setter
	def Prefix(self, value):
		self._set_attribute('prefix', value)
