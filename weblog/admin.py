from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from .apps import SETTINGS as blog_settings
from .models import BlogPost, Translation, PostComment, Category, CategoryTranslation


blogPostInlines = []
categoryInlines = []

class TranslationInline(admin.StackedInline, SummernoteInlineModelAdmin):
    model = Translation
    extra = 1

class CategoryTranslationInline(admin.StackedInline):
    model = CategoryTranslation
    extra = 1

class PostCommentInline(admin.StackedInline):
    model = PostComment
    extra = 0

if blog_settings['multilingual']:
    blogPostInlines.append(TranslationInline)
    categoryInlines.append(CategoryTranslationInline)

if blog_settings['enable_comments']:
    blogPostInlines.append(PostCommentInline)

class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'author', 'publish_date']
    list_filter = ['publish_date', 'categories']
    inlines = blogPostInlines
    summer_note_fields = '__all__'

    def get_form(self, request, obj=None, **kwargs):
        if not blog_settings['multilingual']:
            self.exclude = ('original_language', )
        form = super(BlogPostAdmin, self).get_form(request, obj, **kwargs)
        return form

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = categoryInlines

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category, CategoryAdmin)
