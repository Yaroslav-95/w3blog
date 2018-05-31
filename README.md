
# Weblog version 0.3 #

Weblog is a simple blog engine for Django, with some focus on multilingual capabilities. It includes all of the basic features expected of a traditional Web log (also known as blog), as well as multilingual features, i.e. translations of blog posts which are delivered automatically in the user's preferred language using the internationalization capabilities of Django, enabling the possibility of targeting people from different countries in a single blog/site.

This django app is still a work in progress. More features will be added/completed in the near future. Currently the app's strings are translated only to English (en), Russian (ru), and Spanish (es),

### Quick Start ###

1. Add "weblog" to your INSTALLED_APPS setting in your settings.py

2. Include the app in your project's urls.py; for example:

    url(r'^blog/', include('weblog.urls')),

3. Migrate the models to the database by running "python manage.py migrate"

4. You can configure and customize the blog by adding and modifying to your liking/needs the following settings to your settings.py:

    WEBLOG_SETTINGS = {
        'enable_comments': False,
        'allow_anon_comments': False,
        'multilingual': True,
        'blog_title': 'Django-Weblog',
        'base_template': 'weblog_base.html',
        'show_author': True,
        'use_authors_username': True,
        'show_sidebar': True,
        'show_categories': False,
        'show_archive': True,
        'posts_per_page': 10,
    }

5. Note that if you use your own base template, you will either need to link bootstrap in your base template's head, or write your own styles for the site based on the bootstrap classes. You will as well need to link files "weblog/css/weblog.css" and "weblog/js/weblog.js" in your html head.

Note: This package depends on the following python packages (besides Django and their dependencies): django-summernote
