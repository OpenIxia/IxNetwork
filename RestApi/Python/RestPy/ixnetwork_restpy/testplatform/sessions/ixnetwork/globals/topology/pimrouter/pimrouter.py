from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PimRouter(Base):
	"""The PimRouter class encapsulates a required pimRouter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PimRouter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pimRouter'

	def __init__(self, parent):
		super(PimRouter, self).__init__(parent)

	@property
	def BootstrapMessagePerInterval(self):
		"""Bootstrap Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bootstrapMessagePerInterval')

	@property
	def CRpAdvertiseMessagePerInterval(self):
		"""C-RP Advertise Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cRpAdvertiseMessagePerInterval')

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
	def DiscardJoinPruneProcessing(self):
		"""Discard join/Prune Processing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardJoinPruneProcessing')

	@property
	def EnableRateControl(self):
		"""Enable Rate Control

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRateControl')

	@property
	def HelloMessagePerInterval(self):
		"""Hello Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('helloMessagePerInterval')

	@property
	def Interval(self):
		"""Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interval')

	@property
	def JoinPruneMessagePerInterval(self):
		"""Join/Prune Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('joinPruneMessagePerInterval')

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
	def RegisterMessagePerInterval(self):
		"""Register Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerMessagePerInterval')

	@property
	def RegisterStopMessagePerInterval(self):
		"""Register Stop Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerStopMessagePerInterval')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')
