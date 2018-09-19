from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ActionsTemplate(Base):
	"""The ActionsTemplate class encapsulates a required actionsTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ActionsTemplate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'actionsTemplate'

	def __init__(self, parent):
		super(ActionsTemplate, self).__init__(parent)

	@property
	def ActionTemplate(self):
		"""An instance of the ActionTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.actiontemplate.ActionTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.actiontemplate import ActionTemplate
		return ActionTemplate(self)

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
