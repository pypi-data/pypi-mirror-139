from xmatters.objects.common import SelfLink
from xmatters.connection import ApiBase
import xmatters.objects.events as events
import xmatters.utils as util


class EventFloodFilter(ApiBase):
    def __init__(self, parent, data):
        super(EventFloodFilter, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SuppressionMatch(ApiBase):
    def __init__(self, parent, data):
        super(SuppressionMatch, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.event_id = data.get('eventId')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppression(ApiBase):
    def __init__(self, parent, data):
        super(EventSuppression, self).__init__(parent, data)
        event = data.get('event')
        self.event = events.EventReference(self,
                                           event) if event else None  #: :vartype: :class:`~xmatters.objects.events.EventReference`
        match = data.get('match')
        self.match = SuppressionMatch(self,
                                      data) if match else None  #: :vartype: :class:`~xmatters.objects.event_suppressions.SuppressionMatch`
        at = data.get('at')
        self.at = util.TimeAttribute(at) if at else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        filters = data.get('filters', [])
        self.filter = [EventFloodFilter(self, f) for f in
                       filters]  #: :vartype: [:class:`~xmatters.objects.event_suppressions.EventFloodFilter`]
        self.links = SelfLink(self, data.get('links'))  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
