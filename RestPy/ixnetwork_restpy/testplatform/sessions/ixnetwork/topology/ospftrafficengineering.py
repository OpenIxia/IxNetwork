
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


class OspfTrafficEngineering(Base):
	"""The OspfTrafficEngineering class encapsulates a required ospfTrafficEngineering node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OspfTrafficEngineering property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ospfTrafficEngineering'

	def __init__(self, parent):
		super(OspfTrafficEngineering, self).__init__(parent)

	@property
	def AdministratorGroup(self):
		"""Administrator Group

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('administratorGroup')

	@property
	def BandwidthPriority0(self):
		"""Bandwidth for Priority 0 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority0')

	@property
	def BandwidthPriority1(self):
		"""Bandwidth for Priority 1 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority1')

	@property
	def BandwidthPriority2(self):
		"""Bandwidth for Priority 2 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority2')

	@property
	def BandwidthPriority3(self):
		"""Bandwidth for Priority 3 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority3')

	@property
	def BandwidthPriority4(self):
		"""Bandwidth for Priority 4 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority4')

	@property
	def BandwidthPriority5(self):
		"""Bandwidth for Priority 5 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority5')

	@property
	def BandwidthPriority6(self):
		"""Bandwidth for Priority 6 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority6')

	@property
	def BandwidthPriority7(self):
		"""Bandwidth for Priority 7 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority7')

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
	def Enable(self):
		"""Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enable')

	@property
	def MaxBandwidth(self):
		"""Maximum Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxBandwidth')

	@property
	def MaxReservableBandwidth(self):
		"""Maximum Reservable Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxReservableBandwidth')

	@property
	def MetricLevel(self):
		"""TE Metric Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricLevel')

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

	def get_device_ids(self, PortNames=None, AdministratorGroup=None, BandwidthPriority0=None, BandwidthPriority1=None, BandwidthPriority2=None, BandwidthPriority3=None, BandwidthPriority4=None, BandwidthPriority5=None, BandwidthPriority6=None, BandwidthPriority7=None, Enable=None, MaxBandwidth=None, MaxReservableBandwidth=None, MetricLevel=None):
		"""Base class infrastructure that gets a list of ospfTrafficEngineering device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AdministratorGroup (str): optional regex of administratorGroup
			BandwidthPriority0 (str): optional regex of bandwidthPriority0
			BandwidthPriority1 (str): optional regex of bandwidthPriority1
			BandwidthPriority2 (str): optional regex of bandwidthPriority2
			BandwidthPriority3 (str): optional regex of bandwidthPriority3
			BandwidthPriority4 (str): optional regex of bandwidthPriority4
			BandwidthPriority5 (str): optional regex of bandwidthPriority5
			BandwidthPriority6 (str): optional regex of bandwidthPriority6
			BandwidthPriority7 (str): optional regex of bandwidthPriority7
			Enable (str): optional regex of enable
			MaxBandwidth (str): optional regex of maxBandwidth
			MaxReservableBandwidth (str): optional regex of maxReservableBandwidth
			MetricLevel (str): optional regex of metricLevel

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
