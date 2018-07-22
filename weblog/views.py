from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from .apps import SETTINGS as blog_settings
from .models import BlogPost, Translation, PostComment, Category, CategoryTranslation, PostCommentForm
from .templatetags.weblog_extras import MONTHS
import datetime

#Need to change the way this works later
IS_MULTILINGUAL = blog_settings['multilingual']
BASE_TEMPLATE = blog_settings['base_template']
BLOG_TITLE = blog_settings['blog_title']
SHOW_SIDEBAR = blog_settings['show_sidebar']
POSTS_PER_PAGE = blog_settings['posts_per_page']
SHOW_AUTHOR = blog_settings['show_author']
USE_AUTHORS_USERNAME = blog_settings['use_authors_username']
ENABLE_COMMENTS = blog_settings['enable_comments']
ALLOW_ANON_COMMENTS = blog_settings['allow_anon_comments']

# View for the blog's home page, as well as category and archive pages
def Index(request, **kwargs):
    context_dict = blog_settings.copy()
    now = datetime.datetime.now()
    all_pages = BlogPost.objects.filter(published=True, publish_date__lte=now)
    category = None

    # Check for arguments to see if it is the main page, category page, or archive
    if kwargs is not None:
        category_slug = kwargs.get('category_slug')
        year = kwargs.get('year')
        month = kwargs.get('month')
    if category_slug:
        if category_slug == 'misc':
            all_pages = BlogPost.objects.filter(published=True, publish_date__lte=now, categories=None)
            context_dict['category'] = 'misc'
        else:
            category = get_object_or_404(Category, slug=category_slug)
            context_dict['category'] = category
            all_pages = BlogPost.objects.filter(published=True, publish_date__lte=now, categories__slug=category_slug)
    if year:
        context_dict['year'] = year
        all_pages = BlogPost.objects.filter(published=True, publish_date__lte=now, publish_date__year=year)
        context_dict['breadcrumbs'] = [{'url': reverse('weblog:ArchiveIndex', kwargs={'year': year}), 'name': str(year)},]
        if month:
            context_dict['month'] = MONTHS[int(month)-1]
            all_pages = all_pages.filter(published=True, publish_date__lte=now, publish_date__month=month)
            context_dict['breadcrumbs'].append({'url': reverse('weblog:ArchiveIndex', kwargs={'year': year, 'month': month}), 'name': MONTHS[int(month)-1]})

    # Check how many blog posts there are in total, to calculate into how many pages
    # the index needs to be divided
    post_count = all_pages.count()
    if post_count < 1:
        return render(request, 'weblog/index.html', context_dict)
    page = 0
    if request.GET.get('page'):
        page = int(request.GET['page'])-1
    if page * POSTS_PER_PAGE + 1 > post_count:
        page = 0
    context_dict['current_page'] = page+1
    slice_start = page*POSTS_PER_PAGE
    slice_end = page*POSTS_PER_PAGE + POSTS_PER_PAGE
    if slice_end >= post_count:
        slice_end = post_count
    if post_count % POSTS_PER_PAGE == 0:
        last_page = int(post_count/POSTS_PER_PAGE)
    else:
        last_page = int(post_count/POSTS_PER_PAGE)+1
    context_dict['last_page'] = last_page

    # Check for pinned posts if it is the home page of the blog
    # and get the pinned and necessary posts depending on the page
    posts_raw = list(all_pages[slice_start:slice_end])
    if len(kwargs) < 1:
        for pinned_post in BlogPost.objects.filter(pinned=True).order_by('-pin_priority'):
            if pinned_post in posts_raw:
                posts_raw.remove(pinned_post)
            posts_raw.append(pinned_post)

    # Get the language from the user agent, if there's none, use the default
    current_language = translation.get_language()
    if current_language is None:
        current_language = settings.LANGUAGE_CODE

    # If it is a category page, get the category url and breadcrumbs
    if category_slug:
        if IS_MULTILINGUAL and category_slug != 'misc':
            category_translations = CategoryTranslation.objects.filter(category=category)
            if category_translations.count() > 0:
                for cat_trans in category_translations:
                    if current_language[0:2] == cat_trans.language[0:2]:
                        context_dict['category'] = cat_trans
        if category_slug == 'misc':
            context_dict['breadcrumbs'] = [{'url': reverse('weblog:CategoryIndex', kwargs={'category_slug': category_slug}), 'name': pgettext_lazy('Posts without category', 'Uncategorized')},]
        else:
            context_dict['breadcrumbs'] = [{'url': reverse('weblog:CategoryIndex', kwargs={'category_slug': category_slug}), 'name': context_dict['category']},]

    # Earlier we got just the posts from BlogPost model, now, if we are using the localization capabilities
    # we check for the language in use and select the appropiate translation language if available
    # otherwise default to the original blog post, or fallback language
    posts = []
    pinned_posts = []
    for post_raw in posts_raw:
        post = {'publish_date': post_raw.publish_date, 'url': post_raw.get_absolute_url()}
        if SHOW_AUTHOR:
            post['author'] = post_raw.author.get_full_name()
            if USE_AUTHORS_USERNAME:
                post['author'] = post_raw.author.get_username()
        translation_exists = False
        post_translations = Translation.objects.filter(post=post_raw)
        if post_translations.count() < 1 or not IS_MULTILINGUAL:
            post['title'] = post_raw.title
            post['content'] = post_raw.content
            post['preview_image'] = post_raw.preview_image
            if len(post_raw.preview_text) > 5:
                post['preview_text'] = post_raw.preview_text
            else:
                post['preview_text'] = post_raw.content.split('</p>', 1)[0]+'</p>'
        else:
            post_trans = None
            orig_lang = post_raw.original_language
            if len(orig_lang) < 2:
                orig_lang = settings.LANGUAGE_CODE[0:2]
            post['languages'] = [orig_lang,]
            for post_translation in post_translations:
                post['languages'].append(post_translation.language)
                if current_language[0:2] == post_translation.language[0:2]:
                    post_trans = post_translation
            if post_trans:
                post['title'] = post_trans.title
                post['content'] = post_trans.content
                post['current_language'] = post_trans.language
                post['preview_image'] = post_trans.preview_image
                if len(post_trans.preview_text) > 5:
                    post['preview_text'] = post_trans.preview_text
                else:
                    post['preview_text'] = post_trans.content.split('</p>', 1)[0]+'</p>'
            else:
                post['title'] = post_raw.title
                post['content'] = post_raw.content
                post['current_language'] = orig_lang
                post['preview_image'] = post_raw.preview_image
                if len(post_raw.preview_text) > 5:
                    post['preview_text'] = post_raw.preview_text
                else:
                    post['preview_text'] = post_raw.content.split('</p>', 1)[0]+'</p>'
        if post_raw.pinned:
            pinned_posts.append(post)
        else:
            posts.append(post)
    context_dict['posts'] = posts
    context_dict['pinned_posts'] = pinned_posts
    return render(request, 'weblog/index.html', context_dict)


