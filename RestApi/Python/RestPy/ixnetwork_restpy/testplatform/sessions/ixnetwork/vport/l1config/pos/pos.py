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
		"""C2 Byte

		Returns:
			number
		"""
		return self._get_attribute('c2Expected')
	@C2Expected.setter
	def C2Expected(self, value):
		self._set_attribute('c2Expected', value)

	@property
	def C2Tx(self):
		"""C2 Byte

		Returns:
			number
		"""
		return self._get_attribute('c2Tx')
	@C2Tx.setter
	def C2Tx(self, value):
		self._set_attribute('c2Tx', value)

	@property
	def CrcSize(self):
		"""The type of cyclic redundancy check (CRC) to be used.

		Returns:
			str(crc16|crc32)
		"""
		return self._get_attribute('crcSize')
	@CrcSize.setter
	def CrcSize(self, value):
		self._set_attribute('crcSize', value)

	@property
	def DataScrambling(self):
		"""Data scrambling is enabled on this POS port.

		Returns:
			bool
		"""
		return self._get_attribute('dataScrambling')
	@DataScrambling.setter
	def DataScrambling(self, value):
		self._set_attribute('dataScrambling', value)

	@property
	def EnablePPM(self):
		"""If true, enables the portsppm

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def InterfaceType(self):
		"""The POS interface type for the port.

		Returns:
			str(oc12|oc192|oc3|oc48|stm1|stm16|stm4|stm64)
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Loopback(self):
		"""If enabled, the port is set to internally loopback from transmit to receive.

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def PayloadType(self):
		"""The POS payload type.

		Returns:
			str(ciscoFrameRelay|ciscoHdlc|frameRelay|ppp)
		"""
		return self._get_attribute('payloadType')
	@PayloadType.setter
	def PayloadType(self, value):
		self._set_attribute('payloadType', value)

	@property
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency.

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def TrafficMapType(self):
		"""The POS traffic map type.

		Returns:
			str(dcc|spe)
		"""
		return self._get_attribute('trafficMapType')
	@TrafficMapType.setter
	def TrafficMapType(self, value):
		self._set_attribute('trafficMapType', value)

	@property
	def TransmitClocking(self):
		"""The POS transmit clocking type.

		Returns:
			str(external|internal|recovered)
		"""
		return self._get_attribute('transmitClocking')
	@TransmitClocking.setter
	def TransmitClocking(self, value):
		self._set_attribute('transmitClocking', value)
