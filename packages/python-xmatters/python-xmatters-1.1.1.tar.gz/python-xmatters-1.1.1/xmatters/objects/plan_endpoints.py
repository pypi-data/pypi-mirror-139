import xmatters.objects.common
import xmatters.objects.plans
from xmatters.connection import ApiBase
import xmatters.factories


class ServiceAuthentication(ApiBase):
    def __init__(self, parent, data):
        super(ServiceAuthentication, self).__init__(parent, data)
        self.username = data.get('username')    #: :vartype: str
        self.connection_status = data.get('connectionStatus')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class BasicAuthentication(ApiBase):
    def __init__(self, parent, data):
        super(BasicAuthentication, self).__init__(parent, data)
        self.username = data.get('username')   #: :vartype: str
        self.password = data.get('password')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OAuth2Authentication(ApiBase):
    def __init__(self, parent, data):
        super(OAuth2Authentication, self).__init__(parent, data)
        self.username = data.get('username')    #: :vartype: str
        self.oauth_token_url = data.get('oauthTokenUrl')   #: :vartype: str
        self.oauth_client_id = data.get('oauthClientId')    #: :vartype: str
        self.client_secret = data.get('client_secret')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Endpoint(ApiBase):
    def __init__(self, parent, data):
        super(Endpoint, self).__init__(parent, data)
        self.id = data.get('id')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
        self.url = data.get('url')   #: :vartype: str
        self.endpoint_type = data.get('endpointType')   #: :vartype: str
        self.authentication_type = data.get('authenticationType')   #: :vartype: str
        auth = data.get('authentication')
        self.authentication = xmatters.factories.AuthFactory.construct(self, data) if auth else None    #: :vartype: :class:`~xmatters.factories.AuthFactory`
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, data) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.trust_self_signed = data.get('trustSelfSigned')    #: :vartype: bool
        self.preemptive = data.get('preemptive')   #: :vartype: bool
        self.data = data.get('data')   #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
