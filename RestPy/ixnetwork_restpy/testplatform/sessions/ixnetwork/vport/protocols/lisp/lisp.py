
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			number
		"""
		return self._get_attribute('burstIntervalInMs')
	@BurstIntervalInMs.setter
	def BurstIntervalInMs(self, value):
		self._set_attribute('burstIntervalInMs', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Ipv4MapRegisterPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRegisterPacketsPerBurst')
	@Ipv4MapRegisterPacketsPerBurst.setter
	def Ipv4MapRegisterPacketsPerBurst(self, value):
		self._set_attribute('ipv4MapRegisterPacketsPerBurst', value)

	@property
	def Ipv4MapRequestPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRequestPacketsPerBurst')
	@Ipv4MapRequestPacketsPerBurst.setter
	def Ipv4MapRequestPacketsPerBurst(self, value):
		self._set_attribute('ipv4MapRequestPacketsPerBurst', value)

	@property
	def Ipv4SmrPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4SmrPacketsPerBurst')
	@Ipv4SmrPacketsPerBurst.setter
	def Ipv4SmrPacketsPerBurst(self, value):
		self._set_attribute('ipv4SmrPacketsPerBurst', value)

	@property
	def Ipv6MapRegisterPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRegisterPacketsPerBurst')
	@Ipv6MapRegisterPacketsPerBurst.setter
	def Ipv6MapRegisterPacketsPerBurst(self, value):
		self._set_attribute('ipv6MapRegisterPacketsPerBurst', value)

	@property
	def Ipv6MapRequestPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRequestPacketsPerBurst')
	@Ipv6MapRequestPacketsPerBurst.setter
	def Ipv6MapRequestPacketsPerBurst(self, value):
		self._set_attribute('ipv6MapRequestPacketsPerBurst', value)

	@property
	def Ipv6SmrPacketsPerBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6SmrPacketsPerBurst')
	@Ipv6SmrPacketsPerBurst.setter
	def Ipv6SmrPacketsPerBurst(self, value):
		self._set_attribute('ipv6SmrPacketsPerBurst', value)

	@property
	def ProtocolState(self):
		"""

		Returns:
			str(stopped|unknown|stopping|started|starting)
		"""
		return self._get_attribute('protocolState')

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lisp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lisp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
