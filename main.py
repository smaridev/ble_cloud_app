from constants import TOPIC_REGISTRATION, TOPIC_SENSORINFO
from sensor_info import SensorInfo
from registration import RegistrationInfo


def process_southbound_request(request_object):
    try:
        print("req {}".format(request_object))
        req = request_object.get_json()
        print("req {}".format(req))
        #request = request_object
        msg_type = get_msg_type(req)
        print("req {}".format(req))
        if TOPIC_SENSORINFO in msg_type:
            return SensorInfo(req).handle()
        if TOPIC_REGISTRATION in msg_type:
            return RegistrationInfo(req).handle()
        else:
            print("Invalid Message type {} {}".format(req, msg_type))
            return f'failed'
        return f'success'
    except Exception as e:
        print("Exception {}".format(e))
        return f'failed'

def process_northbound_request(request_object):
    try:
        req = request_object.get_json()
        args = request_object.args.to_dict()
        print("ARGS {}".format(args))
        if request_object.method == 'GET':
            if args['type'] == 'sensorinfo':
                return RegistrationInfo(req).handle_get_request(args)
            if args['type'] == 'sensorattrs':
                return SensorInfo(req).handle_get_request(args)
            else:
                return f'Invalid Request'
        return f'Invalid Request'
    except Exception as e:
        print("Exception {}".format(e))


def get_msg_type(request_object):
    if request_object is not None:
        if isinstance(request_object, dict):
            msg = request_object.get('message')
            msg_type = msg.split("/")
            print("msg_type {}".format(msg_type))
            return msg_type
    return None


if __name__ == '__main__':
    req = {
        "message": "Thingy52/4e253754/sensorinfo",
        "tpid": 616890614,
        "appid": 1311061844,
        "tstamp": 1552989807,
        "load": {
            "s_id": "s_1",
            "attr": "pressure",
            "d2": 47,
            "d1": 25,
            "tpid": 616890614,
            "appid": 1311061844,
            "tstamp": 1552989807
        },
    }
   # ret = process_southbound_request(req)
   # ret = process_northbound_request(req)

    req = {
   "message":"Thingy52/registration",
   "tpid":616890614,
   "appid":1311061844,
   "tstamp":1552989802,
   "load":{  
      "ver":1,
      "attr":"registration",
      "tpid":616890615,
      "appid":1311061844,
      "tstamp":1552989802,
       "s_id": "s_2"
        }
    }
    ret = process_southbound_request(req)
    print("return value is {}".format(ret))
    ret = process_northbound_request(req)
