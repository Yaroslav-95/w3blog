from django.apps import AppConfig

SETTINGS = {
    'enable_comments': False,
    'allow_anon_comments': False,
    'multilingual': True,
    'blog_title': 'w3blog',
    'base_template': 'weblog_base.html',
    'show_author': True,
    'use_authors_username': True,
    'show_sidebar': True,
    'show_categories': False,
    'show_archive': True,
    'posts_per_page': 10,
    'dynamic_load': False,
    'infinite_load': False,
    'floating_sidebar': False,
    'enable_rss': True,
}

class WeblogConfig(AppConfig):
    name = 'weblog'
