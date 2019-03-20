from google.cloud import firestore
import json
import time

class DataAccessLayer(object):
    def __init__(self, collection):
        self.db = firestore.Client()
        self.collection = collection

    def add(self, request_object):
        # Add a new document
        doc_ref = self.db.collection(self.collection).add(request_object)
        self.list()
        return True

    def add_or_update(self, request_object, key):
        doc_ref = self.db.collection(self.collection)\
            .document(key).set(request_object)
        self.list()
        return True

    def list(self):
        # Then query for documents
        users_ref = self.db.collection(self.collection)
        docs = users_ref.get()
        response = []
        for doc in docs:
            response.append(doc.to_dict())
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
        return json.dumps(response)


class SensorAttrModel(DataAccessLayer):
    def list_by_sensor(self, s_id, attr = None, start = None, end = None):
        if attr is not None:
            if end == None:
                end = time.time()
            if start == None:
                start = end - 3600

            users_ref = self.db.collection(self.collection)
            docs = users_ref.where(u's_id', u'==', u's_1')\
                .where(u"attribute", "==", attr).get()
                #.where("timestamp", ">", start).get()
              #  .where(u"timestamp", "<=", end).get()

            response = []
            for doc in docs:
                print(u'{} => {}'.format(doc.id, doc.to_dict()))
                doc_dict = doc.to_dict()
                response.append({
                    'ts': doc_dict['timestamp'],
                    'value': doc_dict['value']
                })
            print("response {}".format(response))
            return json.dumps(response)
        else:
            print("Invalid Attr {}".format(attr))
            return []