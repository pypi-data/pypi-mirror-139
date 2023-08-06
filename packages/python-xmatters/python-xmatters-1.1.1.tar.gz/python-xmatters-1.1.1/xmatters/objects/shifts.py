import xmatters.utils
import xmatters.connection
import xmatters.objects.common


class GroupReference(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(GroupReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.target_name = data.get('targetName')    #: :vartype: str
        self.recipient_type = data.get('recipientType')    #: :vartype: str
        self.group_type = data.get('groupType')    #: :vartype: str
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class End(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(End, self).__init__(parent, data)
        self.end_by = data.get('endBy')   #: :vartype: str
        date = data.get('date')
        self.date = xmatters.utils.TimeAttribute(date) if date else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.repetitions = data.get('repetitions')   #: :vartype: int

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Rotation(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Rotation, self).__init__(parent, data)
        self.type = data.get('type')   #: :vartype: str
        self.direction = data.get('direction')   #: :vartype: str
        self.interval = data.get('interval')   #: :vartype: int
        self.interval_unit = data.get('intervalUnit')    #: :vartype: str
        next_rotation_time = data.get('nextRotationTime')
        self.next_rotation_time = xmatters.utils.TimeAttribute(next_rotation_time) if next_rotation_time else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ShiftRecurrence(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(ShiftRecurrence, self).__init__(parent, data)
        self.frequency = data.get('frequency')    #: :vartype: str
        self.repeat_every = data.get('repeatEvery')    #: :vartype: str
        self.on_days = data.get('onDays', [])    #: :vartype: list
        self.on = data.get('on')    #: :vartype: str
        self.months = data.get('months', [])    #: :vartype: list
        self.data_on_month = data.get('dateOfMonth')   #: :vartype: str
        self.day_of_week_classifier = data.get('dayOfWeekClassifier')    #: :vartype: str
        self.day_of_week = data.get('dayOfWeek')   #: :vartype: str
        end = data.get('end')
        self.end = End(self, end) if end else None    #: :vartype: :class:`~xmatters.objects.shifts.End`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ShiftMember(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(ShiftMember, self).__init__(parent, data)
        self.position = data.get('position')    #: :vartype: int
        self.delay = data.get('delay')    #: :vartype: int
        self.escalation_type = data.get('escalationType')   #: :vartype: str
        self.in_rotation = data.get('inRotation')    #: :vartype: bool
        recipient = data.get('recipient')
        self.recipient = xmatters.objects.common.Recipient(self, recipient) if recipient else None    #: :vartype: :class:`~xmatters.objects.common.Recipient`
        shift = data.get('shift')
        self.shift = xmatters.objects.common.ReferenceByIdAndSelfLink(self, shift) if shift else None    #: :vartype: :class:`~xmatters.objects.common.ReferenceByIdAndSelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Shift(xmatters.connection.ApiBase):
    _endpoints = {'get_members': '/members'}

    def __init__(self, parent, data):
        super(Shift, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None    #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.name = data.get('name')   #: :vartype: str
        start = data.get('start')
        self.start = xmatters.utils.TimeAttribute(start) if start else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        end = data.get('end')
        self.end = xmatters.utils.TimeAttribute(end) if end else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.timezone = data.get('timezone')    #: :vartype: str
        recurrence = data.get('recurrence')
        self.recurrence = ShiftRecurrence(self, recurrence) if recurrence else None    #: :vartype: :class:`~xmatters.objects.shifts.ShiftRecurrence`

    @property
    def members(self):
        """ Alias of :meth:`get_members` """
        return self.get_members()

    def get_members(self):
        url = self._get_url(self._endpoints.get('get_members'))
        members = self.con.get(url)
        return xmatters.utils.Pagination(self, members, ShiftMember) if members.get('data') else []
    
    def add_member(self, data):
        url = self._get_url(self._endpoints.get('get_members'))
        data = self.con.post(url, data=data)
        return ShiftMember(self, data) if data else None

    def __repr__(self):
        return '<Shift {}>'.format(self.name)

    def __str__(self):
        return self.__repr__()
