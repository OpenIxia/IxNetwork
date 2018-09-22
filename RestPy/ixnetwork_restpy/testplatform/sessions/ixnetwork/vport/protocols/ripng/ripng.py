from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ripng(Base):
	"""The Ripng class encapsulates a required ripng node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ripng property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ripng'

	def __init__(self, parent):
		super(Ripng, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.router import Router
		return Router(self)

	@property
	def Enabled(self):
		"""Enables this particular protocol interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def NumRoutes(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numRoutes')
	@NumRoutes.setter
	def NumRoutes(self, value):
		self._set_attribute('numRoutes', value)

	@property
	def RunningState(self):
		"""The current running state of the RIPng router.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def TimePeriod(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('timePeriod')
	@TimePeriod.setter
	def TimePeriod(self, value):
		self._set_attribute('timePeriod', value)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the RIPng protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ripng)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the RIPng protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ripng)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
