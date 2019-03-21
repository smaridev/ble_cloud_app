"""
    Validators for BLE Inbound messages
"""

from incoming import PayloadValidator
from incoming import datatypes

from constants import GSupportedAttributes


class EStringIncomingType(datatypes.Types):
    '''
        Enhanced datatype for matching String
    '''
    MAX_STRING_LEN = 2 * 1024  # 2 KB

    _DEFAULT_ERROR = 'Invalid data. A proper string is expected.'

    def __init__(self, required=None, error=None, *args, **kwargs):
        super(EStringIncomingType, self).__init__(
            required, error, *args, **kwargs)
        self.max_len = kwargs.get('max_len', self.MAX_STRING_LEN)
        self.min_len = kwargs.get('min_len', None)
        if self.min_len is not None:
            self.error = "{} Minimum length required is {}.".format(
                self.error, self.min_len)
        if self.max_len is not None:
            self.error = "{} Maximum length allowed is {}.".format(
                self.error, self.max_len)

    def validate(self, val, *args, **kwargs):
        if not isinstance(val, str):
            return False

        if (self.max_len is not None):
            if len(val) > self.max_len:
                return False

        if (self.min_len is not None):
            if len(val) < self.min_len:
                return False

        return True


class EIntegerIncomingType(datatypes.Types):
    '''
        Enhanced datatype for matching Integer
    '''
    _DEFAULT_ERROR = 'Invalid data. A proper integer is expected'

    def __init__(self, required=None, error=None, *args, **kwargs):
        super(EIntegerIncomingType, self).__init__(
            required, error, *args, **kwargs)
        self.max_value = kwargs.get('max_value', None)
        self.min_value = kwargs.get('min_value', None)
        if self.min_value is not None:
            self.error = "{} Minimum value required is {}.".format(
                self.error, self.min_value)
        if self.max_value is not None:
            self.error = "{} Maximum value allowed is {}.".format(
                self.error, self.max_value)

    def validate(self, val, *args, **kwargs):
        if not isinstance(val, int):
            return False

        if (self.max_value is not None):
            if val > self.max_value:
                return False

        if (self.min_value is not None):
            if val < self.min_value:
                return False

        return True


class ETimeStampIncomingType(EIntegerIncomingType):
    # TODO: validate if the integer is of timestamp format
    _DEFAULT_ERROR = 'Invalid data. A proper Timestamp is expected.'

    def __init__(self, required=None, error=None, *args, **kwargs):
        super(EIntegerIncomingType, self).__init__(
            required, error, *args, **kwargs)
        self.max_value = kwargs.get('max_value', None)
        self.min_value = kwargs.get('min_value', None)
        self.validate_upcoming_time = kwargs.get(
            'validate_upcoming_time', False)
        if self.validate_upcoming_time:
            self.error = "{} Minimum value {}".format(
                self.error, "should be greater than current timestamp")
        else:
            if self.min_value is not None:
                self.error = "{} Minimum value required is {}.".format(
                    self.error, self.min_value)
            if self.max_value is not None:
                self.error = "{} Maximum value allowed is {}.".format(
                    self.error, self.max_value)


class LoadFormatValidator(PayloadValidator):
    s_id = EStringIncomingType(required=True, min_len=1)
    appid = EIntegerIncomingType(required=True, min_len=1)
    tstamp = ETimeStampIncomingType(required=True)
    tpid = EIntegerIncomingType(required=True, min_len=1)
    attr = datatypes.Function('validate_attribute',
                              required=True,
                              error='Invalid attribute specified')
    d2 = EIntegerIncomingType(required=False)
    d1 = EIntegerIncomingType(required=False)
    strict = False

    def validate_attribute(self, attr, payload, errors, **kwargs):
        if not isinstance(attr, str):
            return False
        if not attr:
            return False
        if attr not in GSupportedAttributes:
            return False
        return True

class RegistrationLoadFormatValidator(PayloadValidator):
    s_id = EStringIncomingType(required=True, min_len=1)
    appid = EIntegerIncomingType(required=True, min_len=1)
    tstamp = ETimeStampIncomingType(required=True)
    tpid = EIntegerIncomingType(required=True, min_len=1)
    ver = EIntegerIncomingType(required=True, min_len=1)
    name = EStringIncomingType(required=True, min_len=1)
    desc = EStringIncomingType(required=False, min_len=1)
    strict = False


class SensorInfoFormatValidator(PayloadValidator):
    message = EStringIncomingType(required=True, min_len=1)
    tpid = EIntegerIncomingType(required=True, min_len=1)
    appid = EIntegerIncomingType(required=True, min_len=1)
    tstamp = ETimeStampIncomingType(required=True)
    load = datatypes.Function('validate_load',
                              required=True,
                              error='Invalid load specified')
    strict = False

    def validate_load(self, load, payload, errors, **kwargs):
        if not load:
            return False
        if not isinstance(load, dict):
            return False
        try:
            result, err = LoadFormatValidator().validate(load)
            print("result {} err {}".format(result, err))
            if not result:
                errors.append(err)
                return result
            return True

        except Exception as e:
            print("exception: {}".format(e))
            return False


class RegistrationFormatValidator(PayloadValidator):
    tpid = EIntegerIncomingType(required=True, min_len=1)
    appid = EIntegerIncomingType(required=True, min_len=1)
    tstamp = ETimeStampIncomingType(required=True)
    load = datatypes.Function('validate_load',
                              required=True,
                              error='Invalid load specified')
    strict = True

    def validate_load(self, load, payload, errors, **kwargs):
        if not load:
            return False
        if not isinstance(load, dict):
            return False
        try:
            result, err = LoadFormatValidator().validate(load)
            if not result:
                errors.append(err)
                return result
        except Exception:
            return False
        else:
            return True
