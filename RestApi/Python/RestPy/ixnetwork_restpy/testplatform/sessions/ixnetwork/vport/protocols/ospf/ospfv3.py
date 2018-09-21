from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OspfV3(Base):
	"""The OspfV3 class encapsulates a required ospfV3 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OspfV3 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ospfV3'

	def __init__(self, parent):
		super(OspfV3, self).__init__(parent)

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
		"""Enables the OSPF Router to participate in DR/BDR election process

		Returns:
			bool
		"""
		return self._get_attribute('enableDrOrBdr')
	@EnableDrOrBdr.setter
	def EnableDrOrBdr(self, value):
		self._set_attribute('enableDrOrBdr', value)

	@property
	def Enabled(self):
		"""Enables this emulated OSPFv3 router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RunningState(self):
		"""The current state of the OSPFv6 router.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def GracefulRouterRestart(self, Arg2):
		"""Executes the gracefulRouterRestart operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospfV3)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router])): NOT DEFINED

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GracefulRouterRestart', payload=locals(), response_object=None)

	def GracefulRouterRestart(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the gracefulRouterRestart operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospfV3)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router])): NOT DEFINED
			Arg3 (number): NOT DEFINED
			Arg4 (str(softwareReloadOrUpgrade|softwareRestart|switchToRedundantControlProcessor|unknown)): NOT DEFINED
			Arg5 (number): NOT DEFINED

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GracefulRouterRestart', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Starts the OSPFv3 protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospfV3)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the OSPFv3 protocol on a port or group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ospfV3)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
