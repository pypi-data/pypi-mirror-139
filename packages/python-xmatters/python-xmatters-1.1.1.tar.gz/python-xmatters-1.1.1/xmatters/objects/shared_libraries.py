import xmatters.objects.plans
import xmatters.connection


class SharedLibrary(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(SharedLibrary, self).__init__(parent, data)
        self.id = data.get('id')  #: :vartype: str
        self.name = data.get('name')  #: :vartype: str
        self.script = data.get('script')  #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(self, plan) if plan else None  #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
