import pygeowms.wms as wms


def test_wms_encoding():

    url = (
        'http://127.0.0.1:8001/ESACCI-L3S_SOILMOISTURE-SSMV-COMBINED-1978-2013-fv01.2_3.nc.wms?LAYERS=sm&'
        'cmap=cpa_SWI_ASCAT_Dataviewer&TIME=2013-12-31T00:00:00&COLORBARRANGE=0.0,1.0&TRANSPARENT=TRUE&'
        'SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&'
        'BBOX=67.5,0,90,22.5&WIDTH=256&HEIGHT=256')

    results = wms.encode(url)
    assert results.bbox == [67.5, 0, 90, 22.5]
    assert results.width == 256
    assert results.height == 256
