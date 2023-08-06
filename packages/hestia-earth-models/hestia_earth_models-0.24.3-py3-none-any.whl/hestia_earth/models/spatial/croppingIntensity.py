from hestia_earth.schema import MeasurementStatsDefinition

from hestia_earth.models.log import logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement
from hestia_earth.models.utils.site import valid_site_type
from .utils import download, find_existing_measurement, has_geospatial_data, _site_gadm_id
from . import MODEL

TERM_ID = 'croppingIntensity'
EE_PARAMS = {
    'type': 'raster',
    'reducer': 'sum'
}


def _measurement(value: float):
    measurement = _new_measurement(TERM_ID, MODEL)
    measurement['value'] = [round(value, 7)]
    measurement['statsDefinition'] = MeasurementStatsDefinition.SPATIAL.value
    return measurement


def _download(site: dict):
    # 1) extract maximum monthly growing area (MMGA)
    MMGA_value = download(
        collection='MMGA',
        ee_type=EE_PARAMS['type'],
        reducer=EE_PARAMS['reducer'],
        fields=EE_PARAMS['reducer'],
        latitude=site.get('latitude'),
        longitude=site.get('longitude'),
        gadm_id=_site_gadm_id(site),
        boundary=site.get('boundary')
    )
    MMGA_value = MMGA_value.get(EE_PARAMS['reducer'], 0)

    # 2) extract area harvested (AH)
    AH_value = download(
        collection='AH',
        ee_type=EE_PARAMS['type'],
        reducer=EE_PARAMS['reducer'],
        fields=EE_PARAMS['reducer'],
        latitude=site.get('latitude'),
        longitude=site.get('longitude'),
        gadm_id=_site_gadm_id(site),
        boundary=site.get('boundary')
    )
    AH_value = AH_value.get(EE_PARAMS['reducer'])

    # 3) estimate croppingIntensity from MMGA and AH.
    return None if MMGA_value is None or AH_value is None or AH_value == 0 else (MMGA_value / AH_value)


def _run(site: dict):
    value = find_existing_measurement(TERM_ID, site) or _download(site)
    return [_measurement(value)] if value else []


def _should_run(site: dict):
    should_run = has_geospatial_data(site) and valid_site_type(site)
    logShouldRun(MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else []
