from google.cloud import firestore


class DataAccessLayer(object):
    def __init__(self, collection):
        self.db = firestore.Client()
        self.collection = collection

    def add(self, request_object):
        # Add a new document
        doc_ref = self.db.collection(self.collection).add(request_object)
        self.list()

    def list(self):
        # Then query for documents
        users_ref = self.db.collection(self.collection)
        docs = users_ref.get()

        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

    def list_by_sensor(self, s_id):
        users_ref = self.db.collection(self.collection)
        docs = users_ref.where(u's_id', u'==', s_id).get()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
