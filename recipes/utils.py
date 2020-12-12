import uuid
from pathlib import Path


def step_image_upload_to(instance, filename):
    name = uuid.uuid4()
    extensions = Path(filename).suffixes
    return f'recipes/step/{name}{"".join(extensions)}'


def recipe_image_upload_to(instance, filename):
    name = uuid.uuid4()
    extensions = Path(filename).suffixes
    return f'recipes/image/{name}{"".join(extensions)}'