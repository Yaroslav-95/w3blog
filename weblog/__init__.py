from . import apps
from django.conf import settings

try:
    apps.SETTINGS['enable_comments'] = settings.WEBLOG_ENABLE_COMMENTS
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['allow_anon_comments'] = settings.WEBLOG_ALLOW_ANON_COMMENTS
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['multilingual'] = settings.WEBLOG_MULTILINGUAL
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['blog_title'] = settings.WEBLOG_TITLE
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['base_template'] = settings.WEBLOG_BASE_TEMPLATE
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['show_author'] = settings.WEBLOG_SHOW_AUTHOR
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['use_authors_username'] = settings.WEBLOG_USE_AUTHORS_USERNAME
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['show_sidebar'] = settings.WEBLOG_SHOW_SIDEBAR
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['show_categories'] = settings.WEBLOG_SHOW_CATEGORIES
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['show_archive'] = settings.WEBLOG_SHOW_ARCHIVE
except AttributeError:
    pass
except NameError:
    pass

try:
    apps.SETTINGS['posts_per_page'] = settings.WEBLOG_POSTS_PER_PAGE
except AttributeError:
    pass
except NameError:
    pass