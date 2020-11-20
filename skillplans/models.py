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
        verbose_name = "Skill Plans"
        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access the AA Skill Plans module"),)


class AaSkillplansCharacter(models.Model):
    """
    Character Model
    """

    # DB field definitions ...

    class Meta:
        default_permissions = ()

    @classmethod
    def get_esi_scopes(cls) -> list:
        """
        returns the ESI scopes needed for this model/module
        :return:
        """

        return [
            "esi-skills.read_skillqueue.v1",
            "esi-skills.read_skills.v1",
        ]
