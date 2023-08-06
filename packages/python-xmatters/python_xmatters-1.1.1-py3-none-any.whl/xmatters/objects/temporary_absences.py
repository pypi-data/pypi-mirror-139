import xmatters.utils
import xmatters.objects.people
import xmatters.objects.shifts
import xmatters.connection


class TemporaryAbsence(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(TemporaryAbsence, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        self.absence_type = data.get('absenceType')   #: :vartype: str
        member = data.get('member')
        self.member = xmatters.objects.people.PersonReference(self, member) if member else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        start = data.get('start')
        self.start = xmatters.utils.TimeAttribute(start) if start else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        end = data.get('end')
        self.end = xmatters.utils.TimeAttribute(end) if end else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        group = data.get('group')
        self.group = xmatters.objects.shifts.GroupReference(self, group) if group else None    #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        replacement = data.get('replacement')
        self.replacement = xmatters.objects.people.PersonReference(self, replacement) if replacement else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()


