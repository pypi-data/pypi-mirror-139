from abc import ABC, abstractmethod

import xmatters.objects.groups
import xmatters.objects.audits
import xmatters.objects.people
import xmatters.objects.dynamic_teams
import xmatters.objects.scenarios
import xmatters.objects.device_names
import xmatters.objects.plan_endpoints
import xmatters.objects.plan_properties
import xmatters.objects.forms
import xmatters.objects.devices
import xmatters.utils


class Factory(ABC):
    """ ABC for factory objects """

    @property
    @abstractmethod
    def id_attr(self):
        pass

    @property
    @abstractmethod
    def factory_objects(self):
        pass

    def __new__(cls, parent, data):
        return cls.construct(parent, data)

    @classmethod
    def construct(cls, parent, data):
        """ Determine which object to construct from 'identifier' attribute in object """
        identifier = data.get(cls.id_attr)
        # noinspection PyUnresolvedReferences
        constructor = cls.factory_objects.get(identifier)
        return constructor(parent, data) if constructor else None


class DeviceFactory(Factory):
    """ Construct Device object based on 'deviceType' attribute """
    id_attr = 'deviceType'
    factory_objects = {'EMAIL': xmatters.objects.devices.EmailDevice,
                       'VOICE': xmatters.objects.devices.VoiceDevice,
                       'TEXT_PHONE': xmatters.objects.devices.SMSDevice,
                       'TEXT_PAGER': xmatters.objects.devices.TextPagerDevice,
                       'APPLE_PUSH': xmatters.objects.devices.ApplePushDevice,
                       'ANDROID_PUSH': xmatters.objects.devices.AndroidPushDevice,
                       'FAX': xmatters.objects.devices.FaxDevice,
                       'VOICE_IVR': xmatters.objects.devices.PublicAddressDevice,
                       'GENERIC': xmatters.objects.devices.GenericDevice}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientFactory(Factory):
    """ Construct recipient object based on 'recipientType' attribute """
    id_attr = 'recipientType'
    factory_objects = {'GROUP': xmatters.objects.groups.Group,
                       'PERSON': xmatters.objects.people.Person,
                       'DEVICE': xmatters.objects.devices.Device,
                       'DYNAMIC_TEAM': xmatters.objects.dynamic_teams.DynamicTeam}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditFactory(Factory):
    """ Construct audit object based on 'type' attribute """
    id_attr = 'type'
    factory_objects = {'EVENT_ANNOTATED': xmatters.objects.audits.AuditAnnotation,
                       'EVENT_CREATED': xmatters.objects.audits.Audit,
                       'EVENT_SUSPENDED': xmatters.objects.audits.Audit,
                       'EVENT_RESUMED': xmatters.objects.audits.Audit,
                       'EVENT_COMPLETED': xmatters.objects.audits.Audit,
                       'EVENT_TERMINATED': xmatters.objects.audits.Audit,
                       'RESPONSE_RECEIVED': xmatters.objects.audits.AuditResponse,
                       'NOTIFICATION_DELIVERED': xmatters.objects.audits.AuditNotification,
                       'NOTIFICATION_FAILED': xmatters.objects.audits.AuditNotification}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SectionFactory(Factory):
    """ Construct section object based on 'type' attribute """
    id_attr = 'type'
    factory_objects = {'CONFERENCE_BRIDGE': xmatters.objects.forms.ConferenceBridgeSection,
                       'CUSTOM_SECTION': xmatters.objects.forms.CustomSectionItems,
                       'DEVICE_FILTER': xmatters.objects.forms.DevicesSection,
                       'HANDLING_OPTIONS': xmatters.objects.forms.HandlingSection,
                       'ATTACHMENTS': xmatters.objects.forms.FormSection,
                       'SENDER_OVERRIDES': xmatters.objects.forms.SenderOverridesSection,
                       'RECIPIENTS': xmatters.objects.forms.RecipientsSection,
                       'RESPONSE_CHOICES': xmatters.objects.forms.FormSection,
                       'INCIDENT': xmatters.objects.forms.IncidentSection,
                       'DOCUMENT_UPLOAD': xmatters.objects.forms.FormSection}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuthFactory(Factory):
    """ Construct authentication object based on 'authenticationType' attribute """
    id_attr = 'authenticationType'
    factory_objects = {'NO_AUTH': None,
                       'BASIC': xmatters.objects.plan_endpoints.BasicAuthentication,
                       'OAUTH2': xmatters.objects.plan_endpoints.OAuth2Authentication,
                       'OAUTH2_FORCE': xmatters.objects.plan_endpoints.OAuth2Authentication,
                       'OAUTH_SLACK': xmatters.objects.plan_endpoints.OAuth2Authentication,
                       'XMATTERS': xmatters.objects.plan_endpoints.ServiceAuthentication,
                       'SERVICENOW': xmatters.objects.plan_endpoints.ServiceAuthentication}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertiesFactory(Factory):
    """ Construct plan property object based on 'propertyType' attribute """
    id_attr = 'propertyType'
    factory_objects = {'BOOLEAN': xmatters.objects.plan_properties.Boolean,
                       'HIERARCHY': xmatters.objects.plan_properties.Hierarchy,
                       'LIST_TEXT_MULTI_SELECT': xmatters.objects.plan_properties.MultLinkSelectList,
                       'LIST_TEXT_SINGLE_SELECT': xmatters.objects.plan_properties.SingleSelectList,
                       'NUMBER': xmatters.objects.plan_properties.Number,
                       'PASSWORD': xmatters.objects.plan_properties.Password,
                       'TEXT': xmatters.objects.plan_properties.Text}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermFactory(Factory):
    """ Construct scenario permission object based on 'permissibleType' attribute """
    id_attr = 'permissibleType'
    factory_objects = {'PERSON': xmatters.objects.scenarios.ScenarioPermissionPerson,
                       'ROLE': xmatters.objects.scenarios.ScenarioPermissionRole}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNameFactory(Factory):
    """ Construct device name object based on 'deviceType' attribute """
    id_attr = 'deviceType'
    factory_objects = {
        'ANDROID_PUSH': xmatters.objects.device_names.DeviceName,
        'APPLE_PUSH': xmatters.objects.device_names.DeviceName,
        'EMAIL': xmatters.objects.device_names.DeviceNameEmail,
        'FAX': xmatters.objects.device_names.DeviceName,
        'GENERIC': xmatters.objects.device_names.DeviceName,
        'TEXT_PAGER': xmatters.objects.device_names.DeviceName,
        'TEXT_PHONE': xmatters.objects.device_names.DeviceName,
        'VOICE': xmatters.objects.device_names.DeviceName,
        'VOICE_IVR': xmatters.objects.device_names.DeviceName}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
