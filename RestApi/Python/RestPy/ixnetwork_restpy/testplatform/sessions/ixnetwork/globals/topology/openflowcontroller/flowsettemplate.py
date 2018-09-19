from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowSetTemplate(Base):
	"""The FlowSetTemplate class encapsulates a required flowSetTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowSetTemplate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flowSetTemplate'

	def __init__(self, parent):
		super(FlowSetTemplate, self).__init__(parent)

	@property
	def FlowTemplate(self):
		"""An instance of the FlowTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.flowtemplate.FlowTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.flowtemplate import FlowTemplate
		return FlowTemplate(self)

	@property
	def Predefined(self):
		"""An instance of the Predefined class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.predefined.Predefined)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.predefined import Predefined
		return Predefined(self)
