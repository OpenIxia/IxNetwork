from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dhcp4RelayAgentTlvProfile(Base):
	"""The Dhcp4RelayAgentTlvProfile class encapsulates a required dhcp4RelayAgentTlvProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcp4RelayAgentTlvProfile property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcp4RelayAgentTlvProfile'

	def __init__(self, parent):
		super(Dhcp4RelayAgentTlvProfile, self).__init__(parent)

	@property
	def TlvProfile(self):
		"""An instance of the TlvProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile.TlvProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile import TlvProfile
		return TlvProfile(self)

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
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)
