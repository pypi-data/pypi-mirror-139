import xmatters.connection
import xmatters.objects.shifts


class Service(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Service, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.target_name = data.get('targetName')   #: :vartype: str
        self.recipients_type = data.get('recipientType')   #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        owned_by = data.get('ownedBy')
        self.owned_by = xmatters.objects.shifts.GroupReference(self, owned_by) if owned_by else None    #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
