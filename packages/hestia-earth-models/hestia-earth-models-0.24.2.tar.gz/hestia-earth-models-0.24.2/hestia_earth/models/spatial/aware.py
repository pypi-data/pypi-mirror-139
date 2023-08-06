from hestia_earth.models.log import logShouldRun
from .utils import download, has_geospatial_data
from . import MODEL

KEY = 'aware'
EE_PARAMS = {
    'collection': 'AWARE',
    'type': 'vector',
    'field': 'Name'
}


def _download(site: dict):
    return download(
        collection=EE_PARAMS['collection'],
        ee_type=EE_PARAMS['type'],
        fields=EE_PARAMS['field'],
        latitude=site.get('latitude'),
        longitude=site.get('longitude'),
        boundary=site.get('boundary')
    ).get(EE_PARAMS['field'])


def _run(site: dict): return _download(site)


def _should_run(site: dict):
    should_run = has_geospatial_data(site, by_region=False)
    logShouldRun(MODEL, None, should_run, key=KEY)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else None
