from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceUpdateRsvpMetricSubObjectList(Base):
	"""The PceUpdateRsvpMetricSubObjectList class encapsulates a system managed pceUpdateRsvpMetricSubObjectList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceUpdateRsvpMetricSubObjectList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceUpdateRsvpMetricSubObjectList'

	def __init__(self, parent):
		super(PceUpdateRsvpMetricSubObjectList, self).__init__(parent)

	@property
	def ActiveThisMetric(self):
		"""Specifies whether the corresponding metric object is active or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeThisMetric')

	@property
	def BFlag(self):
		"""B (bound) flag MUST be set in the METRIC object, which specifies that the SID depth for the computed path MUST NOT exceed the metric-value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bFlag')

	@property
	def MetricType(self):
		"""This is a drop down which has 4 choices: IGP/ TE/ Hop count/ MSD.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricType')

	@property
	def MetricValue(self):
		"""User can specify the metric value corresponding to the metric type selected.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricValue')

	def find(self):
		"""Finds and retrieves pceUpdateRsvpMetricSubObjectList data from the server.

		All named parameters support regex and can be used to selectively retrieve pceUpdateRsvpMetricSubObjectList data from the server.
		By default the find method takes no parameters and will retrieve all pceUpdateRsvpMetricSubObjectList data from the server.

		Returns:
			self: This instance with matching pceUpdateRsvpMetricSubObjectList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceUpdateRsvpMetricSubObjectList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceUpdateRsvpMetricSubObjectList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
