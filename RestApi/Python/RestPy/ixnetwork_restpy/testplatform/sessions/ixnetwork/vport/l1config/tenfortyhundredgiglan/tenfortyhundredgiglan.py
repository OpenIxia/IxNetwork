from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TenFortyHundredGigLan(Base):
	"""The TenFortyHundredGigLan class encapsulates a required tenFortyHundredGigLan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TenFortyHundredGigLan property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'tenFortyHundredGigLan'

	def __init__(self, parent):
		super(TenFortyHundredGigLan, self).__init__(parent)

	@property
	def Fcoe(self):
		"""An instance of the Fcoe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.fcoe.fcoe import Fcoe
		return Fcoe(self)._select()

	@property
	def TxLane(self):
		"""An instance of the TxLane class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.txlane.txlane.TxLane)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.txlane.txlane import TxLane
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
	def BadBlocksNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('badBlocksNumber')
	@BadBlocksNumber.setter
	def BadBlocksNumber(self, value):
		self._set_attribute('badBlocksNumber', value)

	@property
	def EnableAutoNegotiation(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoNegotiation')
	@EnableAutoNegotiation.setter
	def EnableAutoNegotiation(self, value):
		self._set_attribute('enableAutoNegotiation', value)

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
	def EnableRsFec(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableRsFec')
	@EnableRsFec.setter
	def EnableRsFec(self, value):
		self._set_attribute('enableRsFec', value)

	@property
	def EnableRsFecStats(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableRsFecStats')
	@EnableRsFecStats.setter
	def EnableRsFecStats(self, value):
		self._set_attribute('enableRsFecStats', value)

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
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('flowControlDirectedAddress')
	@FlowControlDirectedAddress.setter
	def FlowControlDirectedAddress(self, value):
		self._set_attribute('flowControlDirectedAddress', value)

	@property
	def GoodBlocksNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('goodBlocksNumber')
	@GoodBlocksNumber.setter
	def GoodBlocksNumber(self, value):
		self._set_attribute('goodBlocksNumber', value)

	@property
	def IeeeL1Defaults(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ieeeL1Defaults')
	@IeeeL1Defaults.setter
	def IeeeL1Defaults(self, value):
		self._set_attribute('ieeeL1Defaults', value)

	@property
	def LaserOn(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('laserOn')
	@LaserOn.setter
	def LaserOn(self, value):
		self._set_attribute('laserOn', value)

	@property
	def LinkTraining(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('linkTraining')
	@LinkTraining.setter
	def LinkTraining(self, value):
		self._set_attribute('linkTraining', value)

	@property
	def LoopContinuously(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('loopContinuously')
	@LoopContinuously.setter
	def LoopContinuously(self, value):
		self._set_attribute('loopContinuously', value)

	@property
	def LoopCountNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('loopCountNumber')
	@LoopCountNumber.setter
	def LoopCountNumber(self, value):
		self._set_attribute('loopCountNumber', value)

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
		"""Indicates the value that needs to be adjusted for the line transmit frequency

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def SendSetsMode(self):
		"""NOT DEFINED

		Returns:
			str(alternate|typeAOnly|typeBOnly)
		"""
		return self._get_attribute('sendSetsMode')
	@SendSetsMode.setter
	def SendSetsMode(self, value):
		self._set_attribute('sendSetsMode', value)

	@property
	def Speed(self):
		"""The speed of the lan

		Returns:
			str(speed100g|speed10g|speed25g|speed40g|speed50g)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)

	@property
	def StartErrorInsertion(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('startErrorInsertion')
	@StartErrorInsertion.setter
	def StartErrorInsertion(self, value):
		self._set_attribute('startErrorInsertion', value)

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

	@property
	def TypeAOrderedSets(self):
		"""NOT DEFINED

		Returns:
			str(localFault|remoteFault)
		"""
		return self._get_attribute('typeAOrderedSets')
	@TypeAOrderedSets.setter
	def TypeAOrderedSets(self, value):
		self._set_attribute('typeAOrderedSets', value)

	@property
	def TypeBOrderedSets(self):
		"""NOT DEFINED

		Returns:
			str(localFault|remoteFault)
		"""
		return self._get_attribute('typeBOrderedSets')
	@TypeBOrderedSets.setter
	def TypeBOrderedSets(self, value):
		self._set_attribute('typeBOrderedSets', value)
