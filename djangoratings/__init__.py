import os.path
import warnings
import collections

__version__ = (0, 6, 0)

def _get_git_revision(path):
    revision_file = os.path.join(path, 'refs', 'heads', 'master')
    if not os.path.exists(revision_file):
        return None
    fh = open(revision_file, 'r')
    try:
        return fh.read()
    finally:
        fh.close()

def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, '..'))
    path = os.path.join(checkout_dir, '.git')
    if os.path.exists(path):
        return _get_git_revision(path)
    return None

__build__ = get_revision()

def lazy_object(location):
    def inner(*args, **kwargs):
        parts = location.rsplit('.', 1)
        warnings.warn('`djangoratings.{}` is deprecated. Please use `{}` instead.'.format(parts[1], location), DeprecationWarning)
        try:
            imp = __import__(parts[0], globals(), locals(), [parts[1]], -1)
        except:
            imp = __import__(parts[0], globals(), locals(), [parts[1]])
        func = getattr(imp, parts[1])
        if isinstance(func, collections.Callable):
            return func(*args, **kwargs)
        return func
    return inner

RatingField = lazy_object('djangoratings.fields.RatingField')
AnonymousRatingField = lazy_object('djangoratings.fields.AnonymousRatingField')
Rating = lazy_object('djangoratings.fields.Rating')
