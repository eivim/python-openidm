import json

class OpenIDMObject(object):
    def __init__(self, _id=None, idm=False, **data):
        self._id = _id
        self._idm = idm
        self._loaded = False
        self.data = data

    def set_client(self, client):
        self._client = client

    def read(self):
        if self._id and self._idm:
            json = self._client.read(self.__class__, self._id)
            self._loaded = True
            self.data = json

    def save(self):
        pass # Not implemented
    
    def refresh(self):
        self._loaded = False
        self.read()
    
    def __getattr__(self, name):
        if not self._loaded:
            self.read()
        return self.data.get(name)
    
    def get_json(self):
        if self._id and not self._loaded:
            self.read()
        return json.dumps(self.data, sort_keys=True, indent=2)

    def __repr__(self):
        if self._id:
            _id = self._id
        else: _id = "NewObject"
        return "<%s: %s>" % (self.__class__.__name__, _id)
        
    def __str__(self):
        return self.get_json()


class ManagedUser(OpenIDMObject):
    path = "managed/user"