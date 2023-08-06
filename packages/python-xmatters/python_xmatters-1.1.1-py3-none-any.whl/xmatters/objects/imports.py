import xmatters.connection
from xmatters.objects.common import SelfLink
from xmatters.objects.people import PersonReference
from xmatters.utils import TimeAttribute


class ImportMessage(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(ImportMessage, self).__init__(parent, data)
        self.id = data.get('id')     #: :vartype: str
        self.message_level = data.get('messageLevel')    #: :vartype: str
        self.message_type = data.get('messageType')    #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        self.line = data.get('line')    #: :vartype: int

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.message_type)

    def __str__(self):
        return self.__repr__()


class Import(xmatters.connection.ApiBase):
    _endpoints = {'get_messages': '/import-messages'}

    def __init__(self, parent, data):
        super(Import, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')     #: :vartype: str
        self.transform = data.get('transform')    #: :vartype: str
        self.status = data.get('status')     #: :vartype: str
        started = data.get('started')
        self.started = TimeAttribute(started) if started else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        last_updated_at = data.get('lastUpdatedAt')
        self.last_updated_at = TimeAttribute(last_updated_at) if last_updated_at else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        by = data.get('by')
        self.by = PersonReference(parent, by) if by else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.total_count = data.get('totalCount')     #: :vartype: int
        self.processed_count = data.get('processedCount')     #: :vartype: int
        finished_at = data.get('finishedAt')
        self.finished_at = TimeAttribute(finished_at) if finished_at else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        links = data.get('links')
        self.links = SelfLink(parent, links)    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def get_messages(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_messages'))
        messages = self.con.get(url, params=params, **kwargs).get('data', None)
        return [ImportMessage(self, m) for m in messages] if messages else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()
