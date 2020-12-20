import uuid
from pathlib import Path
from functools  import partial

from rest_framework import serializers
from rest_framework.reverse import reverse


def specific_upload_to(instance, filename, path):
    name = uuid.uuid4()
    extensions = Path(filename).suffixes
    if callable(path):
        path = path(instance)
    return f'{path}/{name}{"".join(extensions)}'


def upload_to(path):
    return partial(specific_upload_to, path=path)


class Empty:
    pass


def nested_gettattr(obj, attr, default=Empty):
    original_obj = obj
    nested_attrs = attr.split('.')
    for nested_attr in nested_attrs:
        obj = getattr(obj, nested_attr, None)
        if obj is None:
            if default is Empty:
                raise AttributeError(f"'{original_obj.__class__.__name__}' has no attribute '{attr}'")
            else:
                return default
    return obj


class RelatedHyperlink(serializers.HyperlinkedRelatedField):
    lookup_url_kwargs = None
    lookup_fields = None

    def __init__(self, view_name=None, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', [self.lookup_field, ])
        self.lookup_url_kwargs = kwargs.pop('lookup_url_kwargs', [self.lookup_field, ])
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format=None):
        url_kwargs = {}
        for lookup_url_kwarg, lookup_field in zip(self.lookup_url_kwargs, self.lookup_fields):
            url_kwargs |= {lookup_url_kwarg: nested_gettattr(obj, lookup_field)}

        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

