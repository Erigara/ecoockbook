import uuid
from pathlib import Path
from functools  import partial


def specific_upload_to(path, instance, filename):
    name = uuid.uuid4()
    extensions = Path(filename).suffixes
    return f'{path}/{instance.pk}/{name}{"".join(extensions)}'


def upload_to(path):
    return partial(specific_upload_to, path=path)
