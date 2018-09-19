from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ReportGeneration(Base):
	"""The ReportGeneration class encapsulates a required reportGeneration node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ReportGeneration property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'reportGeneration'

	def __init__(self, parent):
		super(ReportGeneration, self).__init__(parent)

	@property
	def OutputFile(self):
		"""Signifies the output file

		Returns:
			str
		"""
		return self._get_attribute('OutputFile')
	@OutputFile.setter
	def OutputFile(self, value):
		self._set_attribute('OutputFile', value)

	@property
	def OutputType(self):
		"""Signifies the output type

		Returns:
			str(Html|Pdf)
		"""
		return self._get_attribute('OutputType')
	@OutputType.setter
	def OutputType(self, value):
		self._set_attribute('OutputType', value)

	@property
	def Template(self):
		"""Signifies the template for IxReporter

		Returns:
			str
		"""
		return self._get_attribute('Template')
	@Template.setter
	def Template(self, value):
		self._set_attribute('Template', value)

	@property
	def TestRunId(self):
		"""Signifies the identifier for the test run

		Returns:
			number
		"""
		return self._get_attribute('TestRunId')
	@TestRunId.setter
	def TestRunId(self, value):
		self._set_attribute('TestRunId', value)

	def Start(self):
		"""Executes the start operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=reportGeneration)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)
