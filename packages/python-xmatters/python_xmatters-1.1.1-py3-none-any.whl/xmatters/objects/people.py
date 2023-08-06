import xmatters.factories
import xmatters.utils as utils
from xmatters.objects.common import Recipient, SelfLink, QuotaItem
from xmatters.utils import Pagination
from xmatters.objects.roles import Role
from xmatters.connection import ApiBase
import xmatters.objects.groups


class Person(Recipient):

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')  #: :vartype: str
        self.last_name = data.get('lastName')  #: :vartype: str
        self.license_type = data.get('licenseType')  #: :vartype: str
        self.language = data.get('language')  #: :vartype: str
        self.timezone = data.get('timezone')  #: :vartype: str
        self.web_login = data.get('webLogin')  #: :vartype: str
        self.phone_login = data.get('phoneLogin')  #: :vartype: str
        self.phone_pin = data.get('phonePin')  #: :vartype: str
        self.properties = data.get('properties', {})  #: :vartype: dict
        last_login = data.get('lastLogin')
        self.last_login = utils.TimeAttribute(
            last_login) if last_login else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        when_created = data.get('whenCreated')
        self.when_created = utils.TimeAttribute(
            when_created) if when_created else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        when_updated = data.get('whenUpdated')
        self.when_updated = utils.TimeAttribute(
            when_updated) if when_updated else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        links = data.get('links')
        self.links = SelfLink(self, data) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def full_name(self):
        """
        Get person's full name

        :return: person's full name
        :rtype: str
        """
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def roles(self):
        """ Alias for :meth:`get_roles` """
        return self.get_roles()

    @property
    def devices(self):
        """ Alias for :meth:`get_devices` """
        return self.get_devices()

    @property
    def supervisors(self):
        """ Alias for :meth:`get_supervisors` """
        return self.get_supervisors()

    def get_roles(self):
        url = self._get_url('?embed=roles')
        data = self.con.get(url)
        roles = data.get('roles', {})
        return Pagination(self, roles, Role) if roles.get('data') else []

    def get_supervisors(self, params=None, **kwargs):
        url = self._get_url('/supervisors')
        s = self.con.get(url, params=params, **kwargs)
        return Pagination(self, s, Person) if s.get('data') else []

    def get_devices(self, params=None, **kwargs):
        url = self._get_url('/devices')
        devices = self.con.get(url, params=params, **kwargs)
        return Pagination(self, devices, xmatters.factories.DeviceFactory) if devices.get('data') else []

    def get_groups(self, params=None, **kwargs):
        url = self._get_url('/group-memberships')
        groups = self.con.get(url, params=params, **kwargs)
        return Pagination(self, groups, xmatters.objects.groups.GroupMembership) if groups.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PersonReference(ApiBase):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.target_name = data.get('targetName')  #: :vartype: str
        self.first_name = data.get('firstName')  #: :vartype: str
        self.last_name = data.get('lastName')  #: :vartype: str
        self.recipient_type = data.get('recipientType')  #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def full_name(self):
        """
        :rtype: str
        """
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class UserQuota(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(UserQuota, self).__init__(parent, data)
        self.stakeholder_users_enabled = data.get('stakeholderUsersEnabled')  #: :vartype: bool
        stakeholder_users = data.get('stakeholderUsers')
        self.stakeholder_users = QuotaItem(self, stakeholder_users) if stakeholder_users else None  #: :vartype: :class:`~xmatters.objects.common.QuotaItem`
        full_users = data.get('fullUsers')
        self.full_users = QuotaItem(self, full_users) if full_users else None  #: :vartype: :class:`~xmatters.objects.common.QuotaItem`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
