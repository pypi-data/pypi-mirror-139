==================
django-labportalen
==================
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) ![Django](https://img.shields.io/badge/Django-3.2.8-blue)

``django-labportalen`` is a Django app to communicate with swedish Labportalen service.
Suitable with eRemiss version 3.1.0.

Features
--------
- Create remiss for a patient against a case.
- Fetch analyses reports from SFTP server.


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "labportalen" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'labportalen',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('labportalen/', include('labportalen.urls')),

3. Run ``python manage.py migrate`` to create the labportalen models.

4. Start the development server and visit http://127.0.0.1:8000/labportalen/api/
   to see available labportalen end-points.