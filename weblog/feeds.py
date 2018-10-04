from django.contrib.syndication.views import Feed
from django.conf import settings
from django.urls import reverse
from weblog.models import BlogPost, Translation, Category, CategoryTranslation
from weblog.apps import SETTINGS as blog_settings
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils import translation
import datetime

class BlogFeed(Feed):

    def get_object(self, request, category_slug=None):
        self.current_language = translation.get_language()
        if self.current_language is None:
            self.current_language = settings.LANGUAGE_CODE
        if category_slug:
            if category_slug != 'misc':
                self.category = Category.objects.get(slug=category_slug)
                self.category_name = self.category.name
            if blog_settings['multilingual'] and category_slug != 'misc':
                category_translations = CategoryTranslation.objects.filter(category=self.category)
                if category_translations.count() > 0:
                    for cat_trans in category_translations:
                        if self.current_language[0:2] == cat_trans.language[0:2]:
                            self.category_name = cat_trans
            elif category_slug == 'misc':
                self.category_name = pgettext_lazy('Posts without category', 'Uncategorized')
                return category_slug
        return None

    def title(self, obj):
        if obj:
            return _('%(blog_title)s\'s %(category_name)s RSS feed') % {'blog_title': blog_settings['blog_title'], 'category_name': self.category_name}
        return _('%(blog_title)s RSS feed') % {'blog_title': blog_settings['blog_title']}

    def link(self, obj):
        if obj:
            return reverse('weblog:CategoryIndex', kwargs={'category_slug': obj})
        return reverse('weblog:Index')

    def description(self, obj):
        if obj:
            return _('Latest %(category_name)s blog posts on %(blog_title)s') % {'blog_title': blog_settings['blog_title'], 'category_name': self.category_name}
        return _('Latest blog posts on %(blog_title)s') % {'blog_title': blog_settings['blog_title']}

    def items(self, obj):
        now = datetime.datetime.now()
        if obj:
            return BlogPost.objects.filter(category__slug=obj, published=True, publish_date__lte=now).order_by('-publish_date')[:blog_settings['posts_per_page']]
        return BlogPost.objects.order_by('-publish_date').filter(published=True, publish_date__lte=now)[:blog_settings['posts_per_page']]

    def item_title(self, item):
        translation_exists = False
        post_translations = Translation.objects.filter(post=item)
        if post_translations.count() > 0 and blog_settings['multilingual']:
            orig_lang = item.original_language
            if len(orig_lang) < 2:
                orig_lang = settings.LANGUAGE_CODE[0:2]
            for post_translation in post_translations:
                if self.current_language[0:2] == post_translation.language[0:2]:
                    return post_translation.title
        return item.title

    def item_pubdate(self, item):
        return item.publish_date

    def item_author_name(self, item):
        if blog_settings['show_author']:
            if blog_settings['use_authors_username']:
                return item.author.get_username()
            return item.author.get_full_name()
        return None

    def item_description(self, item):
        translation_exists = False
        post_translations = Translation.objects.filter(post=item)
        if post_translations.count() > 0 and blog_settings['multilingual']:
            orig_lang = item.original_language
            if len(orig_lang) < 2:
                orig_lang = settings.LANGUAGE_CODE[0:2]
                for post_translation in post_translations:
                    if self.current_language[:2] == post_translation.language[:2]:
                        return post_translation.content
        return item.content
