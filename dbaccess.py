import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireStoreAccess:
    # Use a service account
    cred = credentials.Certificate('service-key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    def auth_db(self, model_key, password):
        try:
            username = self.db.collection("model_keys").document(model_key).get().get("username")
        except:
            username = None

        if username is None:
            return None

        try:
            db_pswd = self.db.collection("users").document(username).get(["password"]).get("password")
        except:
            db_pswd = None

        if db_pswd is None:
            return None

        return username if db_pswd==password else None

    def auth_amqp(self, model_key, password):
        if not self.auth_db(model_key, password):
            return None
        with open("amqp_url", "r") as fh:
            amqp_url = fh.read().strip()
        return amqp_url

    def start_training(self, model_key, username, JSON):
        doc_ref = self.db.collection("users").document(username).collection("models").document(model_key)
        train_count = doc_ref.get(["train_count"]).get("train_count") + 1
        doc_ref.update({
            "train_count" : train_count
        })

        new_training_id = "training_{0:0>3d}".format(train_count)
        trainings = doc_ref.collection("trainings")
        trainings.add({
            "done":False,
            **JSON
        }, document_id=new_training_id)

        return new_training_id

    def end_training(self, model_key, username, training_id):
        self.db.collection("users").document(username).collection("models").document(model_key).collection("trainings").document(training_id).update({
            "done" : True
        })

    def epoch_begin(self, model_key, username, JSON):
        epoch = JSON['epoch']
        training_id = JSON['training_id']
        self.db.collection('users').document(username).collection('models').document(model_key).collection('trainings').document(training_id).collection('epochs_list').document(epoch).set({
            "done" : False,
            **JSON
        })

    def epoch_end(self, model_key, username, JSON):
        epoch = JSON['epoch']
        training_id = JSON['training_id']
        JSON.pop('epoch')
        self.db.collection('users').document(username).collection('models').document(model_key).collection('trainings').document(training_id).collection('epochs_list').document(epoch).set({
            "done" : True,
            **JSON
        })
