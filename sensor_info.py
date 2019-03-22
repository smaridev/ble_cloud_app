
from validator import SensorInfoFormatValidator
from constants import ATT_TEMP, ATT_PRESSURE
from dal import DataAccessLayer, SensorAttrModel
import time

app_name_collection_mapping = {
    'Thingy52': 'thingy52',
    'lm75': 'lm75'
}

class SensorInfo(object):
    def __init__(self, request_object, app_name):
        self.request = request_object
        self.app = app_name
        self.collection = app_name_collection_mapping[app_name]

    def transform(self, attr, content):
        try:
            if attr in [ATT_TEMP, ATT_PRESSURE]:
                val = content['d1'] + (content['d2']/100)
                return val
            else:
                return content['d1']
        except Exception as e:
            print("Exception e {}".format(e))
            return 0


    def process_document(self, document):
        return SensorAttrModel(self.collection).add(document)

    def handle(self):
        if SensorInfoFormatValidator().validate(self.request):
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
            attr = content['attr']
            value = self.transform(attr, content)
            document = {
                'tp_id': content['tpid'],
                's_id': content['s_id'],
                'attribute': attr,
                'value': value,
                'app_id': content['appid'],
                'timestamp': content['tstamp'],
                'cid': 'cid123'
            }
            return True, document
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None

    def handle_get_request(self, args):
        try:
            app_id = args['sensor']
            start, end = self.get_timerange(args)
            print("start: {}, end: {}, sensor_id: {}, attr {}".format(start, end, app_id, args['attr']))
            return self.get_attr_timeseries(app_id, args['attr'], start, end)
        except Exception as e:
            print("Exception e {}".format(e))
            return False, None

    def get_attr_timeseries(self, app_id, attr, start, end):
        docs = SensorAttrModel(self.collection).list_by_sensor(int(app_id), attr, start, end)
        return docs

    def get_timerange(self, args):
        end = time.time()
        start = end - 3600
        return start, end
