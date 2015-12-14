# -*- coding: utf-8 -*-
"""
Admin for contributors app.
"""

from django.contrib import admin
from django.template import Context, Template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from .models import Contributor, Position, Stint
from . import tasks
from apps.stories.admin import BylineInline


def byline_image(obj):
    t = Template("{% load byline_image %}{% byline_image contributor size %}")
    d = {"contributor": obj, "size": "80x80"}
    html = t.render(Context(d))
    return mark_safe(html)

class StintInline(admin.TabularInline,):
    model = Stint
    fields = ['position', 'start_date', 'end_date']
    extra = 1

def update_contributors(modeladmin, request, queryset):
    update_contributors.short_description = _('update contributors')
    pks = list(queryset.values_list('pk', flat=True))
    tasks.update_contributor_stints.delay(pks)
    tasks.update_contributor_statuses.delay(pks)

def mark_as_invalid(modeladmin, request, queryset):
    mark_as_invalid.short_description = _('mark as invalid')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):

    actions = [update_contributors, mark_as_invalid]

    form = autocomplete_light.modelform_factory(
        Contributor,
        exclude=()
    )

    list_display = (
        'display_name',
        'bylines_count',
        'verified',
        'status',
        byline_image,
    )

    list_editable = (
        'display_name',
        'verified',
    )

    search_fields = (
        'display_name',
    )

    inlines = [
        StintInline,
        BylineInline,
    ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):

    def active_now(self, instance):
        active = instance.active()
        if len(active) == 1:
            return str(active[0].contributor)
        else:
            return str(len(active))


    def groups_list(self, instance):
        return ', '.join(str(group) for group in instance.groups.all())

    list_display = [
        'title',
        'active_now',
        'groups_list',
        ]


@admin.register(Stint)
class StintAdmin(admin.ModelAdmin):

    form = autocomplete_light.modelform_factory(
        Stint,
        exclude=()
    )

    list_display = (
        '__str__',
        'position',
        'start_date',
        'end_date',
        )

    list_editable = (
        'position',
        'start_date',
        'end_date',
        )
