from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ethernet(Base):
	"""The Ethernet class encapsulates a required ethernet node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ethernet property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ethernet'

	def __init__(self, parent):
		super(Ethernet, self).__init__(parent)

	@property
	def Fcoe(self):
		"""An instance of the Fcoe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.fcoe.fcoe import Fcoe
		return Fcoe(self)._select()

	@property
	def Oam(self):
		"""An instance of the Oam class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.oam.oam.Oam)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.oam.oam import Oam
		return Oam(self)._select()

	@property
	def TxLane(self):
		"""An instance of the TxLane class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.txlane.txlane.TxLane)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.txlane.txlane import TxLane
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
		"""If enabled, allows autonegotiation between ports for speed and duplex operation based on the various choices. The selected capabilities are advertised during AutoNegotiation

		Returns:
			bool
		"""
		return self._get_attribute('autoNegotiate')
	@AutoNegotiate.setter
	def AutoNegotiate(self, value):
		self._set_attribute('autoNegotiate', value)

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
		"""If true, enables the port's MAC flow control and mechanisms to listen for a directed address pause message.

		Returns:
			bool
		"""
		return self._get_attribute('enabledFlowControl')
	@EnabledFlowControl.setter
	def EnabledFlowControl(self, value):
		self._set_attribute('enabledFlowControl', value)

	@property
	def FlowControlDirectedAddress(self):
		"""The 48-bit MAC address that the port listens on for a directed pause.

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
	def MasterSlaveMode(self):
		"""NOT DEFINED

		Returns:
			str(master|slave)
		"""
		return self._get_attribute('masterSlaveMode')
	@MasterSlaveMode.setter
	def MasterSlaveMode(self, value):
		self._set_attribute('masterSlaveMode', value)

	@property
	def Media(self):
		"""Available only for Ethernet cards that support this dual-PHY capability.

		Returns:
			str(copper|fiber|sgmii)
		"""
		return self._get_attribute('media')
	@Media.setter
	def Media(self, value):
		self._set_attribute('media', value)

	@property
	def NegotiateMasterSlave(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('negotiateMasterSlave')
	@NegotiateMasterSlave.setter
	def NegotiateMasterSlave(self, value):
		self._set_attribute('negotiateMasterSlave', value)

	@property
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def Speed(self):
		"""The speed and duplex operation options.

		Returns:
			str(auto|speed1000|speed100fd|speed100hd|speed10fd|speed10hd)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)

	@property
	def SpeedAuto(self):
		"""If selected, allows auto negotiation between ports for speed and duplex operation based on the various choices. The selected capabilities are advertised during AutoNegotiation.

		Returns:
			list(str[all|speed1000|speed100fd|speed100hd|speed10fd|speed10hd])
		"""
		return self._get_attribute('speedAuto')
	@SpeedAuto.setter
	def SpeedAuto(self, value):
		self._set_attribute('speedAuto', value)
