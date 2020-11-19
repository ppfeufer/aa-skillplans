# -*- coding: utf-8 -*-

"""
the views
"""

import datetime as dt

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# from django.utils.translation import gettext_lazy as _

from skillplans import __title__
from skillplans.app_settings import avoid_cdn
from skillplans.utils import LoggerAddTag

from allianceauth.services.hooks import get_extension_logger


logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("skillplans.basic_access")
def dashboard(request):
    """
    Index view
    """

    logger.info("Module called by %s", request.user)

    context = {
        "avoidCdn": avoid_cdn(),
    }

    return render(request, "skillplans/dashboard.html", context)
