=======
Dev_Sup
=======

Dev_Sup is a Django app that supports developer in process of creation of Django application.

Quick start
-----------

1. Add "dev_sup" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dev_sup',
    ]

2. Include the dev_sup URLconf in your project urls.py like this::

    path('', include('dev_sup.urls')),

Pro tip: include it after your ``admin`` paths, so it won't mess them up.

3. Configure your TEMPLATES settings like this::
    
    TEMPLATES = [
        {
            ...
            'DIRS': [os.path.join(BASE_DIR, "dev_sup/templates")],
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'dev_sup.context_processors.all',
                ],
            },
        },
    ]

You will probably need to add ``import os`` on top of your ``settings.py`` module.


4. Run ``python manage.py migrate`` to create the dev_sup models.

5. Run ``python manage.py generate_project`` to generate simple project.

6. Start the development server and visit http://127.0.0.1:8000/ to check out generated project.

7. Visit http://127.0.0.1:8000/admin to add more sites, links, drop down menus and page styles.

You will find more instructions in generated project's index page.
