from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FieldOffset(Base):
	"""The FieldOffset class encapsulates a required fieldOffset node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FieldOffset property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'fieldOffset'

	def __init__(self, parent):
		super(FieldOffset, self).__init__(parent)

	@property
	def Stack(self):
		"""An instance of the Stack class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.stack.stack.Stack)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.stack.stack import Stack
		return Stack(self)
