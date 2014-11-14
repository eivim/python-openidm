# Eivind Mikkelsen <eivind@loom.no>
# 2014-11-14

import json, copy

class ClientError(Exception):
    pass

class OpenIDMObject(object):
    def __init__(self, _path="managed/user", _id=None, idm=False, **data):
        self._path = _path
        self._id = _id
        self._idm = idm
        self._loaded = False
        self._data = data
        self._original = {}
        self._client = None

    def uri(self):
        if self._id:
            return "%s/%s" % (self._path, self._id)
        else:
            return self._path

    def set_client(self, client):
        self._client = client

    def read(self):
        if self._id and self._idm:
            json = self._client.read(self._path, self._id)
            self._loaded = True
            self._data = json
            self._original = json.copy()
        else:
            raise ClientError("Can't read object which is not in OpenIDM.")

    def save(self):
        if not self._idm:
            return self.create()
        return self.patch()
        
    def clone(self, replace={}):
        new = copy.copy(self)
        if '_id' in new._data: del new._data['_id']
        if '_rev' in new._data: del new._data['_rev']
        new._id = None
        new._idm = False
        new._original = new._data.copy()
        
        for key in replace:
            new._data[key] = replace[key]
        
        return new
    
    def create(self):
        if self._idm:
            raise ClientError("Can't create object which already exists in OpenIDM.")
        
        if not self._client:
            raise ClientError("No client set, use set_client()")
        
        try:
            newObject = self._client.create(self._path, self._data)
            self._data = self._original = newObject
            self._idm = True
            self._loaded = True
            self._id = self._data['_id']
            return self
        except:
            raise
        
    def delete(self):
        if not self._idm: raise ClientError("Object not from OpenIDM, can't delete.")
        if not self._id: raise ClientError("No known _id for object, can't delete.")
        try:
            response = self._client.delete(self.uri())
            self._data = {}
            self._original = {}
            self._id = None
            self._idm = False
            return None
        except:
            raise

    def patch(self):
        if not self._idm or not self._id: raise ClientError("Object not from OpenIDM. Use create() for new objects.")
        if not self._loaded: self.read()
        patch = []
        for key in self._data:
            if key in self._original:
                if(self._original[key] != self._data[key]):
                    patch.append({ "operation" : "replace", "field" : key, "value" : self._data[key] })
            else:
                patch.append({ "operation" : "add", "field" : key, "value" : self._data[key]})
        
        for key in self._original:
            if not key in self._data:
                patch.append({"operation" : "remove", "field" : key, "value" : self._original[key]})
                
        if patch:
            try:
                response = self._client.patch(self.uri(), patch)
                self._original = response
                self._data = response.copy()
                self._loaded = True
                return self
            except:
                raise
    
    def get_json(self):
        if self._idm and not self._loaded: self.read()
        return json.dumps(self._data, sort_keys=True, indent=2)
    
    def __getattr__(self, item):
        if self._id and self._idm and not self._loaded: self.read()
            
        if item.startswith("_") and item != "_rev":
            return dict.__getattr__(self, item)
        return self._data[item]
        
    def __setattr__(self, item, value):
        if item.startswith("_") and item != "_rev":
            return dict.__setattr__(self, item, value)
        else:
            if self._idm and not self._loaded: self.read()
            self._data[item] = value
            
    def __delattr__(self, item):
        if item.startswith("_") and item != "_rev":
            return dict.__delattr__(self, item)
        else:
            if self._id and self._idm and not self._loaded: self.read()
            del self._data[item]

    def __repr__(self):
        if self._id:
            return "<%s: %s/%s>" % (self.__class__.__name__, self._path, self._id)
        else:
            return "<%s: %s>" % (self.__class__.__name__, self._path)
        
    def __str__(self):
        return self.get_json()
        
    def __unicode__(self):
        return self.get_json()
