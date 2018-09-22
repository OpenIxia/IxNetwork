from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TenGigWan(Base):
	"""The TenGigWan class encapsulates a required tenGigWan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TenGigWan property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'tenGigWan'

	def __init__(self, parent):
		super(TenGigWan, self).__init__(parent)

	@property
	def Fcoe(self):
		"""An instance of the Fcoe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.fcoe.fcoe import Fcoe
		return Fcoe(self)._select()

	@property
	def TxLane(self):
		"""An instance of the TxLane class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.txlane.txlane.TxLane)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.txlane.txlane import TxLane
		return TxLane(self)._select()

	@property
	def AutoInstrumentation(self):
		"""The auto instrumentation mode.

		Returns:
			str(endOfFrame|floating)
		"""
		return self._get_attribute('autoInstrumentation')
	@AutoInstrumentation.setter
	def AutoInstrumentation(self, value):
		self._set_attribute('autoInstrumentation', value)

	@property
	def C2Expected(self):
		"""The expected value of the link partner's C2 byte. Typically, this will match the value in the Transmit field. (Hex). The default value is 0x24 (hex).

		Returns:
			number
		"""
		return self._get_attribute('c2Expected')
	@C2Expected.setter
	def C2Expected(self, value):
		self._set_attribute('c2Expected', value)

	@property
	def C2Tx(self):
		"""The value of the C2 byte in the transmitted stream. (Hex) The default value is 0x24 (hex).

		Returns:
			number
		"""
		return self._get_attribute('c2Tx')
	@C2Tx.setter
	def C2Tx(self, value):
		self._set_attribute('c2Tx', value)

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
	def EnabledFlowControl(self):
		"""Enables the port's MAC Flow control mechanisms to listen for a directed address pause message.

		Returns:
			bool
		"""
		return self._get_attribute('enabledFlowControl')
	@EnabledFlowControl.setter
	def EnabledFlowControl(self, value):
		self._set_attribute('enabledFlowControl', value)

	@property
	def FlowControlDirectedAddress(self):
		"""This is the 48-bit MAC address that the port will listen on for a directed pause message.

		Returns:
			str
		"""
		return self._get_attribute('flowControlDirectedAddress')
	@FlowControlDirectedAddress.setter
	def FlowControlDirectedAddress(self, value):
		self._set_attribute('flowControlDirectedAddress', value)

	@property
	def IfsStretch(self):
		"""If checked, indicates the ifsStretch as the desired mode of operation. The IFS Stretch ratio determines the number of bits in a frame that require one octet of Inter Frame Spacing Extension.

		Returns:
			bool
		"""
		return self._get_attribute('ifsStretch')
	@IfsStretch.setter
	def IfsStretch(self, value):
		self._set_attribute('ifsStretch', value)

	@property
	def InterfaceType(self):
		"""The 10G WAN interface type for the port.

		Returns:
			str(wanSdh|wanSonet)
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
	def TransmitClocking(self):
		"""The transmit clocking type for this 10G WAN port.

		Returns:
			str(external|internal|recovered)
		"""
		return self._get_attribute('transmitClocking')
	@TransmitClocking.setter
	def TransmitClocking(self, value):
		self._set_attribute('transmitClocking', value)

	@property
	def TxIgnoreRxLinkFaults(self):
		"""If enabled, will allow transmission of packets even if the receive link is down.

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreRxLinkFaults')
	@TxIgnoreRxLinkFaults.setter
	def TxIgnoreRxLinkFaults(self, value):
		self._set_attribute('txIgnoreRxLinkFaults', value)
