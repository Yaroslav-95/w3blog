from django.apps import AppConfig

SETTINGS = {
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
    'enable_rss': True,
}

class WeblogConfig(AppConfig):
    name = 'weblog'
