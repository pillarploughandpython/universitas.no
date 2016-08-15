# -*- coding: utf-8 -*-
"""
Admin for frontpage app.
"""

from django.contrib import admin
from django.forms import Textarea
from .models import StoryModule, FrontpageStory, StaticModule
from apps.photo.admin import ThumbAdmin
import autocomplete_light
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.safestring import mark_safe
from django.template import Context, Template


class StoryModuleInline(admin.TabularInline):
    model = StoryModule
    fields = ('position', 'columns', 'height',),
    extra = 0

@admin.register(FrontpageStory)
class FrontpageStoryAdmin(AdminImageMixin, ThumbAdmin, admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(FrontpageStory, exclude=())
    form.Meta.widgets = {
        'lede': admin.widgets.AdminTextareaWidget(attrs={'rows':3})
    }
    save_on_top = True
    list_per_page = 25
    list_display = (
        'id',
        'kicker',
        'headline',
        'lede',
        # 'imagefile',
        'parent_story',
        'thumbnail',
        # 'placements',
    )
    readonly_fields = ['thumbnail']

    list_editable = (
        'headline',
        # 'kicker',
        # 'lede',
    )
    inlines = (
        StoryModuleInline,
    )
    search_fields = (
        'headline',
        'kicker',
    )

    def parent_story(self, instance):
        template = Template(
            '<div class="parent story">'
            '<a href="{{story.get_edit_url}}">({{ story.pk }})</a> '
            '<a href="{{story.get_absolute_url}}">{{ story.title }}</a>'
            '</div>'
        )
        context = Context({'story':instance.story})
        return mark_safe(template.render(context))


@admin.register(StoryModule)
class StoryModuleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 25
    list_display = (
        'id',
        'frontpage_story',
        'publication_date',
        'position',
        'columns',
        'height',
        'frontpage',
    )

    list_editable = (
        'position',
        'columns',
        'height',
    )
    # inlines = (
    #     FrontpageStoryInline,
    # )


@admin.register(StaticModule)
class StaticModuleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 25
    list_display = (
        'id',
        'position',
        'columns',
        'height',
        'content',
        'frontpage',
    )

    list_editable = (
        'position',
        'columns',
        'height',
    )
