from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Pcc(Base):
	"""The Pcc class encapsulates a required pcc node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pcc property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pcc'

	def __init__(self, parent):
		super(Pcc, self).__init__(parent)

	@property
	def BackupPCEOperationMode(self):
		"""Backup PCE Operation Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupPCEOperationMode')

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
	def LspDelegationDelay(self):
		"""Time in seconds before PCC distributes LSP delegation at startup.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspDelegationDelay')

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
	def PcePathComputationMode(self):
		"""PCE Path Computation Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pcePathComputationMode')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')
