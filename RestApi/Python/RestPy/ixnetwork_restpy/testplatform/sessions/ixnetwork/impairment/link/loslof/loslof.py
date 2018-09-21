from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LosLof(Base):
	"""The LosLof class encapsulates a required losLof node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LosLof property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'losLof'

	def __init__(self, parent):
		super(LosLof, self).__init__(parent)

	@property
	def Duration(self):
		"""The burst duration.

		Returns:
			number
		"""
		return self._get_attribute('duration')
	@Duration.setter
	def Duration(self, value):
		self._set_attribute('duration', value)

	@property
	def IsBurst(self):
		"""If true, loss of signal or loss of frame will be enabled for the specified duration.

		Returns:
			bool
		"""
		return self._get_attribute('isBurst')
	@IsBurst.setter
	def IsBurst(self, value):
		self._set_attribute('isBurst', value)

	@property
	def State(self):
		"""Gets the loss of signal or loss of framing state.

		Returns:
			str(started|stopped)
		"""
		return self._get_attribute('state')

	@property
	def Type(self):
		"""Selects loss of signal or loss of framing.

		Returns:
			str(lof|los)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Units(self):
		"""Burst duration units.

		Returns:
			str(kMicroseconds|kMilliseconds|kSeconds|microseconds|milliseconds|seconds)
		"""
		return self._get_attribute('units')
	@Units.setter
	def Units(self, value):
		self._set_attribute('units', value)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the impairments defined by user (traffic will be impaired).

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/impairment?deepchild=losLof)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the impairments defined by user (traffic will pass unimpaired).

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/impairment?deepchild=losLof)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
