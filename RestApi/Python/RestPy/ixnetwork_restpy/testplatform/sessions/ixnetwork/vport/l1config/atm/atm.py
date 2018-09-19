from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Atm(Base):
	"""The Atm class encapsulates a required atm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Atm property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'atm'

	def __init__(self, parent):
		super(Atm, self).__init__(parent)

	@property
	def C2Expected(self):
		"""The expected value of the C2 byte in the received path overhead. Typically, this will match the value in the Transmit field. For ATM, the expected value is 0x13 (Hex).

		Returns:
			number
		"""
		return self._get_attribute('c2Expected')
	@C2Expected.setter
	def C2Expected(self, value):
		self._set_attribute('c2Expected', value)

	@property
	def C2Tx(self):
		"""The value of the C2 byte in the transmitted path overhead. For ATM, the transmitted value is 0x13 (Hex).

		Returns:
			number
		"""
		return self._get_attribute('c2Tx')
	@C2Tx.setter
	def C2Tx(self, value):
		self._set_attribute('c2Tx', value)

	@property
	def CellHeader(self):
		"""user/network-to-network interface

		Returns:
			str(nni|uni)
		"""
		return self._get_attribute('cellHeader')
	@CellHeader.setter
	def CellHeader(self, value):
		self._set_attribute('cellHeader', value)

	@property
	def CosetActive(self):
		"""CRC + Exclusive OR Operation

		Returns:
			bool
		"""
		return self._get_attribute('cosetActive')
	@CosetActive.setter
	def CosetActive(self, value):
		self._set_attribute('cosetActive', value)

	@property
	def CrcSize(self):
		"""Choose the type of Cyclic Redundancy Check to be used.

		Returns:
			str(crc16|crc32)
		"""
		return self._get_attribute('crcSize')
	@CrcSize.setter
	def CrcSize(self, value):
		self._set_attribute('crcSize', value)

	@property
	def DataScrambling(self):
		"""If enabled, data is scrambled with the x43 + 1 polynomial. Note: The ATM cell header is not scrambled.

		Returns:
			bool
		"""
		return self._get_attribute('dataScrambling')
	@DataScrambling.setter
	def DataScrambling(self, value):
		self._set_attribute('dataScrambling', value)

	@property
	def EnablePPM(self):
		"""If true, enables the portsppm.

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def FillerCell(self):
		"""SONET frame transmission is continuous even when data or control messages are not being transmitted. Choose the ATM cell type to be transmitted during those intervals.

		Returns:
			str(idle|unassigned)
		"""
		return self._get_attribute('fillerCell')
	@FillerCell.setter
	def FillerCell(self, value):
		self._set_attribute('fillerCell', value)

	@property
	def InterfaceType(self):
		"""The interface type for ATM.

		Returns:
			str(oc12|oc3|stm1|stm4)
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
	def PatternMatching(self):
		"""Used to enable capture/filter values for use with ATM ports. When enabled, the frame data from one or more VPI/VCIs may be used as capture trigger or capture filter option.

		Returns:
			bool
		"""
		return self._get_attribute('patternMatching')
	@PatternMatching.setter
	def PatternMatching(self, value):
		self._set_attribute('patternMatching', value)

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
	def ReassemblyTimeout(self):
		"""Sets the value for the Reassembly Timeout. It is the period of time that the receive side will wait for another cell on that channel - for reassembly of cells into a CPCS PDU (packet). If no cell is received within that period, the timer will expire. (in hex)

		Returns:
			number
		"""
		return self._get_attribute('reassemblyTimeout')
	@ReassemblyTimeout.setter
	def ReassemblyTimeout(self, value):
		self._set_attribute('reassemblyTimeout', value)

	@property
	def TransmitClocking(self):
		"""The options for the transmit clock.

		Returns:
			str(external|internal|recovered)
		"""
		return self._get_attribute('transmitClocking')
	@TransmitClocking.setter
	def TransmitClocking(self, value):
		self._set_attribute('transmitClocking', value)
