==================
Core Dashboard App
==================

Resource management via a dashboard for the curator core project.

Quickstart
==========

1. Add "core_dashboard_app" to your INSTALLED_APPS setting
----------------------------------------------------------

.. code:: python

      INSTALLED_APPS = [
          ...
          'core_dashboard_app',
      ]

2. Include the core_dashboard_app URLconf in your project urls.py
-----------------------------------------------------------------

.. code:: python

      url(r'^dashboard/', include('core_dashboard_app.urls')),
