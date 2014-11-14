python-openidm
==============

OpenIDM REST Client for Python.

Example usage with Python Interactive Shell
-------------------------------------------

```
# ./shell.py

Python Interactive Shell for OpenIDM Client
>>>
>>> users = openidm.query("managed/user")
>>> users
[<OpenIDMObject: managed/user/f824a95d-f1a9-4c17-8d65-eca4a146eb30>, <OpenIDMObject: managed/user/c1e05202-ce4c-42a3-8f09-f2549ce51ca2>]
>>>
>>> print users[0]
{
  "_id": "f824a95d-f1a9-4c17-8d65-eca4a146eb30",
  "_rev": "7",
  "accountStatus": "active",
  "email": "foo@bar.baz",
  "familyName": "Foo",
  "givenName": "Bar",
  "lastPasswordAttempt": "Fri Jan 31 2014 01:11:34 GMT+0100 (CET)",
  "lastPasswordSet": "",
  "passwordAttempts": "0",
  "phoneNumber": "",
  "roles": "",
  "userName": "foobar"
}

>>> for user in users:
>>>     user.roles = [ 'openidm-authorized' ]
>>>     user.save()
```
