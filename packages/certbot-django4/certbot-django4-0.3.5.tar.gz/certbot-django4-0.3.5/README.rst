==============
Certbot Django
==============

|  |license| |kit| |format|

This is a fork of the combined plugin for the certbot ACME client and also a Django-app for proving ACME challenges.

This updated version aims to provide support for django 4 and onwards as well.

When creating the "certbot" user that adds the ACME challenges on the server,
note that you must explicitly add the ACMEChallenge permissions in the django admin.
The user "certbot" also needs to be staff.
Just having him as an admin is not enough.

**Original package Documentation**: https://certbot-django.readthedocs.io


.. |license| image:: https://img.shields.io/pypi/l/certbot-django.svg
    :target: https://pypi.python.org/pypi/certbot-django4
.. |kit| image:: https://badge.fury.io/py/certbot-django.svg
    :target: https://pypi.python.org/pypi/certbot-django4
.. |format| image:: https://img.shields.io/pypi/format/certbot-django.svg
    :target: https://pypi.python.org/pypi/certbot-django4
