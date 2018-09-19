from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ixnet(Base):
	"""The Ixnet class encapsulates a required ixnet node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ixnet property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ixnet'

	def __init__(self, parent):
		super(Ixnet, self).__init__(parent)

	@property
	def ConnectedClients(self):
		"""Returns the remote address and remote port for each of the currently connected ixNet clients.

		Returns:
			list(str)
		"""
		return self._get_attribute('connectedClients')

	@property
	def IsActive(self):
		"""Returns true if any remote clients are connected, false if no remote clients are connected.

		Returns:
			bool
		"""
		return self._get_attribute('isActive')
