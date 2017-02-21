from boundaries.models import *
from games.models import *

from django.apps import apps


def clear_game_objects():

    game_models = apps.all_models['games']
    clearing_models= [model.objects.all().delete() for model in game_models.values()]

    if any([model.objects.count() for model in game_models.values()]) > 0:
        return False

    else:
        return True

