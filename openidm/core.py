import json
import httplib2

from openidm.models import OpenIDMObject

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode

class ClientError(Exception):
    pass

def checkResponse(response, content, expected=200):
    if response.status == expected:
        return True
    else:
        raise ClientError("%s %s\n%s" % (response.status, response.reason, content))

class Client(object):
    """
    The core OpenIDM client which handles HTTP requests against REST API.
        
    >>> from openidm import Client
    >>>
    >>> openidm = Client()
    >>> users = openidm.query("managed/user", { "_queryId" : "query-all-ids" })
    >>>
    >>> for user in users:
    >>>     print(user)
    """
    
    def __init__(self, baseURL="http://localhost:8080/openidm",
            username="openidm-admin", password="openidm-admin"):
            
        self.baseURL = baseURL
        self.headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json;charset=utf-8",
            "X-OpenIDM-Username" : username,
            "X-OpenIDM-Password" : password
        }
        
        self.http = httplib2.Http()
        

    def read(self, resource, _id=None):
        if _id:
            return self._get(resource + "/" + _id)
        return self._get(resource)
        
    def query(self, resource, query={ "_queryId" : "query-all-ids"}):
        if not query:
            raise ClientError("Query must be provided")
        
        content = self._get(resource, query)
        if(content and 'result' in content):
            objects = []
            for r in content['result']:
                obj = OpenIDMObject(resource, r['_id'], idm=True)
                obj.set_client(self)
                objects.append(obj)
            return objects
            
    def patch(self, resource, json):
        return self._submit(resource, json, "PATCH")
    
    def action(self, resource, action, json={}, expected=200):
        return self._submit("%s?_action=%s" % (resource, action), json, "POST", expected)
    
    def create(self, resource, json):
        return self.action(resource, 'create', json, expected=201)
    
    def delete(self, resource):
	return self._submit(resource, None, "DELETE")
 
    def _get(self, resource, qs={}):
        request = self.uri(resource)
        if qs: request = request + "?" + urlencode(qs)
        
        response, content = self.http.request(request,
            method = "GET",
            body = None,
            headers = self.headers
        )
            
        if checkResponse(response, content, 200):
            return json.loads(content.decode())    
        
    def _submit(self, resource, data, method, expected=200):
        request = self.uri(resource)
        response, content = self.http.request(request,
            method = method,
            body = json.dumps(data),
            headers = self.headers
        )
        
        if checkResponse(response, content, expected):
            return json.loads(content.decode())
            
    def uri(self, resource):
        return "%s/%s" % (self.baseURL, resource)
