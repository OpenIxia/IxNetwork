from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PortStatusMaskSlave(Base):
	"""The PortStatusMaskSlave class encapsulates a required portStatusMaskSlave node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortStatusMaskSlave property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'portStatusMaskSlave'

	def __init__(self, parent):
		super(PortStatusMaskSlave, self).__init__(parent)

	@property
	def PortAdd(self):
		"""This indicates that a port is added.

		Returns:
			bool
		"""
		return self._get_attribute('portAdd')
	@PortAdd.setter
	def PortAdd(self, value):
		self._set_attribute('portAdd', value)

	@property
	def PortDelete(self):
		"""This indicates that a port is removed.

		Returns:
			bool
		"""
		return self._get_attribute('portDelete')
	@PortDelete.setter
	def PortDelete(self, value):
		self._set_attribute('portDelete', value)

	@property
	def PortModify(self):
		"""This indicates that some attributes of the port is changed.

		Returns:
			bool
		"""
		return self._get_attribute('portModify')
	@PortModify.setter
	def PortModify(self, value):
		self._set_attribute('portModify', value)
