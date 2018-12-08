
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


class Rsvp(Base):
	"""The Rsvp class encapsulates a required rsvp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Rsvp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rsvp'

	def __init__(self, parent):
		super(Rsvp, self).__init__(parent)

	@property
	def NeighborPair(self):
		"""An instance of the NeighborPair class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.neighborpair.NeighborPair)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.neighborpair import NeighborPair
		return NeighborPair(self)

	@property
	def EnableBgpOverLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBgpOverLsp')
	@EnableBgpOverLsp.setter
	def EnableBgpOverLsp(self, value):
		self._set_attribute('enableBgpOverLsp', value)

	@property
	def EnableControlLspInitiationRate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableControlLspInitiationRate')
	@EnableControlLspInitiationRate.setter
	def EnableControlLspInitiationRate(self, value):
		self._set_attribute('enableControlLspInitiationRate', value)

	@property
	def EnableShowTimeValue(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableShowTimeValue')
	@EnableShowTimeValue.setter
	def EnableShowTimeValue(self, value):
		self._set_attribute('enableShowTimeValue', value)

	@property
	def EnableVpnLabelExchangeOverLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVpnLabelExchangeOverLsp')
	@EnableVpnLabelExchangeOverLsp.setter
	def EnableVpnLabelExchangeOverLsp(self, value):
		self._set_attribute('enableVpnLabelExchangeOverLsp', value)

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
	def MaxLspInitiationsPerSec(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxLspInitiationsPerSec')
	@MaxLspInitiationsPerSec.setter
	def MaxLspInitiationsPerSec(self, value):
		self._set_attribute('maxLspInitiationsPerSec', value)

	@property
	def RunningState(self):
		"""

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def UseTransportLabelsForMplsOam(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useTransportLabelsForMplsOam')
	@UseTransportLabelsForMplsOam.setter
	def UseTransportLabelsForMplsOam(self, value):
		self._set_attribute('useTransportLabelsForMplsOam', value)

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=rsvp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=rsvp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
