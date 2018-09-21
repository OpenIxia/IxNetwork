from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ExtendedCommunity(Base):
	"""The ExtendedCommunity class encapsulates a required extendedCommunity node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ExtendedCommunity property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'extendedCommunity'

	def __init__(self, parent):
		super(ExtendedCommunity, self).__init__(parent)

	@property
	def ExtendedCommunity(self):
		"""Associates BGP4 extended community attributes with a route item.

		Returns:
			list(dict(arg1:str[decimal|hex|ip|ieeeFloat],arg2:str[decimal|hex|ip|ieeeFloat],arg3:str[twoOctetAs|fourOctetAs|opaque|ip],arg4:str[routeTarget|origin|extendedBandwidthSubType],arg5:str))
		"""
		return self._get_attribute('extendedCommunity')
	@ExtendedCommunity.setter
	def ExtendedCommunity(self, value):
		self._set_attribute('extendedCommunity', value)
