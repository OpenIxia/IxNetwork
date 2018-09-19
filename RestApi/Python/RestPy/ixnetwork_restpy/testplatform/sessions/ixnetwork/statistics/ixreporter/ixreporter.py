from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ixreporter(Base):
	"""The Ixreporter class encapsulates a required ixreporter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ixreporter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ixreporter'

	def __init__(self, parent):
		super(Ixreporter, self).__init__(parent)

	@property
	def DataCollection(self):
		"""An instance of the DataCollection class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.datacollection.datacollection.DataCollection)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.datacollection.datacollection import DataCollection
		return DataCollection(self)._select()

	@property
	def ReportGeneration(self):
		"""An instance of the ReportGeneration class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.reportgeneration.reportgeneration.ReportGeneration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.reportgeneration.reportgeneration import ReportGeneration
		return ReportGeneration(self)._select()
