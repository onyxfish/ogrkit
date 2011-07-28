ogrkit
======

A suite of command-line utilities implementing basic geometric operations. (Difference, Intersection, etc.)

This project is a cousin of `csvkit <http://github.com/onyxfish/csvkit>`_.

**Note: This is only a proof-of-concept to see if this idea makes sense.**

Installation
------------

It's easy!

::

    pip install ogrkit

Usage
-----

To try the difference utility::

    ogrdifference INPUT_SHAPEFILE OUTPUT_SHAPEFILE [MASK_SHAPEFILES...]

Note: this currently only works with shapefiles, but could be extended to work with any format supported by `OGR <http:/www.gdal.org/>`_.

Authors
-------

* Christopher Groskopf (`@onyxfish <http://twitter.com/onyxfish>`_)

License
-------

MIT

