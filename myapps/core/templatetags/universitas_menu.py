""" Top megamenu for Universitas """

import logging
from django import template
from myapps.stories.models import Section, Story
from myapps.issues.models import PrintIssue

register = template.Library()
logger = logging.getLogger('universitas')


# @register.inclusion_tag('universitas-menu.html')
@register.inclusion_tag('old-menu.html')
def universitas_menu(active_section):

    sections = [
        Section.objects.get(title__iexact=title) for title in [
            'nyheter',
            'kultur',
            'debatt',
            'magasin',
        ]
    ]

    latest_issue = PrintIssue.objects.exclude(pdf=None).order_by(
        'issue__publication_date').last()

    context = {
        'sections': sections,
        'active_section': active_section,
        'latest_issue': latest_issue,
    }
    return context


@register.inclusion_tag('top-stories.html')
def top_stories(section, number, order_by):
    stories = Story.objects.published().filter(
        story_type__section=section
    ).order_by(order_by)[:number]

    context = {
        "stories": stories,
    }
    return context
