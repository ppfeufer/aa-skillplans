# -*- coding: utf-8 -*-

"""
pages url config
"""

from django.conf.urls import url

from skillplans import views


app_name: str = "skillplans"

urlpatterns = [
    url(r"^$", views.dashboard, name="dashboard"),
]
