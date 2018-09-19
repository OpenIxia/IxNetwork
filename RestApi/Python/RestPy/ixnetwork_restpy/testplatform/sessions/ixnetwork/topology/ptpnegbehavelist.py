from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PtpNegBehaveList(Base):
	"""The PtpNegBehaveList class encapsulates a required ptpNegBehaveList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PtpNegBehaveList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ptpNegBehaveList'

	def __init__(self, parent):
		super(PtpNegBehaveList, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def MvActive(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvActive')

	@property
	def MvDelay(self):
		"""Delay To Follow in this message (ns)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvDelay')

	@property
	def MvFieldValue(self):
		"""Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvFieldValue')

	@property
	def MvFieldValue1(self):
		"""Value1

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvFieldValue1')

	@property
	def MvMsgAction(self):
		"""Action On The Message Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvMsgAction')

	@property
	def MvPtpMsgField(self):
		"""PTP Msg Field

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvPtpMsgField')

	@property
	def MvPtpMsgField1(self):
		"""PTP Msg Field1

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mvPtpMsgField1')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PtpMsgType(self):
		"""Displays the current PTP Msg

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ptpMsgType')

	@property
	def PtpValueDisPattern(self):
		"""Pattern For Value Field

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ptpValueDisPattern')

	@property
	def PtpValueDisPattern1(self):
		"""Pattern For Value Field

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ptpValueDisPattern1')
