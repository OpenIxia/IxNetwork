from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ospf(Base):
	"""The Ospf class encapsulates a required ospf node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ospf property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ospf'

	def __init__(self, parent):
		super(Ospf, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.router import Router
		return Router(self)

	@property
	def EnableDrOrBdr(self):
		"""If true, enables this router as the Designated (DR) or Backup Designated Router (BDR).

		Returns:
			bool
		"""
		return self._get_attribute('enableDrOrBdr')
	@EnableDrOrBdr.setter
	def EnableDrOrBdr(self, value):
		self._set_attribute('enableDrOrBdr', value)

	@property
	def Enabled(self):
		"""Enables this emulated OSPF router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FloodLinkStateUpdatesPerInterval(self):
		"""Sets the number of Flood Link State Updates to be sent in each rate control interval.

		Returns:
			number
		"""
		return self._get_attribute('floodLinkStateUpdatesPerInterval')
	@FloodLinkStateUpdatesPerInterval.setter
	def FloodLinkStateUpdatesPerInterval(self, value):
		self._set_attribute('floodLinkStateUpdatesPerInterval', value)

	@property
	def RateControlInterval(self):
		"""Enables the option Rate Control Interval to define a value.

		Returns:
			number
		"""
		return self._get_attribute('rateControlInterval')
	@RateControlInterval.setter
	def RateControlInterval(self, value):
		self._set_attribute('rateControlInterval', value)

	@property
	def RunningState(self):
		"""The current state of the OSPF router.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def Start(self):
		"""Executes the start operation on the server.

		Starts the OSPF protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospf)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the MLD protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospf)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
