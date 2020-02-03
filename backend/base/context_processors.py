import logging

from django.conf import settings

logger = logging.getLogger(__name__)

DEFAULT_STAGE_ENV_SETTINGS = {
    'development': {"name": "Development", "color": '#4fc14f'},
    'staging': {"name": "Staging", "color": '#ffa500'},
    'production': {"name": "Production", "color": '#ff0000'},
}


config = getattr(
    settings,
    'STAGE_ENV_SETTINGS',
    DEFAULT_STAGE_ENV_SETTINGS
)
stage = getattr(
    settings,
    "STAGE_ENV",
    "production"
)


def stage_environ(request):
    try:
        return {
            "STAGE_NAME": config.get(stage).get("name"),
            "STAGE_COLOR": config.get(stage).get("color")
        }
    except Exception as e:
        logger.error(e)
        return {}
