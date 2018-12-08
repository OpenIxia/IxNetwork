
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


class Pos(Base):
	"""The Pos class encapsulates a required pos node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pos property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pos'

	def __init__(self, parent):
		super(Pos, self).__init__(parent)

	@property
	def Dcc(self):
		"""An instance of the Dcc class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.dcc.dcc.Dcc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.dcc.dcc import Dcc
		return Dcc(self)._select()

	@property
	def Ppp(self):
		"""An instance of the Ppp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.ppp.ppp.Ppp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.ppp.ppp import Ppp
		return Ppp(self)._select()

	@property
	def C2Expected(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('c2Expected')
	@C2Expected.setter
	def C2Expected(self, value):
		self._set_attribute('c2Expected', value)

	@property
	def C2Tx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('c2Tx')
	@C2Tx.setter
	def C2Tx(self, value):
		self._set_attribute('c2Tx', value)

	@property
	def CrcSize(self):
		"""

		Returns:
			str(crc16|crc32)
		"""
		return self._get_attribute('crcSize')
	@CrcSize.setter
	def CrcSize(self, value):
		self._set_attribute('crcSize', value)

	@property
	def DataScrambling(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('dataScrambling')
	@DataScrambling.setter
	def DataScrambling(self, value):
		self._set_attribute('dataScrambling', value)

	@property
	def EnablePPM(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def InterfaceType(self):
		"""

		Returns:
			str(oc12|oc192|oc3|oc48|stm1|stm16|stm4|stm64)
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Loopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def PayloadType(self):
		"""

		Returns:
			str(ciscoFrameRelay|ciscoHdlc|frameRelay|ppp)
		"""
		return self._get_attribute('payloadType')
	@PayloadType.setter
	def PayloadType(self, value):
		self._set_attribute('payloadType', value)

	@property
	def Ppm(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def TrafficMapType(self):
		"""

		Returns:
			str(dcc|spe)
		"""
		return self._get_attribute('trafficMapType')
	@TrafficMapType.setter
	def TrafficMapType(self, value):
		self._set_attribute('trafficMapType', value)

	@property
	def TransmitClocking(self):
		"""

		Returns:
			str(external|internal|recovered)
		"""
		return self._get_attribute('transmitClocking')
	@TransmitClocking.setter
	def TransmitClocking(self, value):
		self._set_attribute('transmitClocking', value)
