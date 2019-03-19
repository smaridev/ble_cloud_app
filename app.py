from constants import TOPIC_REGISTRATION, TOPIC_SENSORINFO
from sensor_info import SensorInfo
from validator import RegistrationFormatValidator


def process_request(request_object):
    msg_type = get_msg_type(request_object)
    print("req {}".format(request_object))
    if msg_type == TOPIC_SENSORINFO:
        return SensorInfo(request_object).handle()
    if msg_type == TOPIC_REGISTRATION:
        ret, err = RegistrationFormatValidator().validate(request_object)
        if ret:
            return registration_handler(request_object)
    else:
        print("Invalid Message type {} {}".format(request_object, msg_type))
        return False
    return True


def get_msg_type(request_object):
    if request_object is not None:
        if isinstance(request_object, dict):
            msg = request_object.get('message')
            app, id, topic = msg.split("/")
            print("topic {}".format(topic))
            return topic
    return None


def registration_handler(request_object):
    return True


if __name__ == '__main__':
    req = {
        "message": "Thingy52/4e253754/sensorinfo",
        "tpid": 616890614,
        "appid": 1311061844,
        "tstamp": 1552989807,
        "load": {
            "s_id": "s_1",
            "attr": "temperature",
            "d2": 47,
            "d1": 25,
            "tpid": 616890614,
            "appid": 1311061844,
            "tstamp": 1552989807
        },
    }
    ret = process_request(req)
    print("return value is {}".format(ret))
