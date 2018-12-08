
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


class CMacRange(Base):
	"""The CMacRange class encapsulates a user managed cMacRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CMacRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'cMacRange'

	def __init__(self, parent):
		super(CMacRange, self).__init__(parent)

	@property
	def CMacMappedIp(self):
		"""An instance of the CMacMappedIp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacmappedip.CMacMappedIp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacmappedip import CMacMappedIp
		return CMacMappedIp(self)

	@property
	def CmacRouteAttributes(self):
		"""An instance of the CmacRouteAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrouteattributes.CmacRouteAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrouteattributes import CmacRouteAttributes
		return CmacRouteAttributes(self)._select()

	@property
	def CmacPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cmacPrefixLength')
	@CmacPrefixLength.setter
	def CmacPrefixLength(self, value):
		self._set_attribute('cmacPrefixLength', value)

	@property
	def CvlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cvlanId')
	@CvlanId.setter
	def CvlanId(self, value):
		self._set_attribute('cvlanId', value)

	@property
	def CvlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cvlanPriority')
	@CvlanPriority.setter
	def CvlanPriority(self, value):
		self._set_attribute('cvlanPriority', value)

	@property
	def CvlanTpId(self):
		"""

		Returns:
			str(0x8100|0x9100|0x9200|0x88A8)
		"""
		return self._get_attribute('cvlanTpId')
	@CvlanTpId.setter
	def CvlanTpId(self, value):
		self._set_attribute('cvlanTpId', value)

	@property
	def EnableCvlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCvlan')
	@EnableCvlan.setter
	def EnableCvlan(self, value):
		self._set_attribute('enableCvlan', value)

	@property
	def EnableSecondLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSecondLabel')
	@EnableSecondLabel.setter
	def EnableSecondLabel(self, value):
		self._set_attribute('enableSecondLabel', value)

	@property
	def EnableSvlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSvlan')
	@EnableSvlan.setter
	def EnableSvlan(self, value):
		self._set_attribute('enableSvlan', value)

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
	def FirstLabelStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('firstLabelStart')
	@FirstLabelStart.setter
	def FirstLabelStart(self, value):
		self._set_attribute('firstLabelStart', value)

	@property
	def LabelMode(self):
		"""

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelStep')
	@LabelStep.setter
	def LabelStep(self, value):
		self._set_attribute('labelStep', value)

	@property
	def NoOfCmacs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfCmacs')
	@NoOfCmacs.setter
	def NoOfCmacs(self, value):
		self._set_attribute('noOfCmacs', value)

	@property
	def SecondLabelStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('secondLabelStart')
	@SecondLabelStart.setter
	def SecondLabelStart(self, value):
		self._set_attribute('secondLabelStart', value)

	@property
	def StartCmacPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startCmacPrefix')
	@StartCmacPrefix.setter
	def StartCmacPrefix(self, value):
		self._set_attribute('startCmacPrefix', value)

	@property
	def SvlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('svlanId')
	@SvlanId.setter
	def SvlanId(self, value):
		self._set_attribute('svlanId', value)

	@property
	def SvlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('svlanPriority')
	@SvlanPriority.setter
	def SvlanPriority(self, value):
		self._set_attribute('svlanPriority', value)

	@property
	def SvlanTpId(self):
		"""

		Returns:
			str(0x8100|0x9100|0x9200|0x88A8)
		"""
		return self._get_attribute('svlanTpId')
	@SvlanTpId.setter
	def SvlanTpId(self, value):
		self._set_attribute('svlanTpId', value)

	@property
	def UseSameSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useSameSequenceNumber')
	@UseSameSequenceNumber.setter
	def UseSameSequenceNumber(self, value):
		self._set_attribute('useSameSequenceNumber', value)

	def add(self, CmacPrefixLength=None, CvlanId=None, CvlanPriority=None, CvlanTpId=None, EnableCvlan=None, EnableSecondLabel=None, EnableSvlan=None, Enabled=None, FirstLabelStart=None, LabelMode=None, LabelStep=None, NoOfCmacs=None, SecondLabelStart=None, StartCmacPrefix=None, SvlanId=None, SvlanPriority=None, SvlanTpId=None, UseSameSequenceNumber=None):
		"""Adds a new cMacRange node on the server and retrieves it in this instance.

		Args:
			CmacPrefixLength (number): 
			CvlanId (number): 
			CvlanPriority (number): 
			CvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			EnableCvlan (bool): 
			EnableSecondLabel (bool): 
			EnableSvlan (bool): 
			Enabled (bool): 
			FirstLabelStart (number): 
			LabelMode (str(fixed|increment)): 
			LabelStep (number): 
			NoOfCmacs (number): 
			SecondLabelStart (number): 
			StartCmacPrefix (str): 
			SvlanId (number): 
			SvlanPriority (number): 
			SvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			UseSameSequenceNumber (bool): 

		Returns:
			self: This instance with all currently retrieved cMacRange data using find and the newly added cMacRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the cMacRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CmacPrefixLength=None, CvlanId=None, CvlanPriority=None, CvlanTpId=None, EnableCvlan=None, EnableSecondLabel=None, EnableSvlan=None, Enabled=None, FirstLabelStart=None, LabelMode=None, LabelStep=None, NoOfCmacs=None, SecondLabelStart=None, StartCmacPrefix=None, SvlanId=None, SvlanPriority=None, SvlanTpId=None, UseSameSequenceNumber=None):
		"""Finds and retrieves cMacRange data from the server.

		All named parameters support regex and can be used to selectively retrieve cMacRange data from the server.
		By default the find method takes no parameters and will retrieve all cMacRange data from the server.

		Args:
			CmacPrefixLength (number): 
			CvlanId (number): 
			CvlanPriority (number): 
			CvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			EnableCvlan (bool): 
			EnableSecondLabel (bool): 
			EnableSvlan (bool): 
			Enabled (bool): 
			FirstLabelStart (number): 
			LabelMode (str(fixed|increment)): 
			LabelStep (number): 
			NoOfCmacs (number): 
			SecondLabelStart (number): 
			StartCmacPrefix (str): 
			SvlanId (number): 
			SvlanPriority (number): 
			SvlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			UseSameSequenceNumber (bool): 

		Returns:
			self: This instance with matching cMacRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of cMacRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the cMacRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ReadvertiseCmac(self):
		"""Executes the readvertiseCmac operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=cMacRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ReadvertiseCmac', payload=locals(), response_object=None)
