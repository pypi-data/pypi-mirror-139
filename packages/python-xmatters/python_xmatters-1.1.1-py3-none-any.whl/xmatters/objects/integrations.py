from xmatters.objects.common import ReferenceById, SelfLink
from xmatters.utils import Pagination, TimeAttribute
from xmatters.objects.people import PersonReference
import xmatters.objects.plan_endpoints
import xmatters.objects.plans
from xmatters.connection import ApiBase


class IntegrationReference(ApiBase):
    def __init__(self, parent, data):
        super(IntegrationReference, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IntegrationLog(ApiBase):
    def __init__(self, parent, data):
        super(IntegrationLog, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        integration = data.get('integration')
        self.integration = IntegrationReference(self, integration) if integration else None    #: :vartype: :class:`~xmatters.objects.integrations.IntegrationReference`
        completed = data.get('completed')
        self.completed = TimeAttribute(completed) if completed else None #: :vartype: :class:`~xmatters.utils.TimeAttribute`
        self.request_method = data.get('requestMethod')    #: :vartype: str
        self.request_headers = data.get('requestHeaders', {})    #: :vartype: dict
        self.request_parameters = data.get('requestParameters', {})     #: :vartype: dict
        self.request_body = data.get('requestBody')     #: :vartype: str
        self.remote_address = data.get('remoteAddress')     #: :vartype: str
        self.request_id = data.get('requestId')     #: :vartype: str
        self.status = data.get('status')    #: :vartype: str
        by = data.get('by')
        self.by = PersonReference(self, by) if by else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Integration(ApiBase):
    _endpoints = {'get_logs': '/logs'}

    def __init__(self, parent, data):
        super(Integration, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        plan = data.get('plan')
        self.plan = ReferenceById(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.common.ReferenceById`
        form = data.get('form')
        self.form = ReferenceById(self, form) if form else None    #: :vartype: :class:`~xmatters.objects.common.ReferenceById`
        self.name = data.get('name')    #: :vartype: str
        self.integration_type = data.get('integrationType')     #: :vartype: str
        self.operation = data.get('operation')    #: :vartype: str
        self.triggered_by = data.get('triggeredBy')     #: :vartype: str
        self.created_by = data.get('createdBy')    #: :vartype: str
        self.authentication_type = data.get('authenticationType')     #: :vartype: str
        endpoint = data.get('endpoint')
        self.endpoint = xmatters.objects.plan_endpoints.Endpoint(self, endpoint) if endpoint else None    #: :vartype: :class:`~xmatters.objects.plan_endpoints.Endpoint`
        self.deployed = data.get('deployed')    #: :vartype: bool
        self.script = data.get('script')    #: :vartype: str
        self.migrated_outbound_trigger = data.get('migratedOutboundTrigger')   #: :vartype: str
        self.origin_type = data.get('originType')   #: :vartype: str
        self.is_run_by_service_owner = data.get('isRunByServiceOwner')   #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
    
    def get_logs(self):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.integrations.IntegrationLog`
        """
        endpoint = self._get_url(self._endpoints.get('get_logs'))
        url = self._get_url(endpoint)
        logs = self.con.get(url)
        return Pagination(self, logs, IntegrationLog) if logs.get('data') else []

    @property
    def logs(self):
        """ Alias for :meth:`get_logs` """
        return self.get_logs()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()
