
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


class NetworkRange(Base):
	"""The NetworkRange class encapsulates a user managed networkRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetworkRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'networkRange'

	def __init__(self, parent):
		super(NetworkRange, self).__init__(parent)

	@property
	def EntryTe(self):
		"""An instance of the EntryTe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.entryte.EntryTe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.entryte import EntryTe
		return EntryTe(self)._select()

	@property
	def RangeTe(self):
		"""An instance of the RangeTe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rangete.RangeTe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rangete import RangeTe
		return RangeTe(self)._select()

	@property
	def EnableHostName(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

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
	def EntryCol(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryCol')
	@EntryCol.setter
	def EntryCol(self, value):
		self._set_attribute('entryCol', value)

	@property
	def EntryRow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def GridNodeRoutes(self):
		"""

		Returns:
			list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))
		"""
		return self._get_attribute('gridNodeRoutes')
	@GridNodeRoutes.setter
	def GridNodeRoutes(self, value):
		self._set_attribute('gridNodeRoutes', value)

	@property
	def GridOutsideExLinks(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))
		"""
		return self._get_attribute('gridOutsideExLinks')
	@GridOutsideExLinks.setter
	def GridOutsideExLinks(self, value):
		self._set_attribute('gridOutsideExLinks', value)

	@property
	def GridOutsideLinks(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))
		"""
		return self._get_attribute('gridOutsideLinks')
	@GridOutsideLinks.setter
	def GridOutsideLinks(self, value):
		self._set_attribute('gridOutsideLinks', value)

	@property
	def HostNamePrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostNamePrefix')
	@HostNamePrefix.setter
	def HostNamePrefix(self, value):
		self._set_attribute('hostNamePrefix', value)

	@property
	def InterfaceIps(self):
		"""

		Returns:
			list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))
		"""
		return self._get_attribute('interfaceIps')
	@InterfaceIps.setter
	def InterfaceIps(self, value):
		self._set_attribute('interfaceIps', value)

	@property
	def InterfaceMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def Ipv6MtMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MtMetric')
	@Ipv6MtMetric.setter
	def Ipv6MtMetric(self, value):
		self._set_attribute('ipv6MtMetric', value)

	@property
	def LinkType(self):
		"""

		Returns:
			str(pointToPoint|broadcast)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def NoOfCols(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def RouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def RouterIdIncrement(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerIdIncrement')
	@RouterIdIncrement.setter
	def RouterIdIncrement(self, value):
		self._set_attribute('routerIdIncrement', value)

	@property
	def TePaths(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))
		"""
		return self._get_attribute('tePaths')
	@TePaths.setter
	def TePaths(self, value):
		self._set_attribute('tePaths', value)

	@property
	def UseWideMetric(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useWideMetric')
	@UseWideMetric.setter
	def UseWideMetric(self, value):
		self._set_attribute('useWideMetric', value)

	def add(self, EnableHostName=None, Enabled=None, EntryCol=None, EntryRow=None, GridNodeRoutes=None, GridOutsideExLinks=None, GridOutsideLinks=None, HostNamePrefix=None, InterfaceIps=None, InterfaceMetric=None, Ipv6MtMetric=None, LinkType=None, NoOfCols=None, NoOfRows=None, RouterId=None, RouterIdIncrement=None, TePaths=None, UseWideMetric=None):
		"""Adds a new networkRange node on the server and retrieves it in this instance.

		Args:
			EnableHostName (bool): 
			Enabled (bool): 
			EntryCol (number): 
			EntryRow (number): 
			GridNodeRoutes (list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))): 
			GridOutsideExLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))): 
			GridOutsideLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))): 
			HostNamePrefix (str): 
			InterfaceIps (list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))): 
			InterfaceMetric (number): 
			Ipv6MtMetric (number): 
			LinkType (str(pointToPoint|broadcast)): 
			NoOfCols (number): 
			NoOfRows (number): 
			RouterId (str): 
			RouterIdIncrement (str): 
			TePaths (list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))): 
			UseWideMetric (bool): 

		Returns:
			self: This instance with all currently retrieved networkRange data using find and the newly added networkRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the networkRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableHostName=None, Enabled=None, EntryCol=None, EntryRow=None, GridNodeRoutes=None, GridOutsideExLinks=None, GridOutsideLinks=None, HostNamePrefix=None, InterfaceIps=None, InterfaceMetric=None, Ipv6MtMetric=None, LinkType=None, NoOfCols=None, NoOfRows=None, RouterId=None, RouterIdIncrement=None, TePaths=None, UseWideMetric=None):
		"""Finds and retrieves networkRange data from the server.

		All named parameters support regex and can be used to selectively retrieve networkRange data from the server.
		By default the find method takes no parameters and will retrieve all networkRange data from the server.

		Args:
			EnableHostName (bool): 
			Enabled (bool): 
			EntryCol (number): 
			EntryRow (number): 
			GridNodeRoutes (list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))): 
			GridOutsideExLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))): 
			GridOutsideLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))): 
			HostNamePrefix (str): 
			InterfaceIps (list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))): 
			InterfaceMetric (number): 
			Ipv6MtMetric (number): 
			LinkType (str(pointToPoint|broadcast)): 
			NoOfCols (number): 
			NoOfRows (number): 
			RouterId (str): 
			RouterIdIncrement (str): 
			TePaths (list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))): 
			UseWideMetric (bool): 

		Returns:
			self: This instance with matching networkRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of networkRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the networkRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
