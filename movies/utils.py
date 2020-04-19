from django.db import transaction


def nested_commit_on_success(func):
    def _nested_commit_on_success(*args, **kwds):
        with transaction.atomic():
            return func(*args, **kwds)

    return _nested_commit_on_success
