from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Lisp(Base):
	"""The Lisp class encapsulates a required lisp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Lisp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'lisp'

	def __init__(self, parent):
		super(Lisp, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.router import Router
		return Router(self)

	@property
	def SiteEidRange(self):
		"""An instance of the SiteEidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.siteeidrange.siteeidrange.SiteEidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.siteeidrange.siteeidrange import SiteEidRange
		return SiteEidRange(self)

	@property
	def BurstIntervalInMs(self):
		"""It shows the details abou the burst interval in micro seconds

		Returns:
			number
		"""
		return self._get_attribute('burstIntervalInMs')
	@BurstIntervalInMs.setter
	def BurstIntervalInMs(self, value):
		self._set_attribute('burstIntervalInMs', value)

	@property
	def Enabled(self):
		"""If true, it shows enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Ipv4MapRegisterPacketsPerBurst(self):
		"""It gives details about the ip v4 map register packets per burst

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRegisterPacketsPerBurst')
	@Ipv4MapRegisterPacketsPerBurst.setter
	def Ipv4MapRegisterPacketsPerBurst(self, value):
		self._set_attribute('ipv4MapRegisterPacketsPerBurst', value)

	@property
	def Ipv4MapRequestPacketsPerBurst(self):
		"""It gives details about the ip v4 map requests packets per burst

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRequestPacketsPerBurst')
	@Ipv4MapRequestPacketsPerBurst.setter
	def Ipv4MapRequestPacketsPerBurst(self, value):
		self._set_attribute('ipv4MapRequestPacketsPerBurst', value)

	@property
	def Ipv4SmrPacketsPerBurst(self):
		"""It gives details about the Ip v4 Smr packets per bursts

		Returns:
			number
		"""
		return self._get_attribute('ipv4SmrPacketsPerBurst')
	@Ipv4SmrPacketsPerBurst.setter
	def Ipv4SmrPacketsPerBurst(self, value):
		self._set_attribute('ipv4SmrPacketsPerBurst', value)

	@property
	def Ipv6MapRegisterPacketsPerBurst(self):
		"""It gives details about the ip v6 map register packets per burst

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRegisterPacketsPerBurst')
	@Ipv6MapRegisterPacketsPerBurst.setter
	def Ipv6MapRegisterPacketsPerBurst(self, value):
		self._set_attribute('ipv6MapRegisterPacketsPerBurst', value)

	@property
	def Ipv6MapRequestPacketsPerBurst(self):
		"""It gives details about the ip v6 map requests packets per burst

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRequestPacketsPerBurst')
	@Ipv6MapRequestPacketsPerBurst.setter
	def Ipv6MapRequestPacketsPerBurst(self, value):
		self._set_attribute('ipv6MapRequestPacketsPerBurst', value)

	@property
	def Ipv6SmrPacketsPerBurst(self):
		"""It gives details about the Ip v6 Smr packets per bursts

		Returns:
			number
		"""
		return self._get_attribute('ipv6SmrPacketsPerBurst')
	@Ipv6SmrPacketsPerBurst.setter
	def Ipv6SmrPacketsPerBurst(self, value):
		self._set_attribute('ipv6SmrPacketsPerBurst', value)

	@property
	def ProtocolState(self):
		"""Shows different protocol states (read-only)

		Returns:
			str(stopped|unknown|stopping|started|starting)
		"""
		return self._get_attribute('protocolState')

	def Start(self):
		"""Executes the start operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lisp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lisp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
