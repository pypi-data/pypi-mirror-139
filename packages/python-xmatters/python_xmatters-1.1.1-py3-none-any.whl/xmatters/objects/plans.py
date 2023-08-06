import xmatters.factories as factory
import xmatters.objects.forms
from xmatters.objects.plan_endpoints import Endpoint
from xmatters.connection import ApiBase
from xmatters.objects.common import SelfLink
from xmatters.utils import Pagination, TimeAttribute
from xmatters.objects.integrations import Integration
from xmatters.objects.people import Person
from xmatters.objects.plan_constants import PlanConstant
from xmatters.objects.shared_libraries import SharedLibrary
from xmatters.objects.subscription_forms import SubscriptionForm


class PlanPointer(ApiBase):
    def __init__(self, parent, data):
        super(PlanPointer, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlanReference(ApiBase):
    def __init__(self, parent, data):
        super(PlanReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Plan(ApiBase):
    _endpoints = {'creator': '?embed=creator',
                  'get_forms': '/forms',
                  'get_form_by_id': '/forms/{form_id}',
                  'get_integrations': '/integrations',
                  'get_integration_by_id': '/integrations/{int_id}',
                  'get_constants': '/constants',
                  'get_properties': '/property-definitions',
                  'get_libraries': '/shared-libraries',
                  'get_library_by_id': '/shared-libraries/{lib_id}',
                  'get_endpoints': '/endpoints',
                  'get_subscription_forms': '/subscription-forms',
                  'delete_constant': '/constants/{const_id}',
                  'delete_endpoints': '/endpoints/{end_id}',
                  'delete_property': '/property-definitions/{prop_id}'}

    def __init__(self, parent, data):
        super(Plan, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.plan_type = data.get('planType')    #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        self.enabled = data.get('enabled')   #: :vartype: bool
        self.editable = data.get('editable')    #: :vartype: bool
        self.logging_level = data.get('loggingLevel')   #: :vartype: str
        self.accessible = data.get('accessibleByAll')    #: :vartype: bool
        self.flood_control = data.get('floodControl')    #: :vartype: bool
        created = data.get('created')
        self.created = TimeAttribute(created) if created else None    #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.position = data.get('position')   #: :vartype: int

    @property
    def creator(self):
        """ Alias of :meth:`get_creator` """
        return self.get_creator()

    @property
    def constants(self):
        """ Alias of :meth:`get_constants` """
        return self.get_constants()

    @property
    def endpoints(self):
        """ Alias of :meth:`get_endpoints` """
        return self.get_endpoints()

    @property
    def forms(self):
        """ Alias of :meth:`get_forms` """
        return self.get_forms()

    @property
    def integrations(self):
        """ Alias of :meth:`get_integrations` """
        return self.get_integrations()

    @property
    def property_definitions(self):
        """ Alias of :meth:`get_properties` """
        return self.get_properties()

    def get_creator(self):
        """
        Get plan creator

        :return: Plan creator
        :rtype: :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url(self._endpoints.get('creator'))
        creator = self.con.get(url).get('creator')
        return Person(self, creator) if creator else None

    def get_forms(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_forms'))
        fs = self.con.get(url, params=params, **kwargs)
        return Pagination(self, fs, xmatters.objects.forms.Form) if fs.get('data') else []

    def get_form_by_id(self, form_id, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_form_by_id').format(form_id=form_id))
        data = self.con.get(url, params=params, **kwargs)
        return xmatters.objects.forms.Form(self, data) if data else None

    def create_form(self, data):
        url = self._get_url(self._endpoints.get('get_forms'))
        data = self.con.post(url, data=data)
        return xmatters.objects.forms.Form(self, data) if data else None

    def update_form(self, data):
        url = self._get_url(self._endpoints.get('get_forms'))
        data = self.con.post(url, data=data)
        return xmatters.objects.forms.Form(self, data) if data else None

    def get_constants(self):
        url = self._get_url(self._endpoints.get('get_constants'))
        constants = self.con.get(url)
        return Pagination(self, constants, PlanConstant) if constants.get('data') else []

    def create_constant(self, data):
        url = self._get_url(self._endpoints.get('get_constants'))
        data = self.con.post(url, data=data)
        return PlanConstant(self, data) if data else None

    def update_constant(self, data):
        url = self._get_url(self._endpoints.get('get_constants'))
        data = self.con.post(url, data=data)
        return PlanConstant(self, data) if data else None

    def delete_constant(self, constant_id):
        url = self._get_url(self._endpoints.get('delete_constant').format(const_id=constant_id))
        data = self.con.delete(url)
        return PlanConstant(self, data) if data else None

    def get_integrations(self, integration_type=None, deployed=None, **kwargs):
        params = {'integrationType': integration_type,
                  'deployed': deployed}

        url = self._get_url(self._endpoints.get('get_integrations'))
        ints = self.con.get(url, params=params, **kwargs)
        return Pagination(self, ints, Integration) if ints.get('data') else []

    def get_integration_by_id(self, integration_id):
        url = self._get_url(self._endpoints.get('get_integration_by_id').format(int_id=integration_id))
        data = self.con.get(url)
        return Integration(self, data) if data else None

    def create_integration(self, data):
        url = self._get_url(self._endpoints.get('get_integrations'))
        data = self.con.post(url, data=data)
        return Integration(self, data) if data else None

    def update_integration(self, data):
        url = self._get_url(self._endpoints.get('get_integrations'))
        data = self.con.post(url, data=data)
        return Integration(self, data) if data else None

    def delete_integration(self, integration_id):
        url = self._get_url(self._endpoints.get('get_integration_by_id').format(int_id=integration_id))
        data = self.con.delete(url)
        return Integration(self, data) if data else None

    def get_properties(self):
        url = self._get_url(self._endpoints.get('get_properties'))
        props = self.con.get(url)
        return Pagination(self, props, factory.PropertiesFactory) if props.get('data') else []

    def create_property(self, data):
        url = self._get_url(self._endpoints.get('get_properties'))
        data = self.con.post(url, data=data)
        return factory.PropertiesFactory.construct(self, data) if data else None

    def update_property(self, data):
        url = self._get_url(self._endpoints.get('get_properties'))
        data = self.con.post(url, data=data)
        return factory.PropertiesFactory.construct(self, data) if data else None

    def delete_property(self, property_id):
        url = self._get_url(self._endpoints.get('delete_property').format(prop_id=property_id))
        data = self.con.delete(url)
        return factory.PropertiesFactory.construct(self, data) if data else None

    def get_shared_libraries(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_libraries'))
        libs = self.con.get(url, params=params, **kwargs)
        return Pagination(self, libs, SharedLibrary) if libs.get('data') else []

    def get_shared_library_by_id(self, library_id):
        url = self._get_url(self._endpoints.get('get_library_by_id').format(lib_id=library_id))
        data = self.con.get(url)
        return SharedLibrary(self, data) if data else None

    def create_shared_library(self, data):
        url = self._get_url(self._endpoints.get('get_libraries'))
        data = self.con.post(url, data=data)
        return SharedLibrary(self, data) if data else None

    def update_shared_library(self, data):
        url = self._get_url(self._endpoints.get('get_libraries'))
        data = self.con.post(url, data=data)
        return SharedLibrary(self, data) if data else None

    def delete_shared_library(self, library_id):
        url = self._get_url(self._endpoints.get('get_library_by_id').format(lib_id=library_id))
        data = self.con.delete(url)
        return SharedLibrary(self, data) if data else None

    def get_endpoints(self):
        url = self._get_url(self._endpoints.get('get_endpoints'))
        endpoints = self.con.get(url)
        return Pagination(self, endpoints, xmatters.objects.plan_endpoints.Endpoint) if endpoints.get('data') else []

    def create_endpoint(self, data):
        url = self._get_url(self._endpoints.get('get_endpoints'))
        data = self.con.post(url, data=data)
        return xmatters.objects.plan_endpoints.Endpoint(self, data) if data else None

    def update_endpoint(self, data):
        url = self._get_url(self._endpoints.get('get_endpoints'))
        data = self.con.post(url, data=data)
        return xmatters.objects.plan_endpoints.Endpoint(self, data) if data else None

    def delete_endpoint(self, endpoint_id):
        url = self._get_url(self._endpoints.get('delete_endpoint').format(end_id=endpoint_id))
        data = self.con.delete(url)
        return xmatters.objects.plan_endpoints.Endpoint(self, data) if data else None

    def get_subscription_forms(self, params=None, **kwargs):
        url = self._get_url(self._endpoints.get('get_subscription_forms'))
        sub_forms = self.con.get(url, params=params, **kwargs)
        return Pagination(self, sub_forms, SubscriptionForm) if sub_forms.get('data') else []

    def create_subscription_form(self, data):
        url = self._get_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.post(url, data=data)
        return SubscriptionForm(self, data) if data else None

    def update_subscription_form(self, data):
        url = self._get_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.post(url, data=data)
        return SubscriptionForm(self, data) if data else None


    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()
