#!/usr/bin/env python

from osgeo import gdal
from osgeo import ogr

gdal.UseExceptions()

def get_bounding_box(geom):
    """
    Gets the Envelope of an OGRGeometry as a Polygon.
    """
    min_x, min_y, max_x, max_y = geom.GetEnvelope()

    wkt = 'POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))' % \
        (min_x, min_y, min_x, max_y,
        max_x, max_y, max_x, min_y,
        min_x, min_y)

    return ogr.CreateGeometryFromWkt(wkt)

