import pyrebase


class DatabaseReference:

    firebase_config = "REDACTED"

    def __init__(self):
        firebase = pyrebase.initialize_app(DatabaseReference.firebase_config)
        self.db = firebase.database()

    def _get_ref(self, keys):
        assert len(keys) > 0

        ref = self.db
        for key in keys:
            ref = ref.child(key)

        return ref

    def save_json_data(self, keys, data):
        self._get_ref(keys).set(data)

    def load_json_data(self, keys):
        return self._get_ref(keys).get()

    def keys_at_path(self, keys):
        return self._get_ref(keys).shallow().get().val()
