from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedFilter(Base):
	"""The LearnedFilter class encapsulates a required learnedFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedFilter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedFilter'

	def __init__(self, parent):
		super(LearnedFilter, self).__init__(parent)

	@property
	def Capabilities(self):
		"""An instance of the Capabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.capabilities.Capabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.capabilities import Capabilities
		return Capabilities(self)._select()

	@property
	def Prefix(self):
		"""An instance of the Prefix class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.prefix.Prefix)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.prefix import Prefix
		return Prefix(self)._select()

	@property
	def Afi(self):
		"""Address Family Identifier value. Identifies the network layer protocol to be used with these routes.

		Returns:
			number
		"""
		return self._get_attribute('afi')
	@Afi.setter
	def Afi(self, value):
		self._set_attribute('afi', value)

	@property
	def EnableAfiSafi(self):
		"""If enabled, allows the user to set values to be used for BGP-MP - the user-specified AFI and SAFI values for the BGP MP_REACH_NLRI.

		Returns:
			bool
		"""
		return self._get_attribute('enableAfiSafi')
	@EnableAfiSafi.setter
	def EnableAfiSafi(self, value):
		self._set_attribute('enableAfiSafi', value)

	@property
	def EnablePrefix(self):
		"""If enabled, BGP Prefix Filters configured in this dialog will be used to filter for routes that match those filter entries. Only those routes will be stored in the routing table. If disabled, all learned BGP routes will be stored.

		Returns:
			bool
		"""
		return self._get_attribute('enablePrefix')
	@EnablePrefix.setter
	def EnablePrefix(self, value):
		self._set_attribute('enablePrefix', value)

	@property
	def Safi(self):
		"""Subsequent Address Family Identifier value. Used with, and provides additional information about, the AFI in the NLRI, per RFC 2858.

		Returns:
			number
		"""
		return self._get_attribute('safi')
	@Safi.setter
	def Safi(self, value):
		self._set_attribute('safi', value)