def PostView(request, category_slug, post_slug, language=None):
    # If the multilingual setting is off, but somehow a language was passed
    # in the url, redirect to the original post
    if language and not IS_MULTILINGUAL:
        redirect('weblog:PostView', category_slug=category_slug, post_slug=post_slug)

    post = get_object_or_404(BlogPost, slug=post_slug)
    context_dict = blog_settings.copy()
    context_dict['comment_form'] = PostCommentForm()
    context_dict['post_url'] = post.get_absolute_url()
    post_translations = Translation.objects.filter(post=post)
    category = None
    # Get the current language in case there is a translation for the post in that language
    current_language = translation.get_language()
    if current_language is None:
        current_language = settings.LANGUAGE_CODE

    # Check to see if the category slug is misc, if it is, it means that the
    # post doesn't belong in any category
    if category_slug:
        if category_slug == 'misc':
            context_dict['category'] = 'misc'
        else:
            category = get_object_or_404(Category, slug=category_slug)
            context_dict['category'] = category
            # If we have the multilingual setting on, get the translation for the category
            if IS_MULTILINGUAL:
                category_translations = CategoryTranslation.objects.filter(category=category)
                if category_translations.count() > 0:
                    for cat_trans in category_translations:
                        if current_language[0:2] == cat_trans.language[0:2]:
                            context_dict['category'] = cat_trans
        # Put the necessary data about the category for the breadcrumbs
        if category_slug == 'misc':
            context_dict['breadcrumbs'] = [{'url': reverse('weblog:CategoryIndex', kwargs={'category_slug': category_slug}), 'name': pgettext_lazy('Posts without category', 'Uncategorized')},]
        else:
            context_dict['breadcrumbs'] = [{'url': reverse('weblog:CategoryIndex', kwargs={'category_slug': category_slug}), 'name': context_dict['category']},]

    # Put the necessary information about the author, based on the
    # current project's settings
    if SHOW_AUTHOR:
        context_dict['post_author'] = post.author.get_full_name()
        if USE_AUTHORS_USERNAME:
            context_dict['post_author'] = post.author.get_username()

    # Should we allow comments?
    if ENABLE_COMMENTS:
        context_dict['comments'] = PostComment.objects.filter(post=post)

    # If this is a POST request, it (probably) means that the user is attempting to post a comment
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        context_dict['comment_submission'] = True
        # Check that the form data is clean and correct
        if form.is_valid():
            comment_content = form.cleaned_data['content']
            # Make sure that either anonymous comments are allowed or
            # that the user is authenticated
            if request.user.is_authenticated:
                new_comment = PostComment(author=request.user, post=post, content=comment_content)
                new_comment.save()
            elif ALLOW_ANON_COMMENTS:
                new_comment = PostComment(post=post, content=comment_content)
                new_comment.save()
            else:
                context_dict['comment_submission_error'] = _('You need to sign in to submit a comment')
        else:
            context_dict['comment_submission_error'] = _('Error submitting comment: Invalid data')

    # Put the post content in the context dictionary
    context_dict['post'] = post
    # Get all the categories, and if necessary, their translations
    if post.categories.all().count() > 0:
        context_dict['post_categories'] = []
        for raw_category in post.categories.all():
            next_category = {'name': raw_category.name, 'slug': raw_category.slug}
            if CategoryTranslation.objects.filter(category=raw_category).count() > 0 and IS_MULTILINGUAL:
                for category_translation in CategoryTranslation.objects.filter(category=raw_category):
                    if current_language[0:2] == category_translation.language[0:2]:
                        next_category['name'] = category_translation.name
            context_dict['post_categories'].append(next_category)

    # Breadcrumbs data about the post
    if post_translations.count() < 1 or not IS_MULTILINGUAL:
        context_dict['breadcrumbs'].append({'url': post.get_absolute_url(), 'name': post.title})
        return render(request, 'weblog/post.html', context_dict)

    # Get the original languageof the post, if it is set, otherwise
    # assume that it is the language of the site (the one set in settings.py)
    orig_lang = post.original_language
    if len(orig_lang) < 2:
        orig_lang = settings.LANGUAGE_CODE[:2]
    # Get the languages for all the translations of the post, so that
    # if a visitor desires, they can read the post in another language
    # agnostic of their locale or site preferences
    context_dict['post_languages'] = []
    post_languages = []
    for post_translation in post_translations:
        post_languages.append(post_translation.language[:2].lower())
        if language and language == post_translation.language[0:2]:
            context_dict['post_translation'] = post_translation
        elif current_language[0:2] == post_translation.language[0:2] and not language:
            context_dict['post_translation'] = post_translation
    for lang in settings.LANGUAGES:
        if lang[0][:2] == orig_lang.lower():
            context_dict['post_languages'].append(lang)
            continue
        if lang[0][:2] in post_languages:
            context_dict['post_languages'].append(lang)

    # If we are reading a translation, and not the original text,
    # use those translations for the breadcrumbs, otherwise, use the original title
    if 'post_translation' in context_dict:
        context_dict['breadcrumbs'].append({'url': post.get_absolute_url(), 'name': post_translation.title})
    else:
        context_dict['breadcrumbs'].append({'url': post.get_absolute_url(), 'name': post.title})
    return render(request, 'weblog/post.html', context_dict)

# A dirty hack to change the language on the fly.
# Was meant for testing purposes, but I suppose
# it can also be used on production.
# Be aware that it changes the language settings
# for the whole site/project for the session
def ChangeLanguage(request, language):
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    if request.GET.get('next'):
        response = HttpResponseRedirect(request.GET['next'])
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    response = HttpResponseRedirect(reverse('weblog:Index'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
