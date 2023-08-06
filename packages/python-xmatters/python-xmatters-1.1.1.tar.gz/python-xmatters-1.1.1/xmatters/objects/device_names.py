import xmatters.connection


class TargetDeviceNameSelector(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(TargetDeviceNameSelector, self).__init__(parent, data)
        self.name = data.get('name')  #: :vartype: str
        self.selected = data.get('selected')  #: :vartype: bool
        self.visible = data.get('visible')  #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceName(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(DeviceName, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.device_type = data.get('deviceType')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        self.privileged = data.get('privileged')  #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceNameEmail(DeviceName):
    def __init__(self, parent, data):
        super(DeviceNameEmail, self).__init__(parent, data)
        self.domains = data.get('domains', [])  #: :vartype: list

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()
