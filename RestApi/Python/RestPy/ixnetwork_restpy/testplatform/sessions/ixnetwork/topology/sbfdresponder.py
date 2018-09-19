from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SbfdResponder(Base):
	"""The SbfdResponder class encapsulates a required sbfdResponder node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SbfdResponder property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'sbfdResponder'

	def __init__(self, parent):
		super(SbfdResponder, self).__init__(parent)

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
	def MinRxInterval(self):
		"""Minimum Rx Interval in ms supported by the Responder

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minRxInterval')

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
	def SBFDDiscriminator(self):
		"""Configures the local S-BFD discriminator

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sBFDDiscriminator')

	@property
	def SBFDState(self):
		"""Configures the S-BFD session state to be sent in Response Packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sBFDState')
