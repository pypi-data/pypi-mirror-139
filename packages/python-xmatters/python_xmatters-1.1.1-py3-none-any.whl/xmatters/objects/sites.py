import xmatters.connection
import xmatters.objects.common


class Site(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Site, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.address1 = data.get('address1') #: :vartype: str
        self.address2 = data.get('address2') #: :vartype: str
        self.city = data.get('city')    #: :vartype: str
        self.country = data.get('country')    #: :vartype: str
        self.external_key = data.get('externalKey')    #: :vartype: str
        self.externally_owned = data.get('externallyOwned')    #: :vartype: bool
        self.language = data.get('language')    #: :vartype: str
        self.latitude = data.get('latitude')   #: :vartype: str
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`
        self.longitude = data.get('longitude')   #: :vartype: str
        self.name = data.get('name')   #: :vartype: str
        self.postal_code = data.get('postalCode')   #: :vartype: str
        self.state = data.get('state')    #: :vartype: str
        self.status = data.get('status')   #: :vartype: str
        self.timezone = data.get('timezone')    #: :vartype: str

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
