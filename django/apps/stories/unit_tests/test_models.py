# -*- coding: utf-8 -*-
"""
Tests of stories app.
"""
import pytest
from apps.stories.models import Story

@pytest.mark.django_db
def test_nothing():
    ss = Story.objects.create()

