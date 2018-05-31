from django import template
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.conf import settings
from weblog.apps import SETTINGS as blog_settings
from weblog.models import Category, CategoryTranslation, BlogPost
import datetime

IS_MULTILINGUAL = blog_settings['multilingual']

MONTHS = (
    _('January'),
    _('February'),
    _('March'),
    _('April'),
    _('May'),
    _('June'),
    _('July'),
    _('August'),
    _('September'),
    _('October'),
    _('November'),
    _('December'),
)

register = template.Library()

@register.inclusion_tag('weblog/sidebar_categories.html')
def get_sidebar_categories(selected_cat_slug=None):
    now = datetime.datetime.now()
    current_language = translation.get_language()
    if current_language is None:
        current_language = settings.LANGUAGE_CODE
    context_dict = {'categories': [], 'selected_cat_slug': selected_cat_slug}
    for raw_category in Category.objects.all():
        next_category = {'name': raw_category.name, 'slug': raw_category.slug}
        if CategoryTranslation.objects.filter(category=raw_category).count() > 0 and IS_MULTILINGUAL:
            for category_translation in CategoryTranslation.objects.filter(category=raw_category):
                if current_language[0:2] == category_translation.language[0:2]:
                        next_category['name'] = category_translation.name
        context_dict['categories'].append(next_category)
    if BlogPost.objects.filter(published=True, publish_date__lte=now, categories=None).count() > 0:
        context_dict['categories'].append({'name': pgettext_lazy('Posts without category', 'Uncategorized'), 'slug': 'misc'})
    return context_dict


@register.inclusion_tag('weblog/sidebar_archive.html')
def get_sidebar_archive():
    if BlogPost.objects.all().count() < 1:
        return {}
    now = datetime.datetime.now()
    oldest_post = BlogPost.objects.filter(published=True).reverse()[0]
    first_year = oldest_post.publish_date.year
    first_month = oldest_post.publish_date.month
    newest_post = BlogPost.objects.filter(published=True, publish_date__lte=now)[0]
    latest_year = newest_post.publish_date.year
    latest_month = newest_post.publish_date.month
    c_month = first_month
    c_year = first_year
    archive = []
    while c_year <= latest_year:
        year_posts = BlogPost.objects.filter(publish_date__year=c_year, publish_date__lte=now, published=True)
        if year_posts.count() > 0:
            this_years_months = []
            while (c_year < latest_year or c_month <= latest_month) and c_month <= 12:
                if year_posts.filter(publish_date__month=c_month, publish_date__lte=now, published=True).count() > 0:
                    this_years_months.append((c_month, MONTHS[c_month-1]))
                c_month+=1
            archive.append((c_year, this_years_months))
        c_year+=1
        c_month=1
    archive.reverse()
    return {'archive': archive}
