
from validator import RegistrationFormatValidator
from constants import ATT_TEMP, ATT_PRESSURE
from dal import DataAccessLayer, SensorAttrModel
import time

app_name_to_collection = {
    'Thingy52': 'thingy52_sensor_details',
    'lm75': 'lm75_sensor_details'
}
class RegistrationInfo(object):
    def __init__(self, request_object, app_name):
        self.request = request_object
        self.app_name = app_name
        self.collection = app_name_to_collection[app_name]

    def process_document(self, document):
        return DataAccessLayer(self.collection).add_or_update(document, str(document['app_id']))

    def handle(self):
        if RegistrationFormatValidator().validate(self.request):
            print("request validated")
            status, document = self.prepare_document()
            if status is True:
                if self.process_document(document):
                    return f'success'
                else:
                    return f'failed'
            return f'success'
        return f'failed'

    def prepare_document(self):
        try:
            content = self.request['load']
            print("CONTENT: {}".format(content))
            document = {
                'tp_id': content['tpid'],
                'app_id': content['appid'],
                'timestamp': content['tstamp'],
                'cid': 'cid123',
                'version': content['ver'],
                'description': content['desc'],
                'sensor_name': content['sensor_name'],
                'tp_name': content['tp_name']
            }
            return True, document
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None

    def handle_get_request(self, args):
        try:
            return DataAccessLayer(self.collection).list()
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None
