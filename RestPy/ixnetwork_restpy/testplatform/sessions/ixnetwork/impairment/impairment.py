
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


class Impairment(Base):
	"""The Impairment class encapsulates a required impairment node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Impairment property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'impairment'

	def __init__(self, parent):
		super(Impairment, self).__init__(parent)

	@property
	def DefaultProfile(self):
		"""An instance of the DefaultProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.defaultprofile.DefaultProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.defaultprofile import DefaultProfile
		return DefaultProfile(self)._select()

	@property
	def Link(self):
		"""An instance of the Link class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.link.link.Link)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.link.link import Link
		return Link(self)

	@property
	def Profile(self):
		"""An instance of the Profile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.profile.Profile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.profile.profile import Profile
		return Profile(self)

	@property
	def Errors(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('errors')

	@property
	def State(self):
		"""

		Returns:
			str(applyingChanges|changesPending|errorOccurred|ready)
		"""
		return self._get_attribute('state')

	@property
	def Warnings(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('warnings')

	def Apply(self):
		"""Executes the apply operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/impairment)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Apply', payload=locals(), response_object=None)
