from astroquery import irsa
from astropy import coordinates, units
from . import get_radec


def cone_wise(radec, radius=5/3600, selectcol=['designation', 'ra', 'dec', 'w1mpro', 'w1sigmpro', 'w2mpro',
                                               'w2sigmpro', 'w3mpro', 'w3sigmpro', 'w4mpro', 'w4sigmpro'],
              catalog='allwise_p3as_psd'):
    """ cone search from wise cryogenic all-sky survey
    ra, dec in degrees, radius in arcsec.
    https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-dd?catalog=allwise_p3as_psd
    """

    ra, dec = get_radec(radec)
    co = coordinates.SkyCoord(ra, dec, unit='deg')
    tab = irsa.Irsa.query_region(co, catalog=catalog, selcols=','.join(selectcol))

    return tab


def cone_pyvo(ra, dec, radius=5, table='allwise_p3as_psd'):
    """ Query IRSA with pyvo
    TODO: use unwise? need to figure out which columns

    Default table is allwise.
    Cone search radius in arcseconds.
    """

    url = "https://irsa.ipac.caltech.edu/SCS?table=allwise_p3as_psd"
    co = coordinates.SkyCoord(ra, dec, unit='deg')
    tab = pyvo.conesearch(url, pos=(co.ra.deg, co.dec.deg), radius = rad/3600).to_table()

    return tab
