import xmatters.utils as util
import xmatters.factories
from xmatters.objects.common import SelfLink
from xmatters.utils import Pagination
from xmatters.connection import ApiBase
from xmatters.objects.shifts import GroupReference, Shift


class Replacer(ApiBase):
    def __init__(self, parent, data):
        super(Replacer, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.target_name = data.get('targetName')   #: :vartype: str
        self.recipient_type = data.get('recipientType')   #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.first_name = data.get('firstName')   #: :vartype: str
        self.last_name = data.get('lastName')    #: :vartype: str
        self.status = data.get('status')   #: :vartype: str

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftOccurrenceMember(ApiBase):
    def __init__(self, parent, data):
        super(ShiftOccurrenceMember, self).__init__(parent, data)
        member = data.get('member')
        self.member = xmatters.factories.RecipientFactory.construct(self, member) if member else None    #: :vartype: :class:`~xmatters.factories.RecipientFactory`
        self.position = data.get('position')   #: :vartype: int
        self.delay = data.get('delay')    #: :vartype: int
        self.escalation_type = data.get('escalationType')   #: :vartype: str
        replacements = data.get('replacements', {})
        self.replacements = Pagination(self, replacements, TemporaryReplacement) if replacements.get('data') else []    #: :vartype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.oncall.TemporaryReplacement`

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftReference(ApiBase):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.name = data.get('name')   #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class TemporaryReplacement(ApiBase):
    def __init__(self, parent, data):
        super(TemporaryReplacement, self).__init__(parent, data)
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        replacement = data.get('replacement')
        self.replacement = TemporaryReplacement(self, replacement) if replacement else None    #: :vartype: :class:`~xmatters.objects.oncall.TemporaryReplacement`


class OnCall(ApiBase):
    def __init__(self, parent, data):
        super(OnCall, self).__init__(parent)
        # save shift self link for use with 'shift' property to return full Shift object (not just ShiftReference)
        self._shift_link = data.get('shift', {}).get('links', {}).get('self')
        group = data.get('group')
        self.group = GroupReference(parent, group) if group else None    #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        members = data.get('members', {})
        self.members = Pagination(self, members, ShiftOccurrenceMember) if members.get('data') else []    #: :vartype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.oncall.ShiftOccurrenceMember`

    @property
    def shift(self):
        """ Alias for :meth:`get_shift` """
        return self.get_shift()

    def get_shift(self):
        if self._shift_link:
            url = '{}{}'.format(self.con.instance_url, self._shift_link)
            data = self.con.get(url)
            return Shift(self, data) if data else None
        else:
            return None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
