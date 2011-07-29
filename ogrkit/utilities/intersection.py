#!/usr/bin/env python

import shutil

from osgeo import gdal
from osgeo import ogr

from ogrkit.cli import OGRKitUtility
from ogrkit.utils import get_bounding_box

gdal.UseExceptions()

class OGRIntersection(OGRKitUtility):
    description = 'Produce a shapefile by selecting only the intersection of the input and a mask.'

    def add_arguments(self):
        self.argparser.add_argument('mask', metavar='MASK', type=str)

    def main(self):
        source = ogr.Open(self.args.input, False)
        source_layer = source.GetLayer(0)

        try:
            shutil.rmtree(self.args.output)
        except OSError:
            pass

        driver = ogr.GetDriverByName('ESRI Shapefile')
        dest = driver.CreateDataSource(self.args.output)
        # TODO: should work with source geom_type
        dest_layer = dest.CreateLayer('intersection', geom_type=ogr.wkbMultiPolygon)
        
        for i in range(source_layer.GetLayerDefn().GetFieldCount()):
            dest_layer.CreateField(source_layer.GetLayerDefn().GetFieldDefn(i))

        mask_features = []
        mask_boxes = []

        geo = ogr.Open(self.args.mask, False)
        layer = geo.GetLayer(0)

        for feature in layer:
            mask_features.append(feature)
            mask_boxes.append(get_bounding_box(feature.GetGeometryRef()))

        for feature in source_layer:
            # Skip features that don't have any geometry
            if not feature.GetGeometryRef():
                continue

            masked_feature = ogr.Feature(feature_def=source_layer.GetLayerDefn())
            masked_feature.SetFrom(feature)

            masked_geometry = None

            for (i, mask_feature) in enumerate(mask_features):
                bounding_box = mask_boxes[i]

                if not feature.GetGeometryRef().Intersects(bounding_box):
                    continue

                new_piece = feature.GetGeometryRef().Intersection(mask_feature.GetGeometryRef())

                if new_piece:
                    if masked_geometry:
                        masked_geometry = masked_geometry.Union(new_piece)
                    else:
                        masked_geometry = new_piece

            # Don't create features which have been completely excluded
            if not masked_geometry:
                continue

            masked_feature.SetGeometryDirectly(masked_geometry)
            dest_layer.CreateFeature(masked_feature)

