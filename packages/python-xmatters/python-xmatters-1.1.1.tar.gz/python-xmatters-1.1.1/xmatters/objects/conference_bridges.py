from xmatters.objects.common import SelfLink
import xmatters.connection


class ConferenceBridge(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(ConferenceBridge, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        self.toll_number = data.get('tollNumber')    #: :vartype: str
        self.toll_free_number = data.get('tollFreeNumber')    #: :vartype: str
        self.preferred_connection_type = data.get('preferredConnectionType')    #: :vartype: str
        self.pause_before_bridge_prompt = data.get('pauseBeforeBridgePrompt')    #: :vartype: int
        self.static_bridge_number = data.get('staticBridgeNumber')    #: :vartype: bool
        self.bridge_number = data.get('bridgeNumber')    #: :vartype: int
        self.dial_after_bridge = data.get('dialAfterBridge')    #: :vartype: str
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
