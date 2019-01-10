
# w3blog version 0.5 #

w3blog is a simple blog engine for Django, with some focus on multilingual capabilities. It includes all of the basic features expected of a traditional Web log (also known as blog), as well as multilingual features, i.e. translations of blog posts which are delivered automatically in the user's preferred language using the internationalization capabilities of Django, enabling the possibility of targeting people from different countries in a single blog/site.

This django app is still a work in progress. More features will be added/completed in the near future. Currently the app's strings are translated only to English (en), Russian (ru), and Spanish (es).

To install, run "pip install w3blog". Currently tested to be compatible with Django 1.11 and 2.0.

## New in v0.5 ##

CSS and JS have been completely reworked to get rid of bloat (ie Bootstrap and JQuery), and provide a much nicer default look. Besides those improvements, new features include:

* An option to enable built-in dynamic load of more posts through ajax instead of the default good old pagination model. ('dynamic_load' = True).
* An option to use infinite scroll for dynamic load (more posts load automatically when scrolling to the bottom; "'dynamic_load' = True" and "'infinite_load' = True").
* Option to make the sidebar float (only for medium/big screen sizes) ('floating_sidebar' = True).
* Comments now include the date they were published (for some reason forgot to add that on previous versions).

If you encounter any errors or problems when using this Django app, please do make sure to open an issue on this project's Github page, or if you don't have Github account (and don't wish to create one), send me an email at contact@yaroslavps.com. Note: if you are using something like outlook (or any other big company email) my response email might end up in your spam folder or might be even blocked altogether by your email provider.

### Quick Start ###

1. Add "weblog" to your INSTALLED_APPS setting in your settings.py

2. Include the app as well as django-summernote in your project's urls.py; for example:

```python
url(r'^blog/', include('weblog.urls')),
url(r'^summernote/', include('django_summernote.urls')),
```

3. Migrate the models to the database by running "python manage.py migrate".

4. You can configure and customize the blog by adding and modifying to your liking/needs the following settings to your settings.py:

```python
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
    'dynamic_load': False, # New in version 0.5
    'infinite_load': False, # New in version 0.5
    'floating_sidebar': False, # New in version 0.5. Doesn't affect small screens (ie mobile devices, etc.)
    'enable_rss': True,
    'home_title': 'Welcome to the blog!',
}
```

5. Note that if you use your own base template, you will need to link "weblog/css/weblog.css" and "weblog/js/weblog.js" in your html head. Alternatively you can write your own custom css (or even js), or just extend the default css and js with your own. For reference you can check the project's templates and css in its Github page, especially if you want to rewrite completely the templates with your own.

Read more about it here: https://www.yaroslavps.com/weblog/python/w3blog-blog-engine/

Note: This package depends on the following python packages (besides Django and their dependencies): django-summernote

This project was previously named django-weblog, however, I had to renamed it due to there being an existing package with the same name in PyPI.

### Changelog ###

You can view a short summary of changes for each release in the releases section of the project's page on Github.

Note: If you had already made migrations by yourself for this app before version 0.5.2, you might notice that django is telling you that there are new unapplied migrations. Apply them as you usually would, and if a "Programming Error: column "x" exists in..." happens, run "python manage.py migrate --fake weblog".
