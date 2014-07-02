import json
import httplib2
import inspect

from openidm.models import OpenIDMObject
from urllib import urlencode

class Error(Exception):
    pass

def checkResponse(response):
    if response.status == 200:
        return
    else:
        raise Error("%s %s" % (response.status, response.reason))

class Client(object):
    """
    The core OpenIDM client which handles HTTP communication with
    the ForgeRock OpenIDM REST API.
    
    Getting started:
    
    >>> from openidm import Client
    >>> from openidm.models import ManagedUser
    >>>
    >>> client = Client()
    >>> users = client.query(ManagedUser, { "_queryId" : "query-all-ids" })
    >>>
    >>> for user in users:
    >>>     print(user)
    """
    
    def __init__(self, baseURL="http://localhost:8080/openidm",
            userName="openidm-admin", password="openidm-admin"):
            
        self.baseURL = baseURL
        self.headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json;charset=utf-8",
            "X-OpenIDM-Username" : userName,
            "X-OpenIDM-Password" : password
        }
        
        self.http = httplib2.Http()
        

    def read(self, resource, _id=None):
        if _id:
            return self._get(resource.path + "/" + _id)
        return self._get(resource.path)
        
    
    def query(self, resource, query={ "_queryId" : "query-all-ids"}):
        if not query:
            raise Error("Query must be provided")
    
        if inspect.isclass(resource):
            uri = resource.path
        else:
            raise Error("Invalid target")
        
        content = self._get(uri, query)
        if(content and content.has_key('result')):
            objects = []
            for r in content['result']:
                obj = resource(r['_id'], idm=True)
                obj.set_client(self)
                objects.append(obj)
            return objects
                      
                      
    def _get(self, resource, qs={}):
        request = self.uri(resource)
        if qs: request = request + "?" + urlencode(qs)
          
        response, content = self.http.request(request,
            method = "GET",
            body = None,
            headers = self.headers
        )
            
        checkResponse(response)
        if(response.status == 200):
            return json.loads(content)
        
    def _post(self, resource, json):
        raise Error("Not implemented yet")
        
        
    def _put(self, resource, json):
        raise Error("Not implemented yet")
        
        
    def uri(self, resource):
        return "%s/%s" % (self.baseURL, resource)