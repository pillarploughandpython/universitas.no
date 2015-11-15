"""Keyword and related stories"""

from django.utils.translation import ugettext_lazy as _
from django.db import models
from collections import Counter, defaultdict
import nltk
import re
import json

CORPUS_FILE = '/tmp/corpus.json'
CORPUSCOUNT_FILE = '/tmp/corpuscount.json'


class KeyWordStoryMixin(models.Model):

    class Meta:
        abstract = True

    keywords = models.CharField(
        verbose_name=_('keywords'),
        max_length=1024,
        blank=True,
    )

    related_stories = models.ManyToManyField(
        'stories.Story',
        verbose_name=_('related stories'),
    )

    def get_words(self):
        """Extract all words from text for natural language text processing"""
        content = [self.title, self.lede, self.bodytext_markup]
        content += [aside.aside.bodytext_markup for aside in self.asides()]
        for bl in self.byline_set.all():
            content.append(','.join([bl.contributor.display_name, bl.title]))
        text = '\n'.join(content)
        regex = re.compile(r'@[^:@ ]+:', flags=re.M)
        text = regex.sub('', text).replace('_', '').replace('Nomen Nescio', '')
        return re.findall(r"[-\w',.]*[\w]|[\w.,!?]", text)

    def build_keywords(self, corpus_dict=None, limit=10):
        """build keywords"""
        if corpus_dict is None:
            corpus_dict = get_corpus_dict()
        stems = stem_words(self.get_words())
        valid_words = (word for word in stems if word in corpus_dict)
        word_counts = Counter(valid_words).items()
        keywords = ((w, c, corpus_dict[w]) for w, c in word_counts)
        best = sorted(
            keywords,
            key=lambda kw: kw[1] / kw[2],
            reverse=True
        )[:limit]
        self.keywords = '\n'.join(kw[0] for kw in best)
        self.save(update_fields=['keywords'])
        return best

    def get_related_stories(self):
        """figure out related stories"""
        cls = self.__class__
        if not self.keywords:
            return cls.objects.none()
        scores = defaultdict(lambda: 0)
        keywords = self.keywords.split('\n')
        for keyword in keywords:
            candidates = cls.objects.exclude(
                pk=self.pk).filter(
                keywords__icontains=keyword)
            for candidate in candidates:
                score = 2 - (
                    (self.keywords.index(
                        keyword) / len(self.keywords)) +
                    (candidate.keywords.index(
                        keyword) / len(candidate.keywords))
                )
                scores[candidate.pk] += score
        pks = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)[:3]
        for pk in pks:
            self.related_stories.add(pk)


# def load_json_file(filename):
#     with open(filename, 'r') as fp:
#         data = json.load(fp)
#     return data


# def save_json_file(filename, data):
#     with open(filename, 'w') as fp:
#         json.dump(data, fp)


def try_json_first(filename):
    """decorator that memoizes json data if called with no args"""
    def decorator_wrapper(func):
        def func_wrapper(*args, **kwargs):
            if args or kwargs:
                return func(*args, **kwargs)
            try:
                with open(filename, 'r') as fp:
                    return json.load(fp)
            except FileNotFoundError:
                data = func()
                with open(filename, 'w') as fp:
                    json.dump(data, fp)
                return data
        return func_wrapper
    return decorator_wrapper


@try_json_first(CORPUSCOUNT_FILE)
def get_corpus_dict(**kwargs):
    cutoff = kwargs.get('cutoff', 5)
    corpus = get_corpus()
    counter = Counter(stem_words(corpus))
    corpdict = {w: count for w, count in counter.items() if count > cutoff}
    return corpdict


@try_json_first(CORPUS_FILE)
def get_corpus(**kwargs):
    """Create a list of all words in all stories"""
    queryset = kwargs.get('queryset', None)
    stemmed = kwargs.get('stemmed', False)
    if queryset is None:
        from .models import Story
        queryset = Story.objects.all()
    corpus = []
    counter = 0
    for story in queryset:
        counter += 1
        corpus.extend(story.get_words())
        corpus.append('\n')

    if stemmed:
        corpus = stem_words(corpus)

    return corpus


def stem_words(words, language='no'):
    stemmer = nltk.stem.snowball.NorwegianStemmer(ignore_stopwords=False)
    regex = re.compile('[-a-zA-ZæøåÆØÅ]+')
    words = [stemmer.stem(word.lower()) for word in words if regex.match(word)]
    return words
