from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name=pgettext_lazy('Noun, not personal name', 'Name'), blank=False, unique=True)
    slug = models.SlugField(max_length=60, verbose_name=_('Slug (URL)'), db_index=True, unique=True)
    parent_category = models.ForeignKey('self', verbose_name=_('Parent category'), null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return reverse('weblog:CategoryIndex', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = pgettext_lazy('Post category', 'Category')
        verbose_name_plural = pgettext_lazy('Post categories', 'Categories')

class CategoryTranslation(models.Model):
    name = models.CharField(max_length=250, verbose_name=pgettext_lazy('Noun, not personal name', 'Name'), blank=False)
    language = models.CharField(max_length=5, verbose_name=_('Language (ISO)'), blank=False)
    category = models.ForeignKey(Category, verbose_name = pgettext_lazy('Post category', 'Category'), blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def slug(self):
        return self.category.slug

    class Meta:
        verbose_name = _('Category name translation')
        verbose_name_plural = _('Category name translations')


class BlogPost(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    title = models.CharField(max_length=100, verbose_name=pgettext_lazy('As in name', 'Title'), blank=False)
    content = models.TextField(verbose_name=pgettext_lazy('Of post, comment, article, etc.', 'Content'), blank=False)
    preview_image = models.ImageField(upload_to='weblog/preview_images/%Y/%m/%d/', blank=True, verbose_name=_('Preview image'))
    preview_text = models.CharField(max_length=250, blank=True, verbose_name=_('Preview Text'))
    original_language = models.CharField(max_length=5, verbose_name=_('Original language (ISO)'), blank=True)
    slug = models.SlugField(max_length=100, verbose_name=_('Slug (URL)'), db_index=True, unique=True)
    categories = models.ManyToManyField(Category, verbose_name=pgettext_lazy('Post categories', 'Categories'), blank=True)
    pinned = models.BooleanField(verbose_name=_('Pin blog post'), default=False)
    pin_priority = models.IntegerField(verbose_name=_('Pinned post priority (if pinned)'), default=0)
    published = models.BooleanField(verbose_name=pgettext_lazy('Make post viewable', 'Published'))
    publish_date = models.DateTimeField(verbose_name=_('Publish date'))

    def get_absolute_url(self):
        if self.categories.all().count() > 0:
            category = self.categories.all()[0].slug
            return reverse('weblog:PostView', kwargs={'category_slug': category, 'post_slug': self.slug})
        else:
            return reverse('weblog:PostView', kwargs={'category_slug': 'misc', 'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date', 'title']
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

class Translation(models.Model):
    post = models.ForeignKey(BlogPost, verbose_name=pgettext_lazy('Noun, as in blog post', 'Post'), on_delete=models.CASCADE)
    language = models.CharField(max_length=5, verbose_name=_('Language (ISO)'), blank=False)
    title = models.CharField(max_length=100, verbose_name=pgettext_lazy('As in name', 'Title'), blank=False)
    content = models.TextField(verbose_name=pgettext_lazy('Of post, comment, article, etc.', 'Content'), blank=False)
    preview_image = models.ImageField(upload_to='weblog/preview_images/%Y/%m/%d/', blank=True, verbose_name=_('Preview image'))
    preview_text = models.CharField(max_length=250, blank=True, verbose_name=_('Preview Text'))

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')

class PostComment(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'), null=True, blank=True, on_delete=models.PROTECT)
    post = models.ForeignKey(BlogPost, verbose_name=pgettext_lazy('Noun, as in blog post', 'Post'), on_delete=models.CASCADE)
    content = models.TextField(verbose_name=pgettext_lazy('Of post, comment, article, etc.', 'Content'), blank=False)

    class Meta:
        verbose_name = pgettext_lazy('Noun', 'Comment')
        verbose_name_plural = pgettext_lazy('Noun', 'Comments')

class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ('content',)
        labels = {'content': ''}
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }
