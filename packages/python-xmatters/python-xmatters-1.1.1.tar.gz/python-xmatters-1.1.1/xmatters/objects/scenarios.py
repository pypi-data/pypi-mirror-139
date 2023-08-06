import xmatters.objects.events
import xmatters.objects.forms
import xmatters.factories as factory
import xmatters.utils
import xmatters.connection
import xmatters.objects.people
import xmatters.objects.plans
import xmatters.objects.roles

from xmatters.objects.common import SelfLink
from xmatters.utils import Pagination


class ScenarioPermission(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(ScenarioPermission, self).__init__(parent, data)
        self.permissible_type = data.get('permissibleType')  #: :vartype: str
        self.editor = data.get('editor')  #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionPerson(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionPerson, self).__init__(parent, data)
        person = data.get('person')
        self.person = xmatters.objects.people.PersonReference(self,
                                                              person) if person else None  #: :vartype: :class:`~xmatters.objects.people.PersonReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionRole(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionRole, self).__init__(parent, data)
        role = data.get('role')
        self.role = xmatters.objects.roles.Role(self,
            role) if role else None  #: :vartype: :class:`~xmatters.objects.roles.Role`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Scenario(xmatters.connection.ApiBase):
    _endpoints = {'properties': '?embed=properties',
                  'plan': '?embed=properties',
                  'form': '?embed=form',
                  'properties_translations': '?embed=properties.translations'}

    def __init__(self, parent, data):
        super(Scenario, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        self.description = data.get('description')  #: :vartype: str
        self.priority = data.get('priority')  #: :vartype: str
        self.position = data.get('position')  #: :vartype: int
        self.bypass_phone_intro = data.get('bypassPhoneIntro')  #: :vartype: bool
        self.escalation_override = data.get('escalationOverride')  #: :vartype: bool
        self.expiration_in_minutes = data.get('expirationInMinutes')  #: :vartype: int
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')  #: :vartype: bool
        self.require_phone_password = data.get('requirePhonePassword')  #: :vartype: bool
        sos = data.get('senderOverrides')
        self.sender_overrides = xmatters.objects.forms.SenderOverrides(self, sos) if sos else None  #: :vartype: :class:`~xmatters.objects.forms.SenderOverrides`
        vm_opts = data.get('voicemailOptions')
        self.voicemail_options = xmatters.objects.events.VoicemailOptions(self,
            vm_opts) if vm_opts else None  #: :vartype: :class:`~xmatters.objects.events.VoicemailOptions`
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, factory.DeviceNameFactory) if tdns.get('data') else []  #: :vartype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.utils.DeviceNameFactory`
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None  #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        perm = data.get('permitted', {}).get('data')
        self.permitted = [factory.ScenarioPermFactory.construct(self, p) for p in perm] if perm else []  #: :vartype: [:class:`~xmatters.factories.ScenarioPermFactory.compose(self, p)]`
        rs = data.get('recipients')
        self.recipients = Pagination(self, rs, factory.RecipientFactory) if rs.get('data') else []  #: :vartype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.utils.RecipientFactory`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None  #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    @property
    def properties(self):
        """ Alias of :meth:`get_properties` """
        return self.get_properties()

    @property
    def plan(self):
        """ Alias of :meth:`get_plan` """
        return self.get_plan()

    @property
    def form(self):
        """ Alias of :meth:`get_form` """
        return self.get_form()

    @property
    def properties_translations(self):
        """ Alias of :meth:`get_properties_translations` """
        return self.get_properties_translations()

    def get_plan(self):
        url = self._get_url(self._endpoints.get('plan'))
        plan = self.con.get(url).get('plan', {})
        return xmatters.objects.plans.Plan(self, plan) if plan else None

    def get_form(self):
        url = self._get_url(self._endpoints.get('form'))
        form = self.con.get(url).get('form', {})
        return xmatters.objects.forms.Form(self, form) if form else None

    def get_properties_translations(self):
        url = self._get_url(self._endpoints.get('properties_translations'))
        data = self.con.get(url)
        return data.get('properties', {})

    def get_properties(self):
        url = self._get_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
