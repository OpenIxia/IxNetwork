from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Unconnected(Base):
	"""The Unconnected class encapsulates a required unconnected node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Unconnected property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'unconnected'

	def __init__(self, parent):
		super(Unconnected, self).__init__(parent)

	@property
	def ConnectedVia(self):
		"""The name of a specified connected protocol interface on the link that is directly connected to the DUT.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)
