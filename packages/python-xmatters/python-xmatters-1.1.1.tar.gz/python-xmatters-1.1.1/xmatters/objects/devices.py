import xmatters.connection

from xmatters.objects.common import Recipient, ReferenceById
from xmatters.objects.people import PersonReference


class Provider(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(Provider, self).__init__(parent, data)
        self.id = data.get('id')    #: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return self.__repr__()


class Device(Recipient):

    def __init__(self, parent, data):
        super(Device, self).__init__(parent, data)
        self.default_device = data.get('defaultDevice')    #: :vartype: bool
        self.delay = data.get('delay')    #: :vartype: int
        self.description = data.get('description')    #: :vartype: str
        self.device_type = data.get('deviceType')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        owner = data.get('owner')
        self.owner = PersonReference(self, owner) if owner else None    #: :vartype: :class:`~xmatters.objects.people.PersonReference`
        self.priority_threshold = data.get('priorityThreshold')    #: :vartype: str
        provider = data.get('provider')
        self.provider = ReferenceById(self, provider) if provider else None    #: :vartype: :class:`~xmatters.objects.common.ReferenceById`
        self.sequence = data.get('sequence')    #: :vartype: int
        self.test_status = data.get('testStatus')    #: :vartype: str

    @property
    def timeframes(self):
        """ Alias of :meth:`get_timeframes`"""
        return self.get_timeframes()

    def get_timeframes(self):
        """
        Get device timeframes

        :return: list
        :rtype: list[:class:`~xmatters.objects.devices.DeviceTimeframe`]
        """
        url = self._get_url('?embed=timeframes')
        data = self.con.get(url).get('timeframes', {}).get('data', [])
        return [DeviceTimeframe(self, timeframe) for timeframe in data]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class EmailDevice(Device):
    def __init__(self, parent, data):
        super(EmailDevice, self).__init__(parent, data)
        self.email_address = data.get('emailAddress')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class VoiceDevice(Device):
    def __init__(self, parent, data):
        super(VoiceDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class SMSDevice(Device):
    def __init__(self, parent, data):
        super(SMSDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class TextPagerDevice(Device):
    def __init__(self, parent, data):
        super(TextPagerDevice, self).__init__(parent, data)
        self.pin = data.get('pin')    #: :vartype: str
        self.two_way_device = data.get('twoWayDevice')    #: :vartype: bool

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ApplePushDevice(Device):
    def __init__(self, parent, data):
        super(ApplePushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')    #: :vartype: str
        self.apn_token = data.get('apnToken')    #: :vartype: str
        self.alert_sound = data.get('alertSound')    #: :vartype: str
        self.sound_status = data.get('soundStatus')    #: :vartype: str
        self.sounds_threshold = data.get('soundThreshold')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class AndroidPushDevice(Device):
    def __init__(self, parent, data):
        super(AndroidPushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')    #: :vartype: str
        self.registration_id = data.get('registrationId')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class FaxDevice(Device):
    def __init__(self, parent, data):
        super(FaxDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')    #: :vartype: str
        self.country = data.get('country')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PublicAddressDevice(Device):
    def __init__(self, parent, data):
        super(PublicAddressDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class GenericDevice(Device):
    def __init__(self, parent, data):
        super(GenericDevice, self).__init__(parent, data)
        self.phone_number = data.get('pin')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class DeviceTimeframe(xmatters.connection.ApiBase):
    def __init__(self, parent, data):
        super(DeviceTimeframe, self).__init__(parent, data)
        self.days = data.get('days')    #: :vartype: str
        self.duration_in_minutes = data.get('durationInMinutes')    #: :vartype: int
        self.exclude_holidays = data.get('excludeHolidays')    #: :vartype: bool
        self.name = data.get('name')    #: :vartype: str
        self.start_time = data.get('startTime')    #: :vartype: str
        self.timezone = data.get('timezone')    #: :vartype: str

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()
