from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AsSegment(Base):
	"""The AsSegment class encapsulates a required asSegment node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AsSegment property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'asSegment'

	def __init__(self, parent):
		super(AsSegment, self).__init__(parent)

	@property
	def AsSegments(self):
		"""Used to construct AS list related items.

		Returns:
			list(dict(arg1:bool,arg2:str[asSet|asSequence|asConfedSet|unknown|asConfedSequence],arg3:list[number]))
		"""
		return self._get_attribute('asSegments')
	@AsSegments.setter
	def AsSegments(self, value):
		self._set_attribute('asSegments', value)
