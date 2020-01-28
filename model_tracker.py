import keras
import requests
import json

class ModelTracker(keras.callbacks.Callback):
    def __init__(self, model_key):
        self.__url = "http://localhost:5000/"
        self.__json_header = {'Content-type':'application/json'}
        self.model_key = model_key
        req = requests.post(self.__url + "auth", json={'model_key':model_key},
                      headers=self.__json_header)
        if req.status_code != 200:
            raise Exception("Invalid model key")
            return
        super().__init__()

    def on_train_begin(self, logs={}):
        req = requests.post(self.__url + "start", json=self.params,
                            headers=self.__json_header)
        self.training_id = req.json()['training_id']

    def on_train_end(self, logs={}):
        requests.post(self.__url + "end", json={'training_id' : self.training_id},
                     headers=self.__json_header)

    def on_epoch_begin(self, epoch, logs={}):
        logs['training_id'] = self.training_id
        logs['epoch'] = epoch
        requests.post(self.__url + "epochbegin", data=json.dumps(str(logs)), headers=self.__json_header)

    def on_epoch_end(self, epoch, logs={}):
        logs['training_id'] = self.training_id
        logs['epoch'] = epoch
        requests.post(self.__url + "epochend", data=json.dumps(str(logs)), headers=self.__json_header)
