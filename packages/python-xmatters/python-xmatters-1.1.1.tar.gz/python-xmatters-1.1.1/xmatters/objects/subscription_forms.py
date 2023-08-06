import xmatters.factories
import xmatters.objects.forms
import xmatters.utils
import xmatters.connection
import xmatters.objects.plans
import xmatters.objects.roles
from xmatters.objects.common import SelfLink
from xmatters.utils import Pagination


class SubscriptionForm(xmatters.connection.ApiBase):
    _endpoints = {'target_device_names': '?embed=deviceNames',
                  'visible_target_device_names': '?embed=deviceNames',
                  'property_definitions': '?embed=propertyDefinitions',
                  'roles': '?embed=roles'}

    def __init__(self, parent, data):
        super(SubscriptionForm, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        self.description = data.get('description')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, data) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
        self.scope = data.get('scope')    #: :vartype: str
        form = data.get('form')
        self.form = xmatters.objects.forms.FormReference(self, form) if form else None    #: :vartype: :class:`~xmatters.objects.forms.FormReference`
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.one_way = data.get('oneWay')    #: :vartype: bool
        self.subscribe_others = data.get('subscribeOthers')    #: :vartype: bool
        self.notification_delay = data.get('notificationDelay')   #: :vartype: int
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def target_device_names(self):
        url = self._get_url(self._endpoints.get('target_device_names'))
        data = self.con.get(url)
        tdns = data.get('targetDeviceNames', {})
        return Pagination(self, tdns, xmatters.factories.DeviceNameFactory) if tdns.get('data') else []

    @property
    def visible_target_device_names(self):
        url = self._get_url(self._endpoints.get('visible_target_device_names'))
        data = self.con.get(url)
        vtdns = data.get('visibleTargetDeviceNames', {})
        return Pagination(self, vtdns, xmatters.factories.DeviceNameFactory) if vtdns.get('data') else []

    @property
    def property_definitions(self):
        url = self._get_url(self._endpoints.get('property_definitions'))
        data = self.con.get(url)
        ps = data.get('propertyDefinitions', {})
        return Pagination(self, ps, xmatters.factories.PropertiesFactory) if ps.get('data') else []

    @property
    def roles(self):
        url = self._get_url(self._endpoints.get('roles'))
        data = self.con.get(url).get('roles')
        roles = data.get('roles')
        return Pagination(self, roles, xmatters.objects.roles.Role) if roles else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormReference(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(SubscriptionFormReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
