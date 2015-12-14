# coding: utf-8

from collections import Counter
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from celery import task

from .models import Position, Contributor, Stint

logger = logging.getLogger(__name__)

class Contributions:

    """ Helper object to calculate stints and contributions """

    def __init__(self, contributor):
        self.contributor = contributor
        self.bylines = contributor.byline_set.exclude(
            story__publication_date=None).order_by('story__publication_date')
        self.in_house_bylines = self.bylines.exclude(
            story__story_type__section__title='Debatt')
        self.sections = Counter(
            self.bylines.values_list(
                'story__story_type__section__title',
                flat=True))
        self.credits = Counter(
            self.bylines.values_list('credit', flat=True)
        )

    @property
    def is_external(self):
        return self.in_house_bylines.count() == 0

    @property
    def stints(self):
        return Stint.objects.filter(contributor=self.contributor)

    def create_stints(self):
        journalist_stint = self._create_stint(
            'journalist', [
                'text', 'by', 'text and photo'])
        photographter_stint = self._create_stint(
            'fotograf', [
                'photo', 'text and photo'])
        illustrator_stint = self._create_stint('illustratør', ['illustration'])
        return self.stints

    def _create_stint(self, position_title, byline_types):
        bylines = self.in_house_bylines.filter(credit__in=byline_types)
        position = Position.objects.get_or_create(title=position_title)[0]
        if bylines:
            stint = Stint.objects.get_or_create(
                contributor=self.contributor,
                position=position)[0]
            stint.start_date = bylines.first().story.publication_date.date()
            stint.end_date = bylines.last().story.publication_date.date()
            stint.save()
            return stint

    def get_status(self, save=False):
        cutoff = timezone.timedelta(days=30 * 6)
        if self.is_external:
            status = Contributor.EXTERNAL
        else:
            try:
                last_contribution = self.bylines.last().story.publication_date
            except AttributeError:
                status = Contributor.UNKNOWN
            else:
                if timezone.now() - last_contribution > cutoff:
                    status = Contributor.RETIRED
                else:
                    status = Contributor.ACTIVE
        if save:
            self.contributor.status = status
            self.contributor.save()
        return status

@task
def update_contributor_statuses(pks=None):
    if pks is None:
        queryset = Contributor.objects.all()
    else:
        queryset = Contributor.objects.filter(pk__in=pks)
    for contributor in queryset:
        contr = Contributions(contributor)
        contr.get_status(save=True)
        msg = '{name} {status}, {stints}'.format(
            name=contributor.display_name,
            status=contributor.get_status_display(),
            stints=','.join(str(stint) for stint in contr.stints),
        )
        logger.debug(msg)

@task
def update_contributor_stints(pks=None):
    if pks is None:
        queryset = Contributor.objects.all()
    else:
        queryset = Contributor.objects.filter(pk__in=pks)
    for contributor in queryset:
        contr = Contributions(contributor)
        contr.create_stints()
        msg = '{stints}'.format(
            stints=', '.join(str(stint) for stint in contr.stints),
        )
        logger.debug(msg)
