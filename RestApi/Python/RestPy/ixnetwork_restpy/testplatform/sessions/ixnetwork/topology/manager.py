from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Manager(Base):
	"""The Manager class encapsulates a required manager node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Manager property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'manager'

	def __init__(self, parent):
		super(Manager, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def ManagerActive(self):
		"""Enable Manager

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('managerActive')

	@property
	def ManagerIp(self):
		"""IPv4 Address of the Manager

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('managerIp')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def TcpPort(self):
		"""Specify the TCP port for the Manager

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpPort')
