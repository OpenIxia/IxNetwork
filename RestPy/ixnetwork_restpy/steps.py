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

