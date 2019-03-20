
from validator import SensorInfoFormatValidator
from constants import ATT_TEMP
from dal import DataAccessLayer
class SensorInfo(object):
    def __init__(self, request_object):
        self.request = request_object

    def transform(self, attr, content):
        try:
            if attr == ATT_TEMP:
                val = content['d1'] + (content['d2']/100)
                return val
            return 0
        except Exception as e:
            print("Exception e {}".format(e))
            return 0


    def process_document(self, document):
        return DataAccessLayer('thingy52').add(document)

    def handle(self):
        if SensorInfoFormatValidator().validate(self.request):
            print("request validated")
            status, document = self.prepare_document()
            if status is True:
                return self.process_document(document)
            return False
        return False

    def prepare_document(self):
        try:
            content = self.request['load']
            attr = content['attr']
            value = self.transform(attr, content)
            document = {
                'tp_id': content['tpid'],
                's_id': content['s_id'],
                'attr': attr,
                'value': value,
                'app_id': content['appid'],
                'timestamp': content['tstamp'],
                'cid': 'cid123'
            }
            return True, document
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None