import xmatters.utils as util
from xmatters.objects.common import Recipient
from xmatters.objects.people import PersonReference
from xmatters.connection import ApiBase
import xmatters.objects.events as events


class Notification(ApiBase):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')    #:
        self.category = data.get('category')    #:
        recipient = data.get('recipient')  #:
        self.recipient = Recipient(parent, recipient) if recipient else None    #: :vartype: :class:`~xmatters.objects.common.Recipient`
        self.delivery_status = data.get('deliveryStatus')    #:
        created = data.get('created')  #:
        self.created = util.TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        event = data.get('event')  #:
        self.event = events.EventReference(parent, event) if event else None    #: :vartype: :class:`~xmatters.objects.events.EventReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Response(ApiBase):
    def __init__(self, parent, data):
        super(Response, self).__init__(parent, data)
        self.comment = data.get('comment')    #:
        notification = data.get('notification')  #:
        self.notification = Notification(self, notification) if notification else None    #: :vartype: :class:`~xmatters.objects.events.Notification`
        options = data.get('options', {}).get('data')  #:
        self.options = [events.ResponseOption(self, r) for r in options] if options else None    #: :vartype: [:class:`~xmatters.objects.events.ResponseOption`]
        self.source = data.get('source')    #:
        received = data.get('received')  #:
        self.received = util.TimeAttribute(received) if received else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.response = data.get('response')    #:

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditBase(ApiBase):
    def __init__(self, parent, data):
        super(AuditBase, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.type = data.get('type')    #: :vartype: str
        self.order_id = data.get('orderId')    #: :vartype: int
        at = data.get('at')  #:
        self.at = util.TimeAttribute(at) if at else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class Audit(AuditBase):
    def __init__(self, parent, data):
        super(Audit, self).__init__(parent, data)

        event = data.get('event')  #:
        self.event = events.EventReference(parent, event) if event else None    #: :vartype: :class:`~xmatters.objects.events.EventReference`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class Annotation(ApiBase):
    def __init__(self, parent, data):
        super(Annotation, self).__init__(parent, data)
        event = data.get('event')
        self.event = events.EventReference(parent, event) if event else None    #: :vartype: :class:`~xmatters.objects.events.EventReference`
        author = data.get('author')
        self.author = PersonReference(parent, author) if author else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.comment = data.get('comment')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditNotification(AuditBase):
    def __init__(self, parent, data):
        super(AuditNotification, self).__init__(parent, data)
        notification = data.get('notification')
        self.notification = Notification(self, notification) if notification else None    #: :vartype: :class:`~xmatters.objects.events.Notification`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditAnnotation(AuditBase):
    def __init__(self, parent, data):
        super(AuditAnnotation, self).__init__(parent, data)
        annotation = data.get('annotation')
        self.annotation = Annotation(self, annotation) if annotation else None    #: :vartype: :class:`~xmatters.objects.events.Annotation`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditResponse(AuditBase):
    def __init__(self, parent, data):
        super(AuditResponse, self).__init__(parent, data)
        response = data.get('response')
        self.response = Response(self, response) if response else None    #: :vartype: :class:`~xmatters.objects.audits.Response`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
