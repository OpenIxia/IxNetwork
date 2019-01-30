
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


class PceUpdateSrMetricSubObjectList(Base):
	"""The PceUpdateSrMetricSubObjectList class encapsulates a system managed pceUpdateSrMetricSubObjectList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceUpdateSrMetricSubObjectList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceUpdateSrMetricSubObjectList'

	def __init__(self, parent):
		super(PceUpdateSrMetricSubObjectList, self).__init__(parent)

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
		"""Finds and retrieves pceUpdateSrMetricSubObjectList data from the server.

		All named parameters support regex and can be used to selectively retrieve pceUpdateSrMetricSubObjectList data from the server.
		By default the find method takes no parameters and will retrieve all pceUpdateSrMetricSubObjectList data from the server.

		Returns:
			self: This instance with matching pceUpdateSrMetricSubObjectList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceUpdateSrMetricSubObjectList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceUpdateSrMetricSubObjectList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, ActiveThisMetric=None, BFlag=None, MetricType=None, MetricValue=None):
		"""Base class infrastructure that gets a list of pceUpdateSrMetricSubObjectList device ids encapsulated by this object.

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

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
