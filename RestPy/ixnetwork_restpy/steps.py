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


class Steps(Base):
    _SDM_NAME = 'nest'

    def __init__(self, parent):
        super(Steps, self).__init__(parent)        

    @property
    def Description(self):
        """The description of this step

        Returns:
            str: The description of the step
        """
        return self._get_attribute('description')

    @property
    def Owner(self):
        """The owner of this step

        Returns:
            str: The href of the owner
        """
        return self._get_attribute('owner')

    @property
    def Enabled(self):
        """Enable/disable the step

        Returns: 
            bool
        """
        return self._get_attribute('enabled')
    @Enabled.setter
    def Enabled(self, enabled):
        self._set_attribute('enabled', enabled)

    @property
    def Value(self):
        """The value of the step. This value must be in the same format as the parent multivalue

        Returns:
            str
        """
        return self._get_attribute('step')
    @Value.setter
    def Value(self, value):
        self._set_attribute('step', value)

