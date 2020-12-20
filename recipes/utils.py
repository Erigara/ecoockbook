from ecookbook.utils import upload_to


def recipe_image_path(instance):
    return f'recipes/recipe_image/{instance.recipe.pk}'


def step_path(instance):
    return f'recipes/step_image/{instance.recipe.pk}'


def category_path(instance):
    return f'recipes/category_image/{instance.pk}'


recipe_image_upload_to = upload_to(path=recipe_image_path)
step_upload_to = upload_to(path=step_path)
category_upload_to = upload_to(path=category_path)
