
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


class SessionLifetime(Base):
	"""The SessionLifetime class encapsulates a required sessionLifetime node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SessionLifetime property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'sessionLifetime'

	def __init__(self, parent):
		super(SessionLifetime, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def EnableLifetime(self):
		"""Enable session lifetime

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLifetime')

	@property
	def EnableRestart(self):
		"""Enable automatic session restart after stop at lifetime expiry

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRestart')

	@property
	def MaxLifetime(self):
		"""Maximum session lifetime (in seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLifetime')

	@property
	def MaxRestarts(self):
		"""Maximum number of times each session is automatically restarted

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxRestarts')

	@property
	def MinLifetime(self):
		"""Minimum session lifetime (in seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minLifetime')

	@property
	def RowNames(self):
		"""name of rows.

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def UnlimitedRestarts(self):
		"""Allow each session to always be automatically restarted

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unlimitedRestarts')

	def get_device_ids(self, PortNames=None, EnableLifetime=None, EnableRestart=None, MaxLifetime=None, MaxRestarts=None, MinLifetime=None, UnlimitedRestarts=None):
		"""Base class infrastructure that gets a list of sessionLifetime device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			EnableLifetime (str): optional regex of enableLifetime
			EnableRestart (str): optional regex of enableRestart
			MaxLifetime (str): optional regex of maxLifetime
			MaxRestarts (str): optional regex of maxRestarts
			MinLifetime (str): optional regex of minLifetime
			UnlimitedRestarts (str): optional regex of unlimitedRestarts

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
