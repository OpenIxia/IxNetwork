from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Hops(Base):
	"""The Hops class encapsulates a system managed hops node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Hops property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'hops'

	def __init__(self, parent):
		super(Hops, self).__init__(parent)

	@property
	def DownStreamAddressInfo(self):
		"""This signifies the downstream Address information received in traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('downStreamAddressInfo')

	@property
	def DownStreamLabelsInfo(self):
		"""This signifies the downstream label stack received in traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('downStreamLabelsInfo')

	@property
	def DownStreamMultiPathInfo(self):
		"""This signifies the downstream Multipath information received in traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('downStreamMultiPathInfo')

	@property
	def DownStreamReturnCode(self):
		"""This signifies the downstream return code received in traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('downStreamReturnCode')

	@property
	def DownStreamReturnSubCode(self):
		"""This signifies the downstream return sub code received in traceroute echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('downStreamReturnSubCode')

	@property
	def ErrorTlvType(self):
		"""This signifies the Error TLV in received traceroute echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('errorTlvType')

	@property
	def InterfaceLabelStackTlvInterface(self):
		"""This signifies the inclusion of the Interface Id within Interface and Label Stack TLV in received traceroute echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('interfaceLabelStackTlvInterface')

	@property
	def InterfaceLabelStackTlvIpAddress(self):
		"""This signifies the inclusion of the IP Address within Interface and Label Stack TLV in received traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvIpAddress')

	@property
	def InterfaceLabelStackTlvLabels(self):
		"""This signifies the inclusion of the Label stack in Interface and Label Stack TLV in received traceroute echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvLabels')

	@property
	def ReturnCode(self):
		"""This signifies the return code in MPLS echo reply sent by traceroute hop.

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubcode(self):
		"""This signifies the return subcode in MPLS echo reply sent by traceroute hop.

		Returns:
			number
		"""
		return self._get_attribute('returnSubcode')

	@property
	def SrcIp(self):
		"""This signifies the source IP address.

		Returns:
			str
		"""
		return self._get_attribute('srcIp')

	@property
	def Ttl(self):
		"""This signifies the MPLS Time To Live value.

		Returns:
			number
		"""
		return self._get_attribute('ttl')

	def find(self, DownStreamAddressInfo=None, DownStreamLabelsInfo=None, DownStreamMultiPathInfo=None, DownStreamReturnCode=None, DownStreamReturnSubCode=None, ErrorTlvType=None, InterfaceLabelStackTlvInterface=None, InterfaceLabelStackTlvIpAddress=None, InterfaceLabelStackTlvLabels=None, ReturnCode=None, ReturnSubcode=None, SrcIp=None, Ttl=None):
		"""Finds and retrieves hops data from the server.

		All named parameters support regex and can be used to selectively retrieve hops data from the server.
		By default the find method takes no parameters and will retrieve all hops data from the server.

		Args:
			DownStreamAddressInfo (str): This signifies the downstream Address information received in traceroute echo reply message.
			DownStreamLabelsInfo (str): This signifies the downstream label stack received in traceroute echo reply message.
			DownStreamMultiPathInfo (str): This signifies the downstream Multipath information received in traceroute echo reply message.
			DownStreamReturnCode (str): This signifies the downstream return code received in traceroute echo reply message.
			DownStreamReturnSubCode (number): This signifies the downstream return sub code received in traceroute echo reply message.
			ErrorTlvType (number): This signifies the Error TLV in received traceroute echo reply message.
			InterfaceLabelStackTlvInterface (number): This signifies the inclusion of the Interface Id within Interface and Label Stack TLV in received traceroute echo reply message.
			InterfaceLabelStackTlvIpAddress (str): This signifies the inclusion of the IP Address within Interface and Label Stack TLV in received traceroute echo reply message.
			InterfaceLabelStackTlvLabels (str): This signifies the inclusion of the Label stack in Interface and Label Stack TLV in received traceroute echo reply message.
			ReturnCode (str): This signifies the return code in MPLS echo reply sent by traceroute hop.
			ReturnSubcode (number): This signifies the return subcode in MPLS echo reply sent by traceroute hop.
			SrcIp (str): This signifies the source IP address.
			Ttl (number): This signifies the MPLS Time To Live value.

		Returns:
			self: This instance with matching hops data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of hops data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the hops data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
