from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RangeTe(Base):
	"""The RangeTe class encapsulates a required rangeTe node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RangeTe property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rangeTe'

	def __init__(self, parent):
		super(RangeTe, self).__init__(parent)

	@property
	def EnableRangeTe(self):
		"""Enables the generation of Traffic Engineering data. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableRangeTe')
	@EnableRangeTe.setter
	def EnableRangeTe(self, value):
		self._set_attribute('enableRangeTe', value)

	@property
	def TeAdmGroup(self):
		"""For setting the Administrative group sub-TLV (sub-TLV 3). It is a 4-octet user-defined bit mask used to assign administrative group numbers to the interface., for use in assigning colors and resource classes. Each set bit corresponds to a single administrative group for this interface. The settings translate into Group numbers which range from 0 to 31 (integers).

		Returns:
			str
		"""
		return self._get_attribute('teAdmGroup')
	@TeAdmGroup.setter
	def TeAdmGroup(self, value):
		self._set_attribute('teAdmGroup', value)

	@property
	def TeLinkMetric(self):
		"""The metric associated with the interface that the TE data is advertised on.

		Returns:
			number
		"""
		return self._get_attribute('teLinkMetric')
	@TeLinkMetric.setter
	def TeLinkMetric(self, value):
		self._set_attribute('teLinkMetric', value)

	@property
	def TeMaxBandWidth(self):
		"""For setting the maximum link bandwidth (sub-TLV 9) allowed for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.00.

		Returns:
			number
		"""
		return self._get_attribute('teMaxBandWidth')
	@TeMaxBandWidth.setter
	def TeMaxBandWidth(self, value):
		self._set_attribute('teMaxBandWidth', value)

	@property
	def TeMaxReserveBandWidth(self):
		"""For setting the Maximum reservable link bandwidth sub-TLV 10). It is the maximum bandwidth that can be reserved for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.00.

		Returns:
			number
		"""
		return self._get_attribute('teMaxReserveBandWidth')
	@TeMaxReserveBandWidth.setter
	def TeMaxReserveBandWidth(self, value):
		self._set_attribute('teMaxReserveBandWidth', value)

	@property
	def TeRouterId(self):
		"""The 32-bit TE router ID assigned to the first emulated ISIS router in this network range used with the increment TE router ID value when more than one router is to be created.

		Returns:
			str
		"""
		return self._get_attribute('teRouterId')
	@TeRouterId.setter
	def TeRouterId(self, value):
		self._set_attribute('teRouterId', value)

	@property
	def TeRouterIdIncrement(self):
		"""The 32-bit increment value that will be added to the previous TE Router ID, for automatically creating additional TE Router IDs for the emulated routers in this network range.

		Returns:
			str
		"""
		return self._get_attribute('teRouterIdIncrement')
	@TeRouterIdIncrement.setter
	def TeRouterIdIncrement(self, value):
		self._set_attribute('teRouterIdIncrement', value)

	@property
	def TeUnreservedBandWidth(self):
		"""The traffic engineering unreserved bandwidth for each priority to be advertised. There are eight distinct options. (default = 0.0)

		Returns:
			list(number)
		"""
		return self._get_attribute('teUnreservedBandWidth')
	@TeUnreservedBandWidth.setter
	def TeUnreservedBandWidth(self, value):
		self._set_attribute('teUnreservedBandWidth', value)
