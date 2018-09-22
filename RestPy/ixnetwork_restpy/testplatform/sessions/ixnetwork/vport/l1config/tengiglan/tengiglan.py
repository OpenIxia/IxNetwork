from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TenGigLan(Base):
	"""The TenGigLan class encapsulates a required tenGigLan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TenGigLan property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'tenGigLan'

	def __init__(self, parent):
		super(TenGigLan, self).__init__(parent)

	@property
	def Fcoe(self):
		"""An instance of the Fcoe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.fcoe.fcoe import Fcoe
		return Fcoe(self)._select()

	@property
	def Oam(self):
		"""An instance of the Oam class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.oam.oam.Oam)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.oam.oam import Oam
		return Oam(self)._select()

	@property
	def TxLane(self):
		"""An instance of the TxLane class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.txlane.txlane.TxLane)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.txlane.txlane import TxLane
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
	def AutoNegotiate(self):
		"""NOT DEFINED

		Returns:
			str(asymmetric|both|fullDuplex|none)
		"""
		return self._get_attribute('autoNegotiate')
	@AutoNegotiate.setter
	def AutoNegotiate(self, value):
		self._set_attribute('autoNegotiate', value)

	@property
	def EnableLASIMonitoring(self):
		"""If selected, enables LASI monitoring.

		Returns:
			bool
		"""
		return self._get_attribute('enableLASIMonitoring')
	@EnableLASIMonitoring.setter
	def EnableLASIMonitoring(self, value):
		self._set_attribute('enableLASIMonitoring', value)

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
	def LoopbackMode(self):
		"""NOT DEFINED

		Returns:
			str(internalLoopback|lineLoopback|none)
		"""
		return self._get_attribute('loopbackMode')
	@LoopbackMode.setter
	def LoopbackMode(self, value):
		self._set_attribute('loopbackMode', value)

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
		"""The transmit clocking type for the 10G LAN port.

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
