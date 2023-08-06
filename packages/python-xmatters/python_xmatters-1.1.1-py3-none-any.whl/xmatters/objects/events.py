import xmatters.factories
from xmatters.connection import ApiBase
from xmatters.objects.common import Recipient, SelfLink
from xmatters.objects.forms import FormReference
from xmatters.utils import Pagination, TimeAttribute
from xmatters.objects.event_suppressions import EventSuppression
from xmatters.objects.people import PersonReference
from xmatters.objects.plans import PlanReference


class Message(ApiBase):
    def __init__(self, parent, data):
        super(Message, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.message_type = data.get('messageType')    #: :vartype: str
        self.subject = data.get('subject')   #: :vartype: str
        self.body = data.get('body')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.subject)

    def __str__(self):
        return self.__repr__()


class UserDeliveryResponse(ApiBase):
    def __init__(self, parent, data):
        super(UserDeliveryResponse, self).__init__(parent, data)
        self.text = data.get('text')    #: :vartype: str
        self.notification = data.get('notification')  #: :vartype: str
        received = data.get('received')
        self.received = TimeAttribute(received) if received else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Conference(ApiBase):
    def __init__(self, parent, data):
        super(Conference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.bridge_id = data.get('bridgeId')   #: :vartype: str
        self.bridge_number = data.get('bridgeNumber')   #: :vartype: str
        self.type = data.get('type')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class VoicemailOptions(ApiBase):
    def __init__(self, parent, data):
        super(VoicemailOptions, self).__init__(parent, data)
        self.retry = data.get('retry')    #: :vartype: int
        self.every = data.get('every')    #: :vartype: int
        self.leave = data.get('leave')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Translation(ApiBase):
    def __init__(self, parent, data):
        super(Translation, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.language = data.get('language')   #: :vartype: str
        self.text = data.get('text')   #: :vartype: str
        self.prompt = data.get('prompt')   #: :vartype: str
        self.description = data.get('description')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ResponseOption(ApiBase):
    def __init__(self, parent, data):
        super(ResponseOption, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.number = data.get('number')    #: :vartype: int
        self.text = data.get('text')    #: :vartype: str
        self.description = data.get('description')   #: :vartype: str
        self.prompt = data.get('prompt')   #: :vartype: str
        self.action = data.get('action')   #: :vartype: str
        self.contribution = data.get('contribution')   #: :vartype: str
        self.join_conference = data.get('joinConference')    #: :vartype: bool
        self.allow_comments = data.get('allowComments')    #: :vartype: bool
        self.redirect_rul = data.get('redirectUrl')    #: :vartype: str
        translations = data.get('translations', {}).get('data', [])
        self.translations = [Translation(self, t) for t in translations]    #: :vartype: [:class:`~xmatters.objects.events.Translation`]

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferencePointer(ApiBase):
    def __init__(self, parent, data):
        super(ConferencePointer, self).__init__(parent, data)
        self.bridge_id = data.get('bridgeId')    #: :vartype: str
        self.type = data.get('type')   #: :vartype: str
        self.bridge_number = data.get('bridgeNumber')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventReference(ApiBase):
    def __init__(self, parent, data):
        super(EventReference, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.event_id = data.get('eventId')    #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Notification(ApiBase):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.recipient = Recipient(self, data.get('recipient'))    #: :vartype: :class:`~xmatters.objects.common.Recipient`
        created = data.get('created')
        self.created = TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        delivered = data.get('delivered')
        self.delivered = TimeAttribute(delivered) if delivered else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        responded = data.get('responded')
        self.responded = TimeAttribute(responded) if responded else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.delivery_status = data.get('deliveryStatus')    #: :vartype: str
        responses = data.get('responses')
        self.responses = [UserDeliveryResponse(self, r) for r in responses] if responses.get('data') else []    #: :vartype: [:class:`~xmatters.objects.events.UserDeliveryResponse`]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.recipient.target_name)

    def __str__(self):
        return self.__repr__()


class UserDeliveryData(ApiBase):
    def __init__(self, parent, data):
        super(UserDeliveryData, self).__init__(parent, data)
        event = data.get('event')
        self.event = EventReference(self, event) if event else None    #: :vartype: :class:`~xmatters.objects.events.EventReference`
        person = data.get('person')
        self.person = PersonReference(self, person) if person else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.delivery_status = data.get('deliveryStatus')   #: :vartype: str
        notifications = data.get('notifications', {}).get('data')
        self.notifications = [Notification(self, n) for n in notifications] if notifications else []    #: :vartype: [:class:`~xmatters.objects.events.Notification`]
        response = data.get('response')
        self.response = UserDeliveryResponse(self, response) if response else None    #: :vartype: :class:`~xmatters.objects.events.UserDeliveryResponse`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.person.target_name)

    def __str__(self):
        return self.__repr__()


class Annotation(ApiBase):
    def __init__(self, parent, data):
        super(Annotation, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        event = data.get('event')
        self.event = EventReference(self, event)    #: :vartype: :class:`~xmatters.objects.events.EventReference`
        author = data.get('author')
        self.author = PersonReference(self, author)    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.comment = data.get('comment')   #: :vartype: str
        created = data.get('created')
        self.created = TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Event(ApiBase):
    _endpoints = {'messages': '?embed=messages',
                  'get_annotations': '/annotations',
                  'get_annotation_by_id': '/annotations/{ann_id}',
                  'properties': '?embed=properties',
                  'recipients': '?embed=recipients',
                  'response_options': '?embed=responseOptions&responseOptions.translations',
                  'get_user_delivery_data': '/user-deliveries',
                  'get_audits': '{base_url}/audits',
                  'update_status': '{base_url}/events',
                  'targeted_recipients': '?embed=recipients&targeted=true',
                  'get_suppressions': '{base_url}/event-suppressions'}

    def __init__(self, parent, data):
        super(Event, self).__init__(parent, data)
        self.bypass_phone_intro = data.get('bypassPhoneIntro')   #: :vartype: bool
        created = data.get('created')
        self.created = TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        conference = data.get('conference')
        self.conference = Conference(self, conference) if conference else None    #: :vartype: :class:`~xmatters.objects.events.Conference`
        self.escalation_override = data.get('escalationOverride')   #: :vartype: bool
        self.event_id = data.get('eventId')  #: :vartype: str
        self.event_type = data.get('eventType')   #: :vartype: str
        self.expiration_in_minutes = data.get('expirationInMinutes')   #: :vartype: int
        self.flood_control = data.get('floodControl')   #: :vartype: bool
        plan = data.get('plan')
        self.plan = PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
        form = data.get('form')
        self.form = FormReference(self, form) if form else None    #: :vartype: :class:`~xmatters.objects.forms.FormReference`
        self.id = data.get('id')   #: :vartype: str
        self.incident = data.get('incident')   #: :vartype: str
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')   #: :vartype: bool
        self.other_response_count = data.get('otherResponseCount')    #: :vartype: int
        self.other_response_count_threshold = data.get('otherResponseCountThreshold')   #: :vartype: str
        self.priority = data.get('priority')   #: :vartype: str
        self.require_phone_password = data.get('requirePhonePassword')   #: :vartype: bool
        self.response_count_enabled = data.get('responseCountsEnabled')   #: :vartype: bool
        submitter = data.get('submitter')
        self.submitter = PersonReference(self, submitter) if submitter else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.status = data.get('status')   #: :vartype: str
        terminated = data.get('terminated')
        self.terminated = TimeAttribute(terminated) if terminated else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        voicemail_options = data.get('voicemailOptions')
        self.voicemail_options = VoicemailOptions(self, voicemail_options) if voicemail_options else None    #: :vartype: :class:`~xmatters.objects.events.VoicemailOptions`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def annotations(self):
        """ Alias of :meth:`get_annotations` """
        return self.get_annotations()

    @property
    def messages(self):
        """ Alias of :meth:`get_messages` """
        return self.get_messages()

    @property
    def properties(self):
        """ Alias of :meth:`get_properties` """
        return self.get_properties()

    @property
    def recipients(self):
        """ Alias of :meth:`get_recipients` """
        return self.get_recipients()

    @property
    def response_options(self):
        """ Alias of :meth:`get_response_options` """
        return self.get_response_options()

    @property
    def suppressions(self):
        """ Alias of :meth:`get_suppressions` """
        return self.get_suppressions()

    @property
    def targeted_recipients(self):
        """ Alias of :meth:`get_targeted_recipients` """
        return self.get_targeted_recipients()

    def get_recipients(self):
        url = self._get_url(self._endpoints.get('recipients'))
        data = self.con.get(url)
        recipients = data.get('recipients')
        return Pagination(self, recipients, Message) if recipients.get('data') else []

    def get_response_options(self):
        url = self._get_url(self._endpoints.get('response_options'))
        data = self.con.get(url)
        response_options = data.get('responseOptions', {}).get('data')
        return [ResponseOption(self, r) for r in response_options] if response_options else []

    def get_targeted_recipients(self):
        url = self._get_url(self._endpoints.get('targeted_recipients'))
        data = self.con.get(url)
        recipients = data.get('recipients')
        return Pagination(self, recipients, Message) if recipients.get('data') else []

    def get_properties(self):
        url = self._get_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    def get_messages(self):
        url = self._get_url(self._endpoints.get('messages'))
        data = self.con.get(url)
        messages = data.get('messages')
        return Pagination(self, messages, Message) if messages.get('data') else []

    def get_audits(self, params=None, **kwargs):
        url = self._endpoints.get('get_audits').format(base_url=self.con.api_base_url)
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.AuditFactory) if data.get('data') else []

    def get_user_delivery_data(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_user_delivery_data'))
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, UserDeliveryData) if data.get('data') else []

    def get_annotations(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_annotations'))
        data = self.con.get(url, params=params, **kwargs)
        annotations = data.get('annotations', {})
        return Pagination(self, annotations, Annotation) if annotations.get('data') else []

    def get_annotation_by_id(self, annotation_id):
        url = self._get_url(self._endpoints.get('get_annotation_by_id').format(ann_id=annotation_id))
        data = self.con.get(url)
        return Annotation(self, data) if data else None

    def add_annotation(self, data):
        url = self._get_url(self._endpoints.get('get_annotations'))
        data = self.con.post(url, data=data)
        return Annotation(self, data) if data else None

    def update_status(self, status):
        data = {'id': self.id,
                'status': status}

        url = self._endpoints.get('update_status').format(base_url=self.con.api_base_url)
        data = self.con.post(url, data=data)
        return Event(self, data) if data else None

    def get_suppressions(self, params=None, **kwargs):
        url = self._endpoints.get('get_suppressions').format(base_url=self.con.api_base_url)
        suppressions = self.con.get(url, params=params, **kwargs)
        return Pagination(self, suppressions, EventSuppression) if suppressions.get('data') else []

    def __repr__(self):
        return '<{} Created: {} Type: {}>'.format(self.__class__.__name__, self.created, self.event_type)

    def __str__(self):
        return self.__repr__()
