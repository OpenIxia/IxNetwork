from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupRange(Base):
	"""The GroupRange class encapsulates a user managed groupRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'groupRange'

	def __init__(self, parent):
		super(GroupRange, self).__init__(parent)

	@property
	def SourceRange(self):
		"""An instance of the SourceRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.sourcerange.sourcerange.SourceRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.sourcerange.sourcerange import SourceRange
		return SourceRange(self)

	@property
	def EnablePacking(self):
		"""If enabled, the user can specify the number of records per frame and sources per record.

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def EnableUpdateRequired(self):
		"""If true, updates the the changes to the Source IP addresses to take effect and to be displayed in the table.

		Returns:
			bool
		"""
		return self._get_attribute('enableUpdateRequired')
	@EnableUpdateRequired.setter
	def EnableUpdateRequired(self, value):
		self._set_attribute('enableUpdateRequired', value)

	@property
	def Enabled(self):
		"""Enables the use of the group range in the MLD simulation.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def GroupCount(self):
		"""The total number of IPv6 groups (Multicast Addresses) in this group range.

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupIpFrom(self):
		"""The IPv6 address of the first member of the Group (Multicast Address).

		Returns:
			str
		"""
		return self._get_attribute('groupIpFrom')
	@GroupIpFrom.setter
	def GroupIpFrom(self, value):
		self._set_attribute('groupIpFrom', value)

	@property
	def IncrementStep(self):
		"""The value used to increment the IPv6 address for each additional member of the group.

		Returns:
			number
		"""
		return self._get_attribute('incrementStep')
	@IncrementStep.setter
	def IncrementStep(self, value):
		self._set_attribute('incrementStep', value)

	@property
	def RecordsPerFrame(self):
		"""The total number of group records to be added to each frame/message.

		Returns:
			number
		"""
		return self._get_attribute('recordsPerFrame')
	@RecordsPerFrame.setter
	def RecordsPerFrame(self, value):
		self._set_attribute('recordsPerFrame', value)

	@property
	def SourceMode(self):
		"""Indicates whether the associated source range is a set of IP addresses to be included or excluded.

		Returns:
			str(include|exclude)
		"""
		return self._get_attribute('sourceMode')
	@SourceMode.setter
	def SourceMode(self, value):
		self._set_attribute('sourceMode', value)

	@property
	def SourcesPerRecord(self):
		"""The total number of sources to be added to each record.

		Returns:
			number
		"""
		return self._get_attribute('sourcesPerRecord')
	@SourcesPerRecord.setter
	def SourcesPerRecord(self, value):
		self._set_attribute('sourcesPerRecord', value)

	def add(self, EnablePacking=None, EnableUpdateRequired=None, Enabled=None, GroupCount=None, GroupIpFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None):
		"""Adds a new groupRange node on the server and retrieves it in this instance.

		Args:
			EnablePacking (bool): If enabled, the user can specify the number of records per frame and sources per record.
			EnableUpdateRequired (bool): If true, updates the the changes to the Source IP addresses to take effect and to be displayed in the table.
			Enabled (bool): Enables the use of the group range in the MLD simulation.
			GroupCount (number): The total number of IPv6 groups (Multicast Addresses) in this group range.
			GroupIpFrom (str): The IPv6 address of the first member of the Group (Multicast Address).
			IncrementStep (number): The value used to increment the IPv6 address for each additional member of the group.
			RecordsPerFrame (number): The total number of group records to be added to each frame/message.
			SourceMode (str(include|exclude)): Indicates whether the associated source range is a set of IP addresses to be included or excluded.
			SourcesPerRecord (number): The total number of sources to be added to each record.

		Returns:
			self: This instance with all currently retrieved groupRange data using find and the newly added groupRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the groupRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnablePacking=None, EnableUpdateRequired=None, Enabled=None, GroupCount=None, GroupIpFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None):
		"""Finds and retrieves groupRange data from the server.

		All named parameters support regex and can be used to selectively retrieve groupRange data from the server.
		By default the find method takes no parameters and will retrieve all groupRange data from the server.

		Args:
			EnablePacking (bool): If enabled, the user can specify the number of records per frame and sources per record.
			EnableUpdateRequired (bool): If true, updates the the changes to the Source IP addresses to take effect and to be displayed in the table.
			Enabled (bool): Enables the use of the group range in the MLD simulation.
			GroupCount (number): The total number of IPv6 groups (Multicast Addresses) in this group range.
			GroupIpFrom (str): The IPv6 address of the first member of the Group (Multicast Address).
			IncrementStep (number): The value used to increment the IPv6 address for each additional member of the group.
			RecordsPerFrame (number): The total number of group records to be added to each frame/message.
			SourceMode (str(include|exclude)): Indicates whether the associated source range is a set of IP addresses to be included or excluded.
			SourcesPerRecord (number): The total number of sources to be added to each record.

		Returns:
			self: This instance with matching groupRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateSource(self):
		"""Executes the updateSource operation on the server.

		Updates the source information for the group host for MLD.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=groupRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateSource', payload=locals(), response_object=None)
