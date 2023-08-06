import xmatters.utils
import xmatters.objects.people
import xmatters.factories
import xmatters.connection
import xmatters.objects.oncall
import xmatters.objects.roles
import xmatters.objects.shifts
from xmatters.objects.common import SelfLink, RecipientReference, Recipient, ReferenceByIdAndSelfLink, \
    QuotaItem
from xmatters.utils import Pagination


class GroupMembershipShiftReference(xmatters.connection.ApiBase):
    """ Custom object for shift information embedded in a group membership response """

    def __int__(self, parent, data):
        super(GroupMembershipShiftReference, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        group = data.get('group')
        self.group = xmatters.objects.shifts.GroupReference(self,
                                                            group) if group else None  #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        self.name = data.get('name')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupMembership(xmatters.connection.ApiBase):
    _endpoints = {'shifts': '/groups/{group_id}/members?embed=shifts'}

    def __init__(self, parent, data):
        super(GroupMembership, self).__init__(parent, data)
        group = data.get('group')
        self.group = xmatters.objects.shifts.GroupReference(self,
                                                            group) if group else None  #: :vartype: :class:`~xmatters.objects.shifts.GroupReference`
        member = data.get('member')
        self.member = RecipientReference(self,
                                         member) if member else None  #: :vartype: :class:`~xmatters.objects.common.RecipientReference`
        shifts = data.get('shifts', {})
        self.shifts = Pagination(self, shifts, GroupMembershipShiftReference) if shifts.get(
            'data') else []  #: :vartype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.groups.GroupMembershipShiftReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Group(Recipient):
    _endpoints = {'get_supervisors': '/supervisors',
                  'get_oncall': '{base_url}/on-call?groups={group_id}',
                  'observers': '?embed=observers',
                  'get_shifts': '/shifts',
                  'add_member': '/members',
                  'delete_member': '/members/member_id',
                  'get_members': '/members?embed=shifts',
                  'get_shift_by_id': '/shifts/{shift_id}'}

    def __init__(self, parent, data):
        super(Group, self).__init__(parent, data)
        self.allow_duplicates = data.get('allowDuplicates')  #: :vartype: bool
        self.description = data.get('description')  #: :vartype: str
        self.observed_by_all = data.get('observedByAll')  #: :vartype: bool
        self.response_count = data.get('responseCount')  #: :vartype: int
        self.response_count_threshold = data.get('responseCount')  #: :vartype: str
        self.use_default_devices = data.get('responseCountThreshold')  #: :vartype: bool
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(
            created) if created else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.group_type = data.get('groupType')  #: :vartype: str
        site = data.get('site')
        self.site = ReferenceByIdAndSelfLink(self,
                                             site) if site else None  #: :vartype: :class:`~xmatters.objects.common.ReferenceByIdAndSelfLink`
        self.services = data.get('services', [])  #: :vartype: list

    @property
    def observers(self):
        """ Alias of :meth:`get_observers` """
        return self.get_observers()

    @property
    def supervisors(self):
        """ Alias of :meth:`get_supervisors` """
        return self.get_supervisors()

    def get_observers(self):
        url = self._get_url(self._endpoints.get('observers'))
        observers = self.con.get(url).get('observers', {}).get('data')
        return [xmatters.objects.roles.Role(self, role) for role in observers] if observers else []

    def get_supervisors(self):
        url = self._get_url(self._endpoints.get('get_supervisors'))
        data = self.con.get(url)
        return Pagination(self, data, xmatters.objects.people.Person) if data.get('data') else []

    def get_oncall(self, params=None, **kwargs):
        url = self._endpoints.get('get_oncall').format(base_url=self.con.api_base_url, group_id=self.id)
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.objects.oncall.OnCall) if data.get('data') else []

    def get_shifts(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_shifts'))
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.objects.shifts.Shift) if data.get('data') else []

    def get_shift_by_id(self, shift_id, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_shift_by_id').format(shift_id=shift_id))
        data = self.con.get(url, params=params, **kwargs)
        return xmatters.objects.shifts.Shift(self, data) if data else None

    def create_shift(self, data):
        url = self._get_url(self._endpoints.get('get_shifts'))
        data = self.con.post(url, data=data)
        return xmatters.objects.shifts.Shift(self, data) if data else None

    def delete_shift(self, shift_id):
        url = self._get_url(self._endpoints.get('get_shift_by_id').format(shift_id=shift_id))
        data = self.con.delete(url)
        return xmatters.objects.shifts.Shift(self, data) if data else None

    def get_members(self):
        url = self._get_url(self._endpoints.get('get_members'))
        data = self.con.get(url)
        return Pagination(self, data, GroupMembership) if data.get('data') else []

    def add_member(self, data):
        url = self._get_url(self._endpoints.get('add_member'))
        data = self.con.post(url, data=data)
        return xmatters.factories.RecipientFactory.construct(self, data) if data else None

    def remove_member(self, member_id):
        url = self._get_url(self._endpoints.get('remove_member').format(member_id=member_id))
        data = self.con.delete(url)
        return GroupMembership(self, data) if data else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class GroupQuota(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(GroupQuota, self).__init__(parent, data)
        self.group_quota_enabled = data.get('groupQuotaEnabled')  #: :vartype: bool
        groups = data.get('groups')
        self.stakeholder_users = QuotaItem(self, groups) if groups else None  #: :vartype: :class:`~xmatters.objects.common.QuotaItem`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
