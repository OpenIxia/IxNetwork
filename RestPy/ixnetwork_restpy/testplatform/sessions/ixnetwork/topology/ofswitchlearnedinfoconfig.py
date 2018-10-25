
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


class OFSwitchLearnedInfoConfig(Base):
	"""The OFSwitchLearnedInfoConfig class encapsulates a required oFSwitchLearnedInfoConfig node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OFSwitchLearnedInfoConfig property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'oFSwitchLearnedInfoConfig'

	def __init__(self, parent):
		super(OFSwitchLearnedInfoConfig, self).__init__(parent)

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
	def FlowStatOutGroupMode(self):
		"""Specify the Output Group Type. The options are: 1) All Groups 2) Any Group 3) Custom/Manual

		Returns:
			str(oFPGALL|oFPGANY|outGroupCustom)
		"""
		return self._get_attribute('flowStatOutGroupMode')
	@FlowStatOutGroupMode.setter
	def FlowStatOutGroupMode(self, value):
		self._set_attribute('flowStatOutGroupMode', value)

	@property
	def FlowStatOutGroupValue(self):
		"""If Out Group is Custom/Manual, type the output group value in the box provided

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutGroupValue')
	@FlowStatOutGroupValue.setter
	def FlowStatOutGroupValue(self, value):
		self._set_attribute('flowStatOutGroupValue', value)

	@property
	def FlowStatOutPortMode(self):
		"""Specify the Output Port Type. The options are: 1) OFPP_IN_PORT 2) OFPP_NORMAL 3) OFPP_FLOOD 4) OFPP_ALL 5) OFPP_CONTROLLER 6) OFPP_LOCAL 7) OFPP_ANY 8) Custom/Manual

		Returns:
			str(oFPP_ALL|oFPP_ANY|oFPP_CONTROLLER|oFPP_FLOOD|oFPP_IN_PORT|oFPP_LOCAL|oFPP_NORMAL|outPortCustom)
		"""
		return self._get_attribute('flowStatOutPortMode')
	@FlowStatOutPortMode.setter
	def FlowStatOutPortMode(self, value):
		self._set_attribute('flowStatOutPortMode', value)

	@property
	def FlowStatOutPortValue(self):
		"""If Out Port is Custom/Manual, type the output port value.

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutPortValue')
	@FlowStatOutPortValue.setter
	def FlowStatOutPortValue(self, value):
		self._set_attribute('flowStatOutPortValue', value)

	@property
	def FlowStatTableIdMode(self):
		"""The identifier of the table. The options are: 1) All Tables 2) Custom/Manual.

		Returns:
			str(tableIdAllTables|tableIdCustom)
		"""
		return self._get_attribute('flowStatTableIdMode')
	@FlowStatTableIdMode.setter
	def FlowStatTableIdMode(self, value):
		self._set_attribute('flowStatTableIdMode', value)

	@property
	def FlowStatTableIdValue(self):
		"""If Table ID is Custom/ Manual, type the Table ID Number

		Returns:
			number
		"""
		return self._get_attribute('flowStatTableIdValue')
	@FlowStatTableIdValue.setter
	def FlowStatTableIdValue(self, value):
		self._set_attribute('flowStatTableIdValue', value)

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
