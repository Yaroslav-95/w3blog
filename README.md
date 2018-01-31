
# Weblog version 0.2 #

Weblog is a simple blog engine for Django, with some focus on multilingual capabilities. It includes all of the basic features expected of a traditional Web log (also known as blog), as well as multilingual features, i.e. translations of blog posts which are delivered automatically in the user's preferred language using the internationalization capabilities of Django, enabling the possibility of targeting people from different countries in a single blog/site.

This django app is still a work in progress. More features will be added/completed in the near future. Currently the app's strings are translated only to English (en), Russian (ru), and Spanish (es),

### Quick Start ###

1. Add "weblog" to your INSTALLED_APPS setting in your settings.py

2. Include the app in your project's urls.py; for example:

    url(r'^blog/', include('weblog.urls')),

3. Migrate the models to the database by running "python manage.py migrate"

4. You can configure and customize the blog by adding and modifying to your liking/needs the following settings to your settings.py:

    WEBLOG_ENABLE_COMMENTS = True #Should comments be allowed on your blog
    WEBLOG_ALLOW_ANON_COMMENTS = False #Are visitors allowed to leave comments without signing in (note that you should provide a way for them to register and login if you wish to allow only registered user's comments)
    WEBLOG_MULTILINGUAL = True #Enable multilingual features of the weblog app (i.e.: BlogPost and Category translations)
    WEBLOG_TITLE = 'Weblog Test' #The name/title of your blog (e.g.: Example Site Newsletter)
    WEBLOG_BASE_TEMPLATE = 'site_base.html' #Which base template to use (if not indicated, it will use its own base template)
    WEBLOG_SHOW_AUTHOR = True #Should the author of the post be shown (it uses the Django User model)
    WEBLOG_USE_AUTHORS_USERNAME = True #Show the username of the author instead of the fullname
    WEBLOG_SHOW_SIDEBAR = True #Enable the sidebar
    WEBLOG_SHOW_CATEGORIES = True #Show links to categories in the sidebar
    WEBLOG_SHOW_ARCHIVE = True #Show the archive treeview (Years>Months) in the sidebar
    WEBLOG_POSTS_PER_PAGE = 10 #Number of posts that should be shown per page

5. Note that if you use your own base template, you will either need to link bootstrap in your base template's head, or write your own styles for the site based on the bootstrap classes. You will as well need to link files "weblog/css/weblog.css" and "weblog/js/weblog.js" in your html head.