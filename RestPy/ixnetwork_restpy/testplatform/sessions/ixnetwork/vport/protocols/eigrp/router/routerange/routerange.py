
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


class RouteRange(Base):
	"""The RouteRange class encapsulates a user managed routeRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'routeRange'

	def __init__(self, parent):
		super(RouteRange, self).__init__(parent)

	@property
	def Bandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def Delay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('delay')
	@Delay.setter
	def Delay(self, value):
		self._set_attribute('delay', value)

	@property
	def DestCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destCount')
	@DestCount.setter
	def DestCount(self, value):
		self._set_attribute('destCount', value)

	@property
	def EnablePacking(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstRoute(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def Flag(self):
		"""

		Returns:
			str(externalRoute|candidateDefault)
		"""
		return self._get_attribute('flag')
	@Flag.setter
	def Flag(self, value):
		self._set_attribute('flag', value)

	@property
	def HopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('hopCount')
	@HopCount.setter
	def HopCount(self, value):
		self._set_attribute('hopCount', value)

	@property
	def Load(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('load')
	@Load.setter
	def Load(self, value):
		self._set_attribute('load', value)

	@property
	def Mask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Metric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NextHop(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NomberOfRoutes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nomberOfRoutes')
	@NomberOfRoutes.setter
	def NomberOfRoutes(self, value):
		self._set_attribute('nomberOfRoutes', value)

	@property
	def NumberOfRoutes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def OriginatingAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('originatingAs')
	@OriginatingAs.setter
	def OriginatingAs(self, value):
		self._set_attribute('originatingAs', value)

	@property
	def ProtocolId(self):
		"""

		Returns:
			str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)
		"""
		return self._get_attribute('protocolId')
	@ProtocolId.setter
	def ProtocolId(self, value):
		self._set_attribute('protocolId', value)

	@property
	def Reliability(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reliability')
	@Reliability.setter
	def Reliability(self, value):
		self._set_attribute('reliability', value)

	@property
	def RouteTag(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	@property
	def Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('source')
	@Source.setter
	def Source(self, value):
		self._set_attribute('source', value)

	@property
	def Type(self):
		"""

		Returns:
			str(external|internal)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, Bandwidth=None, Delay=None, DestCount=None, EnablePacking=None, Enabled=None, FirstRoute=None, Flag=None, HopCount=None, Load=None, Mask=None, Metric=None, Mtu=None, NextHop=None, NomberOfRoutes=None, NumberOfRoutes=None, OriginatingAs=None, ProtocolId=None, Reliability=None, RouteTag=None, Source=None, Type=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			Bandwidth (number): 
			Delay (number): 
			DestCount (number): 
			EnablePacking (bool): 
			Enabled (bool): 
			FirstRoute (str): 
			Flag (str(externalRoute|candidateDefault)): 
			HopCount (number): 
			Load (number): 
			Mask (number): 
			Metric (number): 
			Mtu (number): 
			NextHop (str): 
			NomberOfRoutes (number): 
			NumberOfRoutes (number): 
			OriginatingAs (number): 
			ProtocolId (str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)): 
			Reliability (number): 
			RouteTag (number): 
			Source (str): 
			Type (str(external|internal)): 

		Returns:
			self: This instance with all currently retrieved routeRange data using find and the newly added routeRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the routeRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Bandwidth=None, Delay=None, DestCount=None, EnablePacking=None, Enabled=None, FirstRoute=None, Flag=None, HopCount=None, Load=None, Mask=None, Metric=None, Mtu=None, NextHop=None, NomberOfRoutes=None, NumberOfRoutes=None, OriginatingAs=None, ProtocolId=None, Reliability=None, RouteTag=None, Source=None, Type=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			Bandwidth (number): 
			Delay (number): 
			DestCount (number): 
			EnablePacking (bool): 
			Enabled (bool): 
			FirstRoute (str): 
			Flag (str(externalRoute|candidateDefault)): 
			HopCount (number): 
			Load (number): 
			Mask (number): 
			Metric (number): 
			Mtu (number): 
			NextHop (str): 
			NomberOfRoutes (number): 
			NumberOfRoutes (number): 
			OriginatingAs (number): 
			ProtocolId (str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)): 
			Reliability (number): 
			RouteTag (number): 
			Source (str): 
			Type (str(external|internal)): 

		Returns:
			self: This instance with matching routeRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of routeRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the routeRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
