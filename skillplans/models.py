# coding=utf-8

"""
Our Models
"""

from django.db import models


class AaSkillplansGeneralPermissions(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:
        verbose_name = "Skillplans"
        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access the Skillplans module"),)
