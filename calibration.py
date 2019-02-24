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

    timestamp = folder.split("_")[5]
    date = timestamp[:8]

    parameters = hash()
    sources = hash()

    pol = 'VV'

    sentinel = product.readProduct(os.path.join(dataset, date + "_subset_" + pol + ".tif"))

    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Amplitude_' + pol)
    parameters.put('selectedPolarisations', pol)
    parameters.put('outputImageScaleInDb', False)

    output = date + "_calibration_" + pol
    checks = output + ".tif"

    writefile = os.path.join(path, folder, filename, output)
    checkfile = os.path.join(path, folder, filename, checks)

    if os.path.exists(checkfile) == True:
        pass

    else:

        item = gpf.createProduct("Calibration", parameters, sentinel)
        product.writeProduct(item, writefile, 'GeoTIFF')
