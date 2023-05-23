# astrocat

Crossmatching Astrophysical Catalogs

This function will take two DataFrames (main and external), the column names for the R.A. and Dec. for each DataFrame, the list of column names to be added to the main DataFrame, and the maximum distance for a match between catalogs. It will add the new columns to the main df, fill in values for true matches (within max_distance), and return the updated main DataFrame.


## How to use

Intall astrocat package: 

```
!install git+https://github.com/BrunoArsioli/astrocat.git
```

then, import crossmatch_catalog from astrocat.crossmatch library:

```
from astrocat.crossmatch import crossmatch_catalog
```



## crossmatch_astrocat() function:

Here we have a description of the crossmatch_astrocat() function and its input variables. 

```
crossmatch_astrocat(df_main, df_ext, ra_main, dec_main, ra_ext, dec_ext, col_list, max_distance)
```

The crossmatch_astrocat() is meant to crossmatches two astronomical catalogs.

This function finds matches between two catalogs of astronomical objects, given a maximum distance for a match.
For each object in the main catalog, the closest object in the external catalog within max_distance is identified.
If such a match is found, specified information from the external catalog is added to the main catalog.

Parameters
----------

* df_main : DataFrame
    The main catalog DataFrame. Each row represents an astronomical object.

* df_ext : DataFrame
    The external catalog DataFrame. Each row represents an astronomical object.

* ra_main, dec_main : str
    Column names for the right ascension and declination in df_main.

* ra_ext, dec_ext : str
    Column names for the right ascension and declination in df_ext.

* col_list : list of str
    Column names in df_ext that will be added to df_main for matching objects.

* max_distance : float
    Maximum distance in arcseconds to consider for a match.

Returns
-------

* DataFrame
    The updated main catalog DataFrame, with new columns added from df_ext for matching objects.

Examples
--------

Here is how to use this function:

  **i)** If you have CatWISE2020 as the external catalog and want to write W1 and W2 info to your main DataFrame

    col_list = ['W1mag', 'w1snr', 'W2mag', 'w2snr']
    df_main_updated = crossmatch_astrocat(df_main, df_ext, 'RA1', 'DEC1', 'RA2', 'DEC2', col_list, 2.0)


  **ii)** If you want to track the external_source from where the information is read, add a source_id or source_name to col_list:

    col_list = ['WISEname', 'W1mag', 'w1snr', 'W2mag', 'w2snr']
    df_main_updated = crossmatch_astrocat(df_main, df_ext, 'RA1', 'DEC1', 'RA2', 'DEC2', col_list, 2.0)
