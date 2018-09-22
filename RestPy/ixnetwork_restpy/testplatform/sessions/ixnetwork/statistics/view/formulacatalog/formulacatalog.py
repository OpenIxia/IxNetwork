from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FormulaCatalog(Base):
	"""The FormulaCatalog class encapsulates a required formulaCatalog node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FormulaCatalog property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'formulaCatalog'

	def __init__(self, parent):
		super(FormulaCatalog, self).__init__(parent)

	@property
	def FormulaColumn(self):
		"""An instance of the FormulaColumn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn.FormulaColumn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacolumn.formulacolumn import FormulaColumn
		return FormulaColumn(self)
