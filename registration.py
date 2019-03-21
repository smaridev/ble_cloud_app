
from validator import RegistrationFormatValidator
from constants import ATT_TEMP, ATT_PRESSURE
from dal import DataAccessLayer, SensorAttrModel
import time

class RegistrationInfo(object):
    def __init__(self, request_object):
        self.request = request_object

    def process_document(self, document):
        return DataAccessLayer('sensor_details').add_or_update(document, document['s_id'])

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
            document = {
                'tp_id': content['tpid'],
                's_id': content['s_id'],
                'app_id': content['appid'],
                'timestamp': content['tstamp'],
                'cid': 'cid123',
                'version': content['ver'],
                'name': content['name'],
                'description': content['desc']
            }
            return True, document
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None

    def handle_get_request(self, args):
        try:
            return DataAccessLayer('sensor_details').list()
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None
