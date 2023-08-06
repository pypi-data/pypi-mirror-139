# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astropy.units as u
from astropy.wcs import WCS
import numpy as np


def make_simple_wcs(skycoord, resolution, size):
    crpix = (size + 1) / 2
    cdelt = resolution.to(u.deg).value
    skycoord_icrs = skycoord.transform_to('icrs')
    ra = skycoord_icrs.ra.degree
    dec = skycoord_icrs.dec.degree

    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [crpix, crpix]
    wcs.wcs.cdelt = np.array([-cdelt, cdelt])
    wcs.wcs.crval = [ra, dec]
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]

    return wcs
