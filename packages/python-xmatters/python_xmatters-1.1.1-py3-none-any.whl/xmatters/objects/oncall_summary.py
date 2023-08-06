from xmatters import factories as factory
from xmatters.connection import ApiBase
from xmatters.objects.oncall import ShiftReference
from xmatters.objects.people import PersonReference
from xmatters.objects.shifts import GroupReference


class OnCallSummary(ApiBase):
    def __init__(self, parent, data):
        super(OnCallSummary, self).__init__(parent, data)
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None    #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        shift = data.get('shift')
        self.shift = ShiftReference(self, shift) if shift else None    #: :vartype: :class:`~xmatters.objects.oncall.ShiftReference`
        recipient = data.get('recipient')
        self.recipient = factory.RecipientFactory.construct(self, recipient) if recipient else None    #: :vartype: :class:`~xmatters.factories.RecipientFactory.compose`
        absence = data.get('absence')
        self.absence = PersonReference(self, absence) if absence else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.delay = data.get('delay')    #: :vartype: int
        self.escalation_level = data.get('escalationLevel')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


