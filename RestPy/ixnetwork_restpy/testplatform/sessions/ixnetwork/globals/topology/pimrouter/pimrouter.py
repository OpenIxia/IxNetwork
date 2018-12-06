
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


class PimRouter(Base):
	"""The PimRouter class encapsulates a required pimRouter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PimRouter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pimRouter'

	def __init__(self, parent):
		super(PimRouter, self).__init__(parent)

	@property
	def BootstrapMessagePerInterval(self):
		"""Bootstrap Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bootstrapMessagePerInterval')

	@property
	def CRpAdvertiseMessagePerInterval(self):
		"""C-RP Advertise Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cRpAdvertiseMessagePerInterval')

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
	def DiscardJoinPruneProcessing(self):
		"""Discard join/Prune Processing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardJoinPruneProcessing')

	@property
	def EnableRateControl(self):
		"""Enable Rate Control

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRateControl')

	@property
	def HelloMessagePerInterval(self):
		"""Hello Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('helloMessagePerInterval')

	@property
	def Interval(self):
		"""Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interval')

	@property
	def JoinPruneMessagePerInterval(self):
		"""Join/Prune Messages per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('joinPruneMessagePerInterval')

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
	def RegisterMessagePerInterval(self):
		"""Register Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerMessagePerInterval')

	@property
	def RegisterStopMessagePerInterval(self):
		"""Register Stop Messages Per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerStopMessagePerInterval')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	def get_device_ids(self, PortNames=None, BootstrapMessagePerInterval=None, CRpAdvertiseMessagePerInterval=None, DiscardJoinPruneProcessing=None, EnableRateControl=None, HelloMessagePerInterval=None, Interval=None, JoinPruneMessagePerInterval=None, RegisterMessagePerInterval=None, RegisterStopMessagePerInterval=None):
		"""Base class infrastructure that gets a list of pimRouter device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BootstrapMessagePerInterval (str): optional regex of bootstrapMessagePerInterval
			CRpAdvertiseMessagePerInterval (str): optional regex of cRpAdvertiseMessagePerInterval
			DiscardJoinPruneProcessing (str): optional regex of discardJoinPruneProcessing
			EnableRateControl (str): optional regex of enableRateControl
			HelloMessagePerInterval (str): optional regex of helloMessagePerInterval
			Interval (str): optional regex of interval
			JoinPruneMessagePerInterval (str): optional regex of joinPruneMessagePerInterval
			RegisterMessagePerInterval (str): optional regex of registerMessagePerInterval
			RegisterStopMessagePerInterval (str): optional regex of registerStopMessagePerInterval

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
