python-openidm
==============

OpenIDM REST Client for Python.

Note: Just started, not very usable yet (i.e. read-only).

Usage with Python Interactive Shell
-----------------------------------

```
# ./shell.py

Python Interactive Shell for OpenIDM Client
>>>
>>> users = openidm.query(ManagedUser)
>>> users
[<ManagedUser: f824a95d-f1a9-4c17-8d65-eca4a146eb30>, <ManagedUser: c1e05202-ce4c-42a3-8f09-f2549ce51ca2>]
>>>
>>> print users[0]
{
  "_id": "f824a95d-f1a9-4c17-8d65-eca4a146eb30",
  "_rev": "7",
  "accountStatus": "active",
  "email": "eivindm@conduct.no",
  "familyName": "Mikkelsen",
  "givenName": "Eivind",
  "lastPasswordAttempt": "Fri Jan 31 2014 01:11:34 GMT+0100 (CET)",
  "lastPasswordSet": "",
  "passwordAttempts": "0",
  "phoneNumber": "+4740002240",
  "roles": "openidm-admin,openidm-authorized",
  "userName": "eivind"
}
```
