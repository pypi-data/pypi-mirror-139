from astropy import coordinates, units
from astroquery import vizier
from . import get_radec

vz = vizier.Vizier()

def cone_gleam(radec, radius):
    """ query gleam catalog
    radec can be any format (parsed by get_radec).
    radius in degrees.
    """

    ra, dec = get_radec(radec)
    co = coordinates.SkyCoord(ra, dec, unit=units.deg)
    res = vz.query_region(co, radius=radius*units.deg, catalog='VIII/100/gleamegc')

    return res.values()
