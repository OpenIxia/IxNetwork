
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			str
		"""
		return self._get_attribute('advRouterId')
	@AdvRouterId.setter
	def AdvRouterId(self, value):
		self._set_attribute('advRouterId', value)

	@property
	def AreaSummaryLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('areaSummaryLsaCount')

	@property
	def EnableAdvRouterId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvRouterId')
	@EnableAdvRouterId.setter
	def EnableAdvRouterId(self, value):
		self._set_attribute('enableAdvRouterId', value)

	@property
	def EnableFilter(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFilter')
	@EnableFilter.setter
	def EnableFilter(self, value):
		self._set_attribute('enableFilter', value)

	@property
	def EnableLinkStateId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkStateId')
	@EnableLinkStateId.setter
	def EnableLinkStateId(self, value):
		self._set_attribute('enableLinkStateId', value)

	@property
	def ExcludeAdvRouterId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('excludeAdvRouterId')
	@ExcludeAdvRouterId.setter
	def ExcludeAdvRouterId(self, value):
		self._set_attribute('excludeAdvRouterId', value)

	@property
	def ExcludeLinkStateId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('excludeLinkStateId')
	@ExcludeLinkStateId.setter
	def ExcludeLinkStateId(self, value):
		self._set_attribute('excludeLinkStateId', value)

	@property
	def ExternalLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('externalLsaCount')

	@property
	def ExternalSummaryLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('externalSummaryLsaCount')

	@property
	def IsComplete(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isComplete')

	@property
	def LinkStateId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('linkStateId')
	@LinkStateId.setter
	def LinkStateId(self, value):
		self._set_attribute('linkStateId', value)

	@property
	def NetworkLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkLsaCount')

	@property
	def NssaLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nssaLsaCount')

	@property
	def OpaqueAreaScopeLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('opaqueAreaScopeLsaCount')

	@property
	def OpaqueAsScopeLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('opaqueAsScopeLsaCount')

	@property
	def OpaqueLocalScopeLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('opaqueLocalScopeLsaCount')

	@property
	def RouterLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routerLsaCount')

	@property
	def ShowExternalAsLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showExternalAsLsa')
	@ShowExternalAsLsa.setter
	def ShowExternalAsLsa(self, value):
		self._set_attribute('showExternalAsLsa', value)

	@property
	def ShowNetworkLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showNetworkLsa')
	@ShowNetworkLsa.setter
	def ShowNetworkLsa(self, value):
		self._set_attribute('showNetworkLsa', value)

	@property
	def ShowNssaLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showNssaLsa')
	@ShowNssaLsa.setter
	def ShowNssaLsa(self, value):
		self._set_attribute('showNssaLsa', value)

	@property
	def ShowOpaqueAreaLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueAreaLsa')
	@ShowOpaqueAreaLsa.setter
	def ShowOpaqueAreaLsa(self, value):
		self._set_attribute('showOpaqueAreaLsa', value)

	@property
	def ShowOpaqueDomainLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueDomainLsa')
	@ShowOpaqueDomainLsa.setter
	def ShowOpaqueDomainLsa(self, value):
		self._set_attribute('showOpaqueDomainLsa', value)

	@property
	def ShowOpaqueLocalLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showOpaqueLocalLsa')
	@ShowOpaqueLocalLsa.setter
	def ShowOpaqueLocalLsa(self, value):
		self._set_attribute('showOpaqueLocalLsa', value)

	@property
	def ShowRouterLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showRouterLsa')
	@ShowRouterLsa.setter
	def ShowRouterLsa(self, value):
		self._set_attribute('showRouterLsa', value)

	@property
	def ShowSummaryAsLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showSummaryAsLsa')
	@ShowSummaryAsLsa.setter
	def ShowSummaryAsLsa(self, value):
		self._set_attribute('showSummaryAsLsa', value)

	@property
	def ShowSummaryIpLsa(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('showSummaryIpLsa')
	@ShowSummaryIpLsa.setter
	def ShowSummaryIpLsa(self, value):
		self._set_attribute('showSummaryIpLsa', value)

	@property
	def TotalLsaCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalLsaCount')
