# import library
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np

def crossmatch_astrocats(df_main, df_ext, ra_main, dec_main, ra_ext, dec_ext, col_list, max_distance):
    """
    Crossmatches two astronomical catalogs.

    This function finds matches between two catalogs of astronomical objects, given a maximum distance for a match.
    For each object in the main catalog, the closest object in the external catalog within max_distance is identified.
    If such a match is found, specified information from the external catalog is added to the main catalog.

    Parameters
    ----------
    df_main : DataFrame
        The main catalog DataFrame. Each row represents an astronomical object.
    df_ext : DataFrame
        The external catalog DataFrame. Each row represents an astronomical object.
    ra_main, dec_main : str
        Column names for the right ascension and declination in df_main.
    ra_ext, dec_ext : str
        Column names for the right ascension and declination in df_ext.
    col_list : list of str
        Column names in df_ext that will be added to df_main for matching objects.
    max_distance : float
        Maximum distance in arcseconds to consider for a match.

    Returns
    -------
    DataFrame
        The updated main catalog DataFrame, with new columns added from df_ext for matching objects.

    Examples
    --------
    Here is how to use this function:
        If you have CatWISE2020 as the external catalog and want to write W1 and W2 info to your main DataFrame
        df_main_updated = crossmatch_astrocats(df_main, df_ext, 'RA1', 'DEC1', 'RA2', 'DEC2', ['W1mag', 'w1snr', 'W2mag', 'w2snr'], 2.0)
    """

    # create cmain, Astropy object that holds a list of the main catalog coordinates
    cmain = SkyCoord(ra=df_main[ra_main]*u.deg, dec=df_main[dec_main]*u.deg, frame='icrs')

    # create cext, Astropy object that holds a list of the external catalog coordinates
    cext = SkyCoord(ra=df_ext[ra_ext]*u.deg, dec=df_ext[dec_ext]*u.deg, frame='icrs')

    # find closest sources in external catalog for each source in the main catalog
    # idxext has the same size as df_main, and carries the indexes from the external catalog for each source in the main catalog
    idxext, s2d, _ = cmain.match_to_catalog_sky(cext)

    # prepare new columns for the main DataFrame
    for col_name in col_list:
        df_main[col_name] = np.nan

    # get indices of s2d (those are the same index of idxext) that identify 'true matches' within max_distance
    idxmain_match = np.where(s2d.arcsec <= max_distance)

    # idxmain_match is a tuple; extract and store the first list 
    idxmain_match = idxmain_match[0]

    # loop over the columns to extract info
    for col_name in col_list:
        for idx in idxmain_match:
            df_main.at[idx, col_name] = df_ext.at[idxext[idx], col_name]
    
    return df_main
