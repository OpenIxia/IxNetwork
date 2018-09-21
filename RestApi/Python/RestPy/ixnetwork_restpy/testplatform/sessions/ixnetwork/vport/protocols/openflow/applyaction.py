from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ApplyAction(Base):
	"""The ApplyAction class encapsulates a required applyAction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ApplyAction property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'applyAction'

	def __init__(self, parent):
		super(ApplyAction, self).__init__(parent)

	@property
	def ApplyActionMissType(self):
		"""An instance of the ApplyActionMissType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionmisstype.ApplyActionMissType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactionmisstype import ApplyActionMissType
		return ApplyActionMissType(self)._select()

	@property
	def ApplyActionType(self):
		"""An instance of the ApplyActionType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactiontype.ApplyActionType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.applyactiontype import ApplyActionType
		return ApplyActionType(self)._select()

	@property
	def ExperimenterData(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDataLength(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')
	@ExperimenterDataLength.setter
	def ExperimenterDataLength(self, value):
		self._set_attribute('experimenterDataLength', value)

	@property
	def ExperimenterDataLengthMiss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLengthMiss')
	@ExperimenterDataLengthMiss.setter
	def ExperimenterDataLengthMiss(self, value):
		self._set_attribute('experimenterDataLengthMiss', value)

	@property
	def ExperimenterDataMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('experimenterDataMiss')
	@ExperimenterDataMiss.setter
	def ExperimenterDataMiss(self, value):
		self._set_attribute('experimenterDataMiss', value)

	@property
	def ExperimenterId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def ExperimenterIdMiss(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterIdMiss')
	@ExperimenterIdMiss.setter
	def ExperimenterIdMiss(self, value):
		self._set_attribute('experimenterIdMiss', value)
