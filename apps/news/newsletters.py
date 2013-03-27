"""This data provides an official list of newsletters and tracks
backend-specific data for working with them in the email provider.

It's used to lookup the backend-specific newsletter name from a
generic one passed by the user. This decouples the API from any
specific email provider."""
from django.core.cache import cache

from news.models import Newsletter


__all__ = ('clear_newsletter_cache', 'newsletter_field', 'newsletter_name',
           'newsletter_fields', 'newsletter_names')


CACHE_KEY = "newsletters_cache_data"


def _newsletters():
    """Returns a data structure with the data about newsletters.
    It's cached until clear_newsletter_cache() is called, so we're
    not constantly hitting the database for data that rarely changes.

    The returned data structure looks like::

        {
            'by_name': {
                'newsletter_name_1': a Newsletter object,
                'newsletter_name_2': another Newsletter object,
            },
            'by_vendor_id': {
                'NEWSLETTER_ID_1': a Newsletter object,
                'NEWSLETTER_ID_2': another Newsletter object,
            }
        }
    """
    data = cache.get(CACHE_KEY)
    if data is None:
        data = _get_newsletters_data()
        cache.set(CACHE_KEY, data)

    return data


def _get_newsletters_data():
    by_name = {}
    by_vendor_id = {}
    for nl in Newsletter.objects.all():
        by_name[nl.slug] = nl
        by_vendor_id[nl.vendor_id] = nl
    return {
        'by_name': by_name,
        'by_vendor_id': by_vendor_id,
        }


def newsletter_field(name):
    """Lookup the backend-specific field (vendor ID) for the newsletter"""
    return _newsletters()['by_name'][name].vendor_id


def newsletter_name(field):
    """Lookup the generic name for this newsletter field"""
    return _newsletters()['by_vendor_id'][field].slug


def newsletter_names():
    """Get a list of all the available newsletters"""
    return _newsletters()['by_name'].keys()


def newsletter_fields():
    """Get a list of all the newsletter backend-specific fields"""
    return  _newsletters()['by_vendor_id'].keys()


def clear_newsletter_cache():
    cache.delete(CACHE_KEY)
