"""
the views
"""

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import (
    # JsonResponse,
    HttpResponse,
    # HttpResponseNotFound,
    # HttpResponseForbidden,
)
from django.shortcuts import render, redirect
from django.utils.html import format_html


from skillplans import __title__
from skillplans.app_settings import avoid_cdn
from skillplans.models import AaSkillplansCharacter
from skillplans.utils import (
    # add_no_wrap_html,
    # create_link_html,
    # create_fa_button_html,
    LoggerAddTag,
    messages_plus,
    # yesno_str,
)

from esi.decorators import token_required

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter
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


@login_required
@permission_required("memberaudit.basic_access")
@token_required(scopes=AaSkillplansCharacter.get_esi_scopes())
def add_character(request, token) -> HttpResponse:
    """
    adding a character
    :param request:
    :param token:
    :return:
    """
    token_char = EveCharacter.objects.get(character_id=token.character_id)

    try:
        character_ownership = CharacterOwnership.objects.select_related(
            "character"
        ).get(user=request.user, character=token_char)
    except CharacterOwnership.DoesNotExist:
        messages_plus.error(
            request,
            format_html(
                "You can register your main or alt characters."
                "However, character <strong>{}</strong> is neither. ",
                token_char.character_name,
            ),
        )
    else:
        with transaction.atomic():
            character, _ = AaSkillplansCharacter.objects.update_or_create(
                character_ownership=character_ownership
            )

        # tasks.update_character.delay(character_pk=character.pk)

        messages_plus.success(
            request,
            format_html(
                "<strong>{}</strong> has been registered. "
                "Note that it can take a minute until all character data is visible.",
                character.character_ownership.character,
            ),
        )

    return redirect("skillplans:dashboard")


def remove_character(request, character_id: int):
    """
    remove a character
    :param request:
    :param character_id:
    """


def character_view(request, character_id: int) -> HttpResponse:
    """
    character view
    :param request:
    :param character_id:
    """
