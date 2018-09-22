from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EntryTe(Base):
	"""The EntryTe class encapsulates a required entryTe node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EntryTe property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'entryTe'

	def __init__(self, parent):
		super(EntryTe, self).__init__(parent)

	@property
	def EnableEntryTe(self):
		"""If enabled, the Entry TE configuration values specified in the ISIS Advanced Router Settings TE dialog may be overridden, and replaced by the values specified in this dialog.

		Returns:
			bool
		"""
		return self._get_attribute('enableEntryTe')
	@EnableEntryTe.setter
	def EnableEntryTe(self, value):
		self._set_attribute('enableEntryTe', value)

	@property
	def EteAdmGroup(self):
		"""For setting the administrative group sub-TLV (sub-TLV 3). It is a 4-octet user-defined bit mask used to assign administrative group numbers to the interface., for use in assigning colors and resource classes. Each set bit corresponds to a single administrative group for this interface. The settings translate into group numbers which range from 0 to 31 (integers).The default value is 00 00 00 00 (hex)

		Returns:
			str
		"""
		return self._get_attribute('eteAdmGroup')
	@EteAdmGroup.setter
	def EteAdmGroup(self, value):
		self._set_attribute('eteAdmGroup', value)

	@property
	def EteLinkMetric(self):
		"""A user-defined metric for the link.

		Returns:
			number
		"""
		return self._get_attribute('eteLinkMetric')
	@EteLinkMetric.setter
	def EteLinkMetric(self, value):
		self._set_attribute('eteLinkMetric', value)

	@property
	def EteMaxBandWidth(self):
		"""For setting the Maximum link bandwidth (sub-TLV 9) allowed for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.00.

		Returns:
			number
		"""
		return self._get_attribute('eteMaxBandWidth')
	@EteMaxBandWidth.setter
	def EteMaxBandWidth(self, value):
		self._set_attribute('eteMaxBandWidth', value)

	@property
	def EteMaxReserveBandWidth(self):
		"""For setting the Maximum reservable link bandwidth sub-TLV 10). It is the maximum bandwidth that can be reserved for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.00.

		Returns:
			number
		"""
		return self._get_attribute('eteMaxReserveBandWidth')
	@EteMaxReserveBandWidth.setter
	def EteMaxReserveBandWidth(self, value):
		self._set_attribute('eteMaxReserveBandWidth', value)

	@property
	def EteRouterId(self):
		"""This attribute is the TE router ID of the first router in the grid (at row = 0, column = 0), in IPv4 format.

		Returns:
			str
		"""
		return self._get_attribute('eteRouterId')
	@EteRouterId.setter
	def EteRouterId(self, value):
		self._set_attribute('eteRouterId', value)

	@property
	def EteRouterIdIncrement(self):
		"""The increment step to be used for creating the router IDs for the emulated ISIS routers in this network range.

		Returns:
			str
		"""
		return self._get_attribute('eteRouterIdIncrement')
	@EteRouterIdIncrement.setter
	def EteRouterIdIncrement(self, value):
		self._set_attribute('eteRouterIdIncrement', value)

	@property
	def EteUnreservedBandWidth(self):
		"""There are eight levels, one for each possible priority level (for colors or resource classes). The values specify the amount of bandwidth that can be reserved for each of 8 priority levels (0 through 7). The bandwidth values are 32-bit IEEE floating point values, in bytes/sec.The default is 0.00. The total bandwidth for all 8 priority levels may exceed the bandwidth of the link, in cases where the user wants to oversubscribe the link.

		Returns:
			list(number)
		"""
		return self._get_attribute('eteUnreservedBandWidth')
	@EteUnreservedBandWidth.setter
	def EteUnreservedBandWidth(self, value):
		self._set_attribute('eteUnreservedBandWidth', value)
