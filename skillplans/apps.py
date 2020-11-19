# -*- coding: utf-8 -*-

"""
app config
"""

from django.apps import AppConfig

from skillplans import __version__


class AaSkillplansConfig(AppConfig):
    """
    application config
    """

    name = "skillplans"
    label = "skillplans"
    verbose_name = "Skillplans v{}".format(__version__)
