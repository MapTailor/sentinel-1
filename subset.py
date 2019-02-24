import snappy
from snappy import ProductIO as product
from snappy import HashMap as hash
from snappy import GPF as gpf

import os, sys

gpf.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
snappy.HashMap = snappy.jpy.get_type('java.util.HashMap')

path = "C:\\"

for folder in os.listdir(path):

    filename = folder + ".SAFE"

    dataset = os.path.join(path, folder, filename)
    dataset = dataset.format(sys.platform, os.sep)

    print dataset

    timestamp = folder.split("_")[5]
    date = timestamp[:8]

    parameters = hash()
    sources = hash()

    sentinel = product.readProduct(dataset + "//manifest.safe")

    WKTReader = snappy.jpy.get_type('com.vividsolutions.jts.io.WKTReader')

    wkt = "POLYGON((" \
          "14.1223022771676 36.116795674787561, " \
          "14.623741501140653 36.119420063224389, " \
          "14.625412269082306 35.766175579973442, " \
          "14.126199181086793 35.763584814742948, " \
          "14.1223022771676 36.116795674787561" \
          "))"
    geom = WKTReader().read(wkt)

    pols = ["VV", "VH"]

    for pol in pols:

        parameters.put('sourceBands', "Amplitude_" + pol)
        parameters.put('geoRegion', geom)
        parameters.put('copyMetadata', True)

        output = date + "_subset_" + pol
        checks = output + ".tif"

        writefile = os.path.join(path, folder, filename, output)
        checkfile = os.path.join(path, folder, filename, checks)

        if os.path.exists(checkfile) == True:
            pass

        else:

            item = gpf.createProduct("Subset", parameters, sentinel)
            product.writeProduct(item, writefile, 'GeoTIFF')
