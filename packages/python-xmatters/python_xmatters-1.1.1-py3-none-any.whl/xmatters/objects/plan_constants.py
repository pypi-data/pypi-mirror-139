import xmatters.objects.common
import xmatters.objects.plans
import xmatters.connection


class PlanConstant(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(PlanConstant, self).__init__(parent, data)
        self.id = data.get('id')    #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanPointer(self, plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanPointer`
        self.name = data.get('name')   #: :vartype: str
        self.value = data.get('value')    #: :vartype: str
        self.description = data.get('description')    #: :vartype: str
        links = data.get('links')
        self.links = xmatters.objects.common.SelfLink(self, links) if links else None    #: :vartype: :class:`~xmatters.objects.common.SelfLink`

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
