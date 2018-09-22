from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PcRequestMatchCriteria(Base):
	"""The PcRequestMatchCriteria class encapsulates a required pcRequestMatchCriteria node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PcRequestMatchCriteria property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pcRequestMatchCriteria'

	def __init__(self, parent):
		super(PcRequestMatchCriteria, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def DestIpv4Address(self):
		"""Destination IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destIpv4Address')

	@property
	def DestIpv6Address(self):
		"""Destination IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destIpv6Address')

	@property
	def IpVersion(self):
		"""IP Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipVersion')

	@property
	def IroType(self):
		"""Match IRO Option

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('iroType')

	@property
	def MatchEndPoints(self):
		"""Indicates Whether response parameters will be matched based on endpoints in the PCReq messaged received from PCC.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('matchEndPoints')

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
	def SrcIpv4Address(self):
		"""Source IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srcIpv4Address')

	@property
	def SrcIpv6Address(self):
		"""Source IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srcIpv6Address')
