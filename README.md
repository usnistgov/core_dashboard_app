# core_dashboard_app

core_dashboard_app is a Django app providing a way to manage your ressources through a dashboard.

## Quickstart

  1. Add "core_dashboard_app" to your INSTALLED_APPS setting like this::

  ```python
  INSTALLED_APPS = [
      ...
      'core_dashboard_app',
  ]
  ```

  2. Include the core_dashboard_app URLconf in your project urls.py like this::

  ```python
  url(r'^dashboard/', include('core_dashboard_app.urls')),
  ```
