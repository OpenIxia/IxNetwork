
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

	def get_device_ids(self, PortNames=None, ActiveThisMetric=None, BFlag=None, MetricType=None, MetricValue=None):
		"""Base class infrastructure that gets a list of pceUpdateRsvpMetricSubObjectList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ActiveThisMetric (str): optional regex of activeThisMetric
			BFlag (str): optional regex of bFlag
			MetricType (str): optional regex of metricType
			MetricValue (str): optional regex of metricValue

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
