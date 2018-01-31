from django.apps import AppConfig

SETTINGS = {
    'enable_comments': False,
    'allow_anon_comments': True,
    'multilingual': True,
    'blog_title': 'Django-Weblog',
    'base_template': 'base.html',
    'show_author': True,
    'use_authors_username': True,
    'show_sidebar': True,
    'show_categories': False,
    'show_archive': True,
    'posts_per_page': 10,
}

class WeblogConfig(AppConfig):
    name = 'weblog'
