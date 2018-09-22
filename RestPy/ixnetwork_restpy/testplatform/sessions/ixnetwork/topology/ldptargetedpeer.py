from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpTargetedPeer(Base):
	"""The LdpTargetedPeer class encapsulates a required ldpTargetedPeer node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LdpTargetedPeer property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ldpTargetedPeer'

	def __init__(self, parent):
		super(LdpTargetedPeer, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Authentication(self):
		"""The type of cryptographic authentication to be used for this targeted peer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authentication')

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
	def IPAddress(self):
		"""The IP address of the non-directly linked LDP peer to which the targeted Hello is being sent

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('iPAddress')

	@property
	def InitiateTargetedHello(self):
		"""If selected, a Targeted Hello will be sent to the LDP Peer specified by the IP address in this row

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initiateTargetedHello')

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def MD5Key(self):
		"""A value to be used as a secret MD5 key for authentication

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mD5Key')

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
	def TargetedHelloInterval(self):
		"""Targeted Hello Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('targetedHelloInterval')

	@property
	def TargetedHoldTime(self):
		"""Targeted Hold Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('targetedHoldTime')
