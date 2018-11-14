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

import os


class Files(object):
	def __init__(self, file_path, local_file=True):
		"""Wraps access to /api/v1/sessions/<id>/ixnetwork/files functionality

		Use this class when a generated class has an method parameter with a type of (obj[Files]).

		Args:
			file_path (str): the name of the file and path if the file is local
			local_file (bool default[True]): 
				If True then the file_name will be uploaded to the server to its default file storage location 
				and will overwrite any existing file in that location.

		"""
		self._file_path = file_path
		self._file_name = os.path.basename(file_path)
		self._local_file = local_file
	
	@property
	def is_local_file(self):
		return self._local_file

	@property
	def file_path(self):
		return self._file_path

	@property
	def file_name(self):
		return self._file_name



