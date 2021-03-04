"""
the tasks
"""

from bravado.exception import (
    HTTPBadGateway,
    HTTPGatewayTimeout,
    HTTPServiceUnavailable,
)

from celery import shared_task

from eveuniverse.core.esitools import is_esi_online

from skillplans import __title__
from skillplans.utils import LoggerAddTag

from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce


logger = LoggerAddTag(get_extension_logger(__name__), __title__)

DEFAULT_TASK_PRIORITY = 6
ESI_ERROR_LIMIT = 50
ESI_TIMEOUT_ONCE_ERROR_LIMIT_REACHED = 60
ESI_SOV_STRUCTURES_CACHE_KEY = "sov_structures_cache"

# params for all tasks
TASK_DEFAULT_KWARGS = {
    "time_limit": 1200,  # stop after 20 minutes
}

# params for tasks that make ESI calls
TASK_ESI_KWARGS = {
    **TASK_DEFAULT_KWARGS,
    **{
        "autoretry_for": (
            OSError,
            HTTPBadGateway,
            HTTPGatewayTimeout,
            HTTPServiceUnavailable,
        ),
        "retry_kwargs": {"max_retries": 3},
        "retry_backoff": True,
    },
}


@shared_task(**TASK_DEFAULT_KWARGS)
def run_skill_updates() -> None:
    """
    update all sov campaigns
    """

    if not is_esi_online():
        logger.info(
            "ESI is currently offline. Can not start ESI related tasks. Aborting"
        )
        return

    logger.info("Updating sovereignty structures and campaigns from ESI.")

    update_skills.apply_async(priority=DEFAULT_TASK_PRIORITY)


@shared_task(**{**TASK_ESI_KWARGS}, **{"base": QueueOnce})
def update_skills() -> None:
    """
    update skills
    """
