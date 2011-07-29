#!/usr/bin/env python

import shutil

from osgeo import gdal
from osgeo import ogr

from ogrkit.cli import OGRKitUtility
from ogrkit.utils import get_bounding_box

gdal.UseExceptions()

class OGRDifference(OGRKitUtility):
    description = 'Produce a shapefile by subtracting a set of shapefiles from the input.'

    def add_arguments(self):
        self.argparser.add_argument('masks', metavar='MASKS', nargs='+', type=str)

    def main(self):
        source = ogr.Open(self.args.input, False)
        source_layer = source.GetLayer(0)

        try:
            shutil.rmtree(self.args.output)
        except OSError:
            pass

        driver = ogr.GetDriverByName('ESRI Shapefile')
        dest = driver.CreateDataSource(self.args.output)
        dest_layer = dest.CreateLayer('difference', geom_type=ogr.wkbMultiPolygon)
        
        for i in range(source_layer.GetLayerDefn().GetFieldCount()):
            dest_layer.CreateField(source_layer.GetLayerDefn().GetFieldDefn(i))

        mask_features = []
        mask_boxes = []

        for mask in self.args.masks:
            geo = ogr.Open(mask, False)
            layer = geo.GetLayer(0)

            for feature in layer:
                mask_features.append(feature)
                mask_boxes.append(get_bounding_box(feature.GetGeometryRef()))

        for feature in source_layer:
            masked_feature = ogr.Feature(feature_def=source_layer.GetLayerDefn())
            masked_feature.SetFrom(feature)

            masked_geometry = feature.GetGeometryRef().Clone()

            for (i, mask_feature) in enumerate(mask_features):
                bounding_box = mask_boxes[i]

                if not masked_geometry.Intersects(bounding_box):
                    continue

                masked_geometry = masked_geometry.Difference(mask_feature.GetGeometryRef())

            masked_feature.SetGeometryDirectly(masked_geometry)
            dest_layer.CreateFeature(masked_feature)

