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
	def AdvRouterId(self):
		"""Filter on the router ID of the router that is originating the LSA.

		Returns:
			str
		"""
		return self._get_attribute('advRouterId')
	@AdvRouterId.setter
	def AdvRouterId(self, value):
		self._set_attribute('advRouterId', value)

	@property
	def AreaSummaryLsaCount(self):
		"""Filter on the number of LSAs in the Summary Area.

		Returns:
			number
		"""
		return self._get_attribute('areaSummaryLsaCount')

	@property
	def EnableAdvRouterId(self):
		"""If true filter on the advertised router ID.

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvRouterId')
	@EnableAdvRouterId.setter
	def EnableAdvRouterId(self, value):
		self._set_attribute('enableAdvRouterId', value)

	@property
	def EnableFilter(self):
		"""Enables the use of the OSPF learned filter.

		Returns:
			bool
		"""
		return self._get_attribute('enableFilter')
	@EnableFilter.setter
	def EnableFilter(self, value):
		self._set_attribute('enableFilter', value)

	@property
	def EnableLinkStateId(self):
		"""If true, filter on the Link State ID.

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkStateId')
	@EnableLinkStateId.setter
	def EnableLinkStateId(self, value):
		self._set_attribute('enableLinkStateId', value)

	@property
	def ExcludeAdvRouterId(self):
		"""If true, filter on no advertised router ID available.

		Returns:
			bool
		"""
		return self._get_attribute('excludeAdvRouterId')
	@ExcludeAdvRouterId.setter
	def ExcludeAdvRouterId(self, value):
		self._set_attribute('excludeAdvRouterId', value)

	@property
	def ExcludeLinkStateId(self):
		"""If true, filter on no Link State ID available.

		Returns:
			bool
		"""
		return self._get_attribute('excludeLinkStateId')
	@ExcludeLinkStateId.setter
	def ExcludeLinkStateId(self, value):
		self._set_attribute('excludeLinkStateId', value)

	@property
	def ExternalLsaCount(self):
		"""Filter on the number of External LSAs.

		Returns:
			number
		"""
		return self._get_attribute('externalLsaCount')

	@property
	def ExternalSummaryLsaCount(self):
		"""Filter on the number of External Summary LSAs.

		Returns:
			number
		"""
		return self._get_attribute('externalSummaryLsaCount')

	@property
	def IsComplete(self):
		"""If true, indicates the Filter operation has finished.

		Returns:
			bool
		"""
		return self._get_attribute('isComplete')

	@property
	def LinkStateId(self):
		"""Filter on the Link State ID.

		Returns:
			str
		"""
		return self._get_attribute('linkStateId')
	@LinkStateId.setter
	def LinkStateId(self, value):
		self._set_attribute('linkStateId', value)

	@property
	def NetworkLsaCount(self):
		"""Filter on the number of Network LSAs.

		Returns:
			number
		"""
		return self._get_attribute('networkLsaCount')

	@property
	def NssaLsaCount(self):
		"""Filter on the number of NSSA LSAs.

		Returns:
			number
		"""
		return self._get_attribute('nssaLsaCount')

	@property
	def OpaqueAreaScopeLsaCount(self):
		"""Filter on the number of Opaque Area LSAs.

		Returns:
			number
		"""
		return self._get_attribute('opaqueAreaScopeLsaCount')

	@property
	def OpaqueAsScopeLsaCount(self):
		"""Filter on the number of AS Scope LSAs.

		Returns:
			number
		"""
		return self._get_attribute('opaqueAsScopeLsaCount')

	@property
	def OpaqueLocalScopeLsaCount(self):
		"""Filter on the number of Local Scope LSAs.

		Returns:
			number
		"""
		return self._get_attribute('opaqueLocalScopeLsaCount')

	@property
	def RouterLsaCount(self):
		"""Filter on the number of Router LSAs.

		Returns:
			number
		"""
		return self._get_attribute('routerLsaCount')

	@property
	def ShowExternalAsLsa(self):
		"""If true, filter on the LSAs from routers with External routes.

		Returns:
			bool
		"""
		return self._get_attribute('showExternalAsLsa')
	@ShowExternalAsLsa.setter
	def ShowExternalAsLsa(self, value):
		self._set_attribute('showExternalAsLsa', value)

	@property
	def ShowNetworkLsa(self):
		"""If true, filter on LSAs from router with Network routes.

		Returns:
			bool
		"""
		return self._get_attribute('showNetworkLsa')
	@ShowNetworkLsa.setter
	def ShowNetworkLsa(self, value):
		self._set_attribute('showNetworkLsa', value)

	@property
	def ShowNssaLsa(self):
		"""If true, filter on LSAs from router with NSSA routes.

		Returns:
			bool
		"""
		return self._get_attribute('showNssaLsa')
	@ShowNssaLsa.setter
	def ShowNssaLsa(self, value):
		self._set_attribute('showNssaLsa', value)

	@property
	def ShowOpaqueAreaLsa(self):
		"""If true, filter on LSAs from router with Opaque Area routes.

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueAreaLsa')
	@ShowOpaqueAreaLsa.setter
	def ShowOpaqueAreaLsa(self, value):
		self._set_attribute('showOpaqueAreaLsa', value)

	@property
	def ShowOpaqueDomainLsa(self):
		"""If true, filter on LSAs from router with Opaque Domain routes.

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueDomainLsa')
	@ShowOpaqueDomainLsa.setter
	def ShowOpaqueDomainLsa(self, value):
		self._set_attribute('showOpaqueDomainLsa', value)

	@property
	def ShowOpaqueLocalLsa(self):
		"""If true, filter on LSAs from router with Opaque Local routes.

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueLocalLsa')
	@ShowOpaqueLocalLsa.setter
	def ShowOpaqueLocalLsa(self, value):
		self._set_attribute('showOpaqueLocalLsa', value)

	@property
	def ShowRouterLsa(self):
		"""If true, filter on LSAs from router with BR or DBR routes.

		Returns:
			bool
		"""
		return self._get_attribute('showRouterLsa')
	@ShowRouterLsa.setter
	def ShowRouterLsa(self, value):
		self._set_attribute('showRouterLsa', value)

	@property
	def ShowSummaryAsLsa(self):
		"""If true, filter on LSAs from router with Summary AS routes.

		Returns:
			bool
		"""
		return self._get_attribute('showSummaryAsLsa')
	@ShowSummaryAsLsa.setter
	def ShowSummaryAsLsa(self, value):
		self._set_attribute('showSummaryAsLsa', value)

	@property
	def ShowSummaryIpLsa(self):
		"""If true, filter on LSAs from router with Summary IP routes.

		Returns:
			bool
		"""
		return self._get_attribute('showSummaryIpLsa')
	@ShowSummaryIpLsa.setter
	def ShowSummaryIpLsa(self, value):
		self._set_attribute('showSummaryIpLsa', value)

	@property
	def TotalLsaCount(self):
		"""Filter on the total number of LSAs.

		Returns:
			number
		"""
		return self._get_attribute('totalLsaCount')
