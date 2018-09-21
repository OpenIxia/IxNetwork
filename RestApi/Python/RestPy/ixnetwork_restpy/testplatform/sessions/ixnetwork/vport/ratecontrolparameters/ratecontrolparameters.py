from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RateControlParameters(Base):
	"""The RateControlParameters class encapsulates a required rateControlParameters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RateControlParameters property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rateControlParameters'

	def __init__(self, parent):
		super(RateControlParameters, self).__init__(parent)

	@property
	def ArpRefreshInterval(self):
		"""Indicates the Arp Refresh Interval per Port. Set this to override the defaul value of 60 seconds

		Returns:
			number
		"""
		return self._get_attribute('arpRefreshInterval')
	@ArpRefreshInterval.setter
	def ArpRefreshInterval(self, value):
		self._set_attribute('arpRefreshInterval', value)

	@property
	def MaxRequestsPerBurst(self):
		"""Indicates the flow pattern of the ARP/NS request for each port. Enable this, to send the ARP/NS requests in bursts of size defined by 'Max requests per Bursts'.

		Returns:
			number
		"""
		return self._get_attribute('maxRequestsPerBurst')
	@MaxRequestsPerBurst.setter
	def MaxRequestsPerBurst(self, value):
		self._set_attribute('maxRequestsPerBurst', value)

	@property
	def MaxRequestsPerSec(self):
		"""The maximum requests per second.

		Returns:
			number
		"""
		return self._get_attribute('maxRequestsPerSec')
	@MaxRequestsPerSec.setter
	def MaxRequestsPerSec(self, value):
		self._set_attribute('maxRequestsPerSec', value)

	@property
	def MinRetryInterval(self):
		"""Indicates the minimum wait time for re-sending the ARP/NS requests for a particular interface.

		Returns:
			number
		"""
		return self._get_attribute('minRetryInterval')
	@MinRetryInterval.setter
	def MinRetryInterval(self, value):
		self._set_attribute('minRetryInterval', value)

	@property
	def RetryCount(self):
		"""Indicates the number of times the ARP/NS requests will be resent for a particular interface, if there is an ARP issue.

		Returns:
			number
		"""
		return self._get_attribute('retryCount')
	@RetryCount.setter
	def RetryCount(self, value):
		self._set_attribute('retryCount', value)

	@property
	def SendInBursts(self):
		"""Indicates the flow pattern of the ARP/NS request for each port. Enable this, to send the ARP/NS requests in bursts of size defined by 'Max requests per Bursts'.

		Returns:
			bool
		"""
		return self._get_attribute('sendInBursts')
	@SendInBursts.setter
	def SendInBursts(self, value):
		self._set_attribute('sendInBursts', value)

	@property
	def SendRequestsAsFastAsPossible(self):
		"""If enabled, allows to send ARP/NS requests immediately without any rate control.

		Returns:
			bool
		"""
		return self._get_attribute('sendRequestsAsFastAsPossible')
	@SendRequestsAsFastAsPossible.setter
	def SendRequestsAsFastAsPossible(self, value):
		self._set_attribute('sendRequestsAsFastAsPossible', value)
