=====
Admin Export
=====

Add export action in admin model list page.

Quick start
-----------
1. Install this package::

    pip install django-simple-export


2. Add "admin_export" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'admin_export',
    ]


3. Include the polls URLconf in your project urls.py like this::

    path('dae/', include('admin_export.urls')),


4. Add export annotation to your model in admin.py, for example::

    from admin_export.deco import dae_export

    @admin.register(YourModel)
    @dae_export(YourModel)
    class YourAdmin(admin.ModelAdmin):
        # ...


5. Start the development server and visit http://127.0.0.1:8000/admin/,
   then click to view the list of the model(you'll need the Admin app enabled).


6. There will be an 'Export' button in the page before 'Add' button.
   click this button, current data list will be exported into a file.
