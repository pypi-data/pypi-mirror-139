import xmatters.factories as factory
import xmatters.objects.forms
from xmatters.connection import ApiBase
from xmatters.utils import Pagination
from xmatters.objects.conference_bridges import ConferenceBridge
from xmatters.objects.device_types import DeviceTypes
from xmatters.objects.dynamic_teams import DynamicTeam
from xmatters.objects.event_suppressions import EventSuppression
from xmatters.objects.events import Event
from xmatters.objects.groups import Group, GroupQuota
from xmatters.objects.imports import Import
from xmatters.objects.incidents import Incident
from xmatters.objects.oncall import OnCall
from xmatters.objects.oncall_summary import OnCallSummary
from xmatters.objects.people import Person, UserQuota
from xmatters.objects.plans import Plan
from xmatters.objects.roles import Role
from xmatters.objects.scenarios import Scenario
from xmatters.objects.services import Service
from xmatters.objects.sites import Site
from xmatters.objects.subscription_forms import SubscriptionForm
from xmatters.objects.subscriptions import Subscription
from xmatters.objects.temporary_absences import TemporaryAbsence
from xmatters.objects.attachments import Attachments


class AttachmentsEndpoint(ApiBase):
    """ Used to interact with '/attachments' top-level endpoint """

    def __init__(self, parent):
        super(AttachmentsEndpoint, self).__init__(parent, endpoint='/attachments')

    def upload_attachment(self, data):
        """

        :rtype: :class:`~xmatters.objects.attachments.Attachments`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Attachments(self, data) if data else None


class AuditsEndpoint(ApiBase):
    """ Used to interact with '/audits' top-level endpoint """

    def __init__(self, parent):
        super(AuditsEndpoint, self).__init__(parent, endpoint='/audits')

    def get_audits(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.factories.AuditFactory`
        """
        url = self._get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.AuditFactory) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesEndpoint(ApiBase):
    """ Used to interact with '/devices' top-level endpoint """

    def __init__(self, parent):
        super(DevicesEndpoint, self).__init__(parent, endpoint='/devices')

    def get_devices(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, xmatters.factories.DeviceFactory) if data.get('data') else []

    def get_device_by_id(self, device_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url(device_id)
        data = self.con.get(url=url, params=params, **kwargs)
        return xmatters.factories.DeviceFactory.construct(self, data) if data else None

    def create_device(self, data):
        """

        :rtype: :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceFactory.construct(self, data) if data else None

    def update_device(self, data):
        """

        :rtype: :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url()
        data = self.con.post(url=url, data=data)
        return xmatters.factories.DeviceFactory.construct(self, data) if data else None

    def delete_device(self, device_id):
        """

        :rtype: :class:`~xmatters.factories.DeviceFactory`
        """
        url = self._get_url(device_id)
        data = self.con.delete(url=url)
        return xmatters.factories.DeviceFactory.construct(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNamesEndpoint(ApiBase):
    """ Used to interact with '/device-names' top-level endpoint """

    def __init__(self, parent):
        super(DeviceNamesEndpoint, self).__init__(parent, endpoint='/device-names')

    def get_device_names(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.factories.DeviceNameFactory`
        """
        url = self._get_url()
        data = self.con.get(url=url, params=params, **kwargs)
        return Pagination(self, data, factory.DeviceNameFactory) if data.get('data') else []

    def create_device_name(self, data):
        """

        :rtype: :class:`~xmatters.factories.DeviceNameFactory`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.construct(self, data) if data else None

    def update_device_name(self, data):
        """

        :rtype: :class:`~xmatters.factories.DeviceNameFactory`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.construct(self, data) if data else None

    def delete_device_name(self, device_name_id):
        """

        :rtype: :class:`~xmatters.factories.DeviceNameFactory`
        """
        url = self._get_url(device_name_id)
        data = self.con.delete(url)
        return xmatters.factories.DeviceNameFactory.construct(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceTypesEndpoint(ApiBase):

    def __init__(self, parent):
        super(DeviceTypesEndpoint, self).__init__(parent, endpoint='/device-types')

    def get_device_types(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.device_types.DeviceNameFactory`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return DeviceTypes(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DynamicTeamsEndpoint(ApiBase):

    def __init__(self, parent):
        super(DynamicTeamsEndpoint, self).__init__(parent, endpoint='/dynamic-teams')

    def get_dynamic_teams(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.dynamic_teams.DynamicTeam`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, DynamicTeam) if data.get('data') else []

    def get_dynamic_team_by_id(self, dynamic_team_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.dynamic_teams.DynamicTeam`
        """
        url = self._get_url(dynamic_team_id)
        data = self.con.get(url, params=params, **kwargs)
        return DynamicTeam(self, data) if data else None

    def create_dynamic_team(self, data):
        """

        :rtype: :class:`~xmatters.objects.dynamic_teams.DynamicTeam`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    def update_dynamic_team(self, data):
        """

        :rtype: :class:`~xmatters.objects.dynamic_teams.DynamicTeam`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    def delete_dynamic_team(self, dynamic_team_id):
        """

        :rtype: :class:`~xmatters.objects.dynamic_teams.DynamicTeam`
        """
        url = self._get_url(dynamic_team_id)
        data = self.con.delete(url=url)
        return DynamicTeam(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventsEndpoint(ApiBase):

    def __init__(self, parent):
        super(EventsEndpoint, self).__init__(parent, endpoint='/events')

    def get_events(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.events.Event`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Event) if data.get('data') else []

    def get_event_by_id(self, event_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.events.Event`
        """
        url = self._get_url(event_id)
        data = self.con.get(url, params=params, **kwargs)
        return Event(self, data) if data else None

    def change_event_status(self, data):
        """

        :rtype: :class:`~xmatters.objects.events.Event`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Event(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppressionsEndpoint(ApiBase):

    def __init__(self, parent):
        super(EventSuppressionsEndpoint, self).__init__(parent, endpoint='/event-suppressions')

    def get_suppressions_by_event_id(self, event_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.event_suppressions.EventSuppression`
        """
        url = self._get_url(event_id)
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, EventSuppression) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgesEndpoint(ApiBase):

    def __init__(self, parent):
        super(ConferenceBridgesEndpoint, self).__init__(parent, endpoint='/conference-bridges')

    def get_conference_bridges(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.conference_bridges.ConferenceBridge`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, ConferenceBridge) if data.get('data') else []

    def get_conference_bridge_by_id(self, bridge_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.conference_bridges.ConferenceBridge`
        """
        url = self._get_url(bridge_id)
        data = self.con.get(url, params=params, **kwargs)
        return ConferenceBridge(self, data) if data else None

    def create_conference_bridge(self, data):
        """

        :rtype: :class:`~xmatters.objects.conference_bridges.ConferenceBridge`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def update_conference_bridge(self, data):
        """

        :rtype: :class:`~xmatters.objects.conference_bridges.ConferenceBridge`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def delete_conference_bridge(self, bridge_id):
        """

        :rtype: :class:`~xmatters.objects.conference_bridges.ConferenceBridge`
        """
        url = self._get_url(bridge_id)
        data = self.con.delete(url=url)
        return ConferenceBridge(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormsEndpoint(ApiBase):

    def __init__(self, parent):
        super(FormsEndpoint, self).__init__(parent, endpoint='/forms')

    def get_forms(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.forms.Form`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, xmatters.objects.forms.Form) if data.get('data') else []

    def get_form_by_id(self, form_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.forms.Form`
        """
        url = self._get_url(form_id)
        data = self.con.get(url, params=params, **kwargs)
        return xmatters.objects.forms.Form(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupsEndpoint(ApiBase):

    def __init__(self, parent):
        super(GroupsEndpoint, self).__init__(parent, endpoint='/groups')

    def get_groups(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.groups.Group`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.groups.Group`
        """
        url = self._get_url(group_id)
        data = self.con.get(url, params=params, **kwargs)
        return Group(self, data) if data else None

    def get_license_quotas(self):
        """

        :rtype: :class:`~xmatters.objects.groups.GroupQuota`
        """
        url = self._get_url('/license-quotas')
        data = self.con.get(url)
        return GroupQuota(self, data) if data else None

    def create_group(self, data):
        """

        :rtype: :class:`~xmatters.objects.groups.Group`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    def update_group(self, data):
        """

        :rtype: :class:`~xmatters.objects.groups.Group`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    def delete_group(self, group_id):
        """

        :rtype: :class:`~xmatters.objects.groups.Group`
        """
        url = self._get_url(group_id)
        data = self.con.delete(url)
        return Group(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ImportsEndpoint(ApiBase):
    def __init__(self, parent):
        super(ImportsEndpoint, self).__init__(parent, endpoint='/imports')

    def get_import_jobs(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.imports.Import`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs).get('data', {})
        return [Import(self, job) for job in data] if data else []

    def get_import_job_by_id(self, import_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.imports.Import`
        """
        url = self._get_url(import_id)
        data = self.con.get(url, params=params, **kwargs)
        return Import(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentsEndpoint(ApiBase):

    def __init__(self, parent):
        super(IncidentsEndpoint, self).__init__(parent, endpoint='/incidents')

    def get_incidents(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.incidents.Incident`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Incident) if data.get('data') else []

    def get_incident_by_id(self, incident_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.incidents.Incident`
        """
        url = self._get_url(incident_id)
        data = self.con.get(url, params=params, **kwargs)
        return Incident(self, data) if data else None

    def update_incident(self, incident_id, data):
        """

        :rtype: :class:`~xmatters.objects.incidents.Incident`
        """
        url = self._get_url(incident_id)
        data = self.con.post(url, data=data)
        return Incident(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallEndpoint(ApiBase):

    def __init__(self, parent):
        super(OnCallEndpoint, self).__init__(parent, endpoint='/on-call')

    def get_oncall(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.oncall.OnCall`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, OnCall) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummaryEndpoint(ApiBase):

    def __init__(self, parent):
        super(OnCallSummaryEndpoint, self).__init__(parent, endpoint='/on-call-summary')

    def get_oncall_summary(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.oncall_summary.OnCallSummary`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return [OnCallSummary(self, summary) for summary in data] if data else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PeopleEndpoint(ApiBase):
    _endpoints = {'license_quotas': '/license-quotas'}

    def __init__(self, parent):
        super(PeopleEndpoint, self).__init__(parent, endpoint='/people')

    def get_people(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Person) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url(person_id)
        data = self.con.get(url, params=params, **kwargs)
        return Person(self, data) if data else None

    def get_license_quotas(self):
        """

        :rtype: :class:`~xmatters.objects.people.UserQuota`
        """
        url = self._get_url(self._endpoints.get('license_quotas'))
        data = self.con.get(url)
        return UserQuota(self, data) if data else None

    def create_person(self, data):
        """

        :rtype: :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def update_person(self, data):
        """

        :rtype: :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def delete_person(self, person_id):
        """

        :rtype: :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url(person_id)
        data = self.con.delete(url)
        return Person(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlansEndpoint(ApiBase):

    def __init__(self, parent):
        super(PlansEndpoint, self).__init__(parent, endpoint='/plans')

    def get_plans(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.plans.Plan`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Plan) if data.get('data') else []

    def get_plan_by_id(self, plan_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.plans.Plan`
        """
        url = self._get_url(plan_id)
        data = self.con.get(url, params=params, **kwargs)
        return Plan(self, data) if data else None

    def create_plan(self, data):
        """

        :rtype: :class:`~xmatters.objects.plans.Plan`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    def update_plan(self, data):
        """

        :rtype: :class:`~xmatters.objects.plans.Plan`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    def delete_plan(self, plan_id):
        """

        :rtype: :class:`~xmatters.objects.plans.Plan`
        """
        url = self._get_url(plan_id)
        data = self.con.delete(url)
        return Plan(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RolesEndpoint(ApiBase):

    def __init__(self, parent):
        super(RolesEndpoint, self).__init__(parent, endpoint='/roles')

    def get_roles(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.roles.Role`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Role) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenariosEndpoint(ApiBase):

    def __init__(self, parent):
        super(ScenariosEndpoint, self).__init__(parent, endpoint='/scenarios')

    def get_scenarios(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.scenarios.Scenario`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Scenario) if data.get('data') else []

    def get_scenario_by_id(self, scenario_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.scenarios.Scenario`
        """
        url = self._get_url(scenario_id)
        data = self.con.get(url, params=params, **kwargs)
        return Scenario(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ServicesEndpoint(ApiBase):

    def __init__(self, parent):
        super(ServicesEndpoint, self).__init__(parent, endpoint='/services')

    def get_services(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.services.Service`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Service) if data.get('data') else []

    def get_service_by_id(self, service_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.services.Service`
        """
        url = self._get_url(service_id)
        data = self.con.get(url, params=params, **kwargs)
        return Service(self, data) if data else None

    def create_service(self, data):
        """

        :rtype: :class:`~xmatters.objects.services.Service`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    def update_service(self, data):
        """

        :rtype: :class:`~xmatters.objects.services.Service`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    def delete_service(self, service_id):
        """

        :rtype: :class:`~xmatters.objects.services.Service`
        """
        url = self._get_url(service_id)
        data = self.con.delete(url)
        return Service(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SitesEndpoint(ApiBase):

    def __init__(self, parent):
        super(SitesEndpoint, self).__init__(parent, endpoint='/sites')

    def get_sites(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.sites.Site`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Site) if data.get('data') else []

    def get_site_by_id(self, site_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.sites.Site`
        """
        url = self._get_url(site_id)
        data = self.con.get(url, params=params, **kwargs)
        return Site(self, data) if data else None

    def create_site(self, data):
        """

        :rtype: :class:`~xmatters.objects.sites.Site`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    def update_site(self, data):
        """

        :rtype: :class:`~xmatters.objects.sites.Site`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    def delete_site(self, site_id):
        """

        :rtype: :class:`~xmatters.objects.sites.Site`
        """
        url = self._get_url(site_id)
        data = self.con.delete(url)
        return Site(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionsEndpoint(ApiBase):
    _endpoints = {'subscribers': '/subscribers',
                  'unsubscribe': '/subscribers/{}'}

    def __init__(self, parent):
        super(SubscriptionsEndpoint, self).__init__(parent, endpoint='/subscriptions')

    def get_subscriptions(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, Subscription) if data else []

    def get_subscription_by_id(self, subscription_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url(subscription_id)
        data = self.con.get(url, params=params, **kwargs)
        return SubscriptionForm(self, data) if data else None

    def get_subscribers(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.people.Person`
        """
        url = self._get_url('/subscribers')
        subscribers = self.con.get(url, params=params, **kwargs)
        return Pagination(self, subscribers, Person) if subscribers.get('data') else []

    def unsubscribe_person(self, person_id):
        """

        :rtype: :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url(self._endpoints.get('unsubscribe').format(person_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    def create_subscription(self, data):
        """

        :rtype: :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    def update_subscription(self, data):
        """

        :rtype: :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    def delete_subscription(self, subscription_id):
        """

        :rtype: :class:`~xmatters.objects.subscriptions.Subscription`
        """
        url = self._get_url(subscription_id)
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormsEndpoint(ApiBase):

    def __init__(self, parent):
        super(SubscriptionFormsEndpoint, self).__init__(parent, endpoint='/subscription-forms')

    def get_subscription_forms(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.subscription_forms.SubscriptionForm`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, SubscriptionForm) if data.get('data') else []

    def get_subscription_form_by_id(self, sub_form_id, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.objects.subscription_forms.SubscriptionForm`
        """
        url = self._get_url(sub_form_id)
        data = self.con.get(url, params=params, **kwargs)
        return SubscriptionForm(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class TemporaryAbsencesEndpoint(ApiBase):

    def __init__(self, parent):
        super(TemporaryAbsencesEndpoint, self).__init__(parent, endpoint='/temporary-absences')

    def get_temporary_absences(self, params=None, **kwargs):
        """

        :rtype: :class:`~xmatters.utils.Pagination` of :class:`~xmatters.objects.temporary_absences.TemporaryAbsence`
        """
        url = self._get_url()
        data = self.con.get(url, params=params, **kwargs)
        return Pagination(self, data, TemporaryAbsence) if data.get('data') else []

    def create_temporary_absence(self, data):
        """

        :rtype: :class:`~xmatters.objects.temporary_absences.TemporaryAbsence`
        """
        url = self._get_url()
        data = self.con.post(url, data=data)
        return TemporaryAbsence(self, data) if data else None

    def delete_temporary_absence(self, temporary_absence_id):
        """

        :rtype: :class:`~xmatters.objects.temporary_absences.TemporaryAbsence`
        """
        url = self._get_url(temporary_absence_id)
        data = self.con.delete(url)
        return TemporaryAbsence(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

# class UploadUsersEndpoint(ApiBridge):
#     _endpoints = {'upload_user_upload_file': '/uploads/users-v1',
#                   'upload_epic_zipsync_file': '/uploads/epic-v1'}
#
#     def __init__(self, parent):
#         super(UploadUsersEndpoint, self).__init__(parent)
#
#     def upload_user_upload_file(self, file_path):
#         pass
#
#     def upload_epic_zipsync_file(self, file_path):
#         pass
#
#     def __repr__(self):
#         return '<{}>'.format(self.__class__.__name__)
#
#     def __str__(self):
#         return self.__repr__()
