
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


class DefaultProfile(Base):
	"""The DefaultProfile class encapsulates a required defaultProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DefaultProfile property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'defaultProfile'

	def __init__(self, parent):
		super(DefaultProfile, self).__init__(parent)

	@property
	def BitError(self):
		"""An instance of the BitError class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.biterror.biterror.BitError)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.biterror.biterror import BitError
		return BitError(self)._select()

	@property
	def Checksums(self):
		"""An instance of the Checksums class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.checksums.checksums.Checksums)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.checksums.checksums import Checksums
		return Checksums(self)._select()

	@property
	def CustomDelayVariation(self):
		"""An instance of the CustomDelayVariation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.customdelayvariation.customdelayvariation.CustomDelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.customdelayvariation.customdelayvariation import CustomDelayVariation
		return CustomDelayVariation(self)._select()

	@property
	def Delay(self):
		"""An instance of the Delay class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.delay.delay.Delay)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.delay.delay import Delay
		return Delay(self)._select()

	@property
	def DelayVariation(self):
		"""An instance of the DelayVariation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.delayvariation.delayvariation.DelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.delayvariation.delayvariation import DelayVariation
		return DelayVariation(self)._select()

	@property
	def Drop(self):
		"""An instance of the Drop class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.drop.drop.Drop)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.drop.drop import Drop
		return Drop(self)._select()

	@property
	def Duplicate(self):
		"""An instance of the Duplicate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.duplicate.duplicate.Duplicate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.duplicate.duplicate import Duplicate
		return Duplicate(self)._select()

	@property
	def Modifier(self):
		"""An instance of the Modifier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.modifier.modifier.Modifier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.modifier.modifier import Modifier
		return Modifier(self)

	@property
	def Reorder(self):
		"""An instance of the Reorder class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.reorder.reorder.Reorder)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.reorder.reorder import Reorder
		return Reorder(self)._select()

	@property
	def RxRateLimit(self):
		"""An instance of the RxRateLimit class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.rxratelimit.rxratelimit.RxRateLimit)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.rxratelimit.rxratelimit import RxRateLimit
		return RxRateLimit(self)._select()

	@property
	def Name(self):
		"""The name of the profile. Read-only.

		Returns:
			str
		"""
		return self._get_attribute('name')
