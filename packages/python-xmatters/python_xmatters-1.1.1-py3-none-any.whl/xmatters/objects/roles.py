import xmatters.connection

class Role(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Role, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        self.description = data.get('description')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


