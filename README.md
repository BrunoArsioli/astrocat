# astrocat

Crossmatching Astrophysical Catalogs

Astrocat, an open-source project aimed at supporting researchers and data scientists with crossmatching of catalogs. In astrophysics, this task is typically done via TopCat software. When moving the crossmatching tasks to a Python + Astropy framework, I believe you will experience efficiency & time gains in your daily workflow. More functions will be included in future.

Current functions available:

* crossmatch_astrocat() : match your main cat with and external cat, extrac info from ext and add to your main.

* crossmatch_radius()   : have a bird's eye view on how your sky-crossmatch-radius inpact true vs. spurious matches  (still to push into astrocat)

* fits_to_parquet()     : convert .fits to .parquet and save disk space (up to 60% reduction in file size)

* csv_to_parquet()      : convert .csv  to .parquet and save disk space (up to 60% reduction in file size)


## How to Install 

Intall astrocat package: 

```
!install git+https://github.com/BrunoArsioli/astrocat.git
```

then, import crossmatch_catalog from astrocat.crossmatch library:

```
from astrocat import crossmatch
from astrocat import cross_panstarrs
```

## Functions

### --> crossmatch_astrocat() function:

This function will take two DataFrames (main and external), the column names for the R.A. and Dec. for each DataFrame, the list of column names to be added to the main DataFrame, and the maximum distance for a match between catalogs. It will add the new columns to the main df, fill in values for true matches (within max_distance), and return the updated main DataFrame.

Here we have a description of the crossmatch_astrocat() function and its input variables. 

```
crossmatch_astrocat(df_main, df_ext, ra_main, dec_main, ra_ext, dec_ext, col_list, max_distance)
```

The crossmatch_astrocat() is meant to crossmatches two astronomical catalogs.

This function finds matches between two catalogs of astronomical objects, given a maximum distance for a match.
For each object in the main catalog, the closest object in the external catalog within max_distance is identified.
If such a match is found, specified information from the external catalog is added to the main catalog.

#### crossmatch_astrocat() parameters:

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

#### Returns

* DataFrame
    The updated main catalog DataFrame, with new columns added from df_ext for matching objects.

#### Examples

Here is how to use this function:

  **i)** If you have CatWISE2020 as the external catalog and want to write W1 and W2 info to your main DataFrame

    col_list = ['W1mag', 'w1snr', 'W2mag', 'w2snr']
    df_main_updated = crossmatch_astrocat(df_main, df_ext, 'RA1', 'DEC1', 'RA2', 'DEC2', col_list, 2.0)


  **ii)** If you want to track the external_source from where the information is read, add a source_id or source_name to col_list:

    col_list = ['WISEname', 'W1mag', 'w1snr', 'W2mag', 'w2snr']
    df_main_updated = crossmatch_astrocat(df_main, df_ext, 'RA1', 'DEC1', 'RA2', 'DEC2', col_list, 2.0)

### --> cross_panstarrs() function: 

The cross_panstarrs function performs parallel cross-matching with a specified Pan-STARRS catalog using a specified radius. It utilizes ThreadPoolExecutor for efficient processing of HTTP requests in batches.

#### Example:

Python
import pandas as pd
from astrocat import cross_panstarrs

- Sample DataFrame with source positions
data = {'ra': [123.456, 20.0, 21.1, 22.2], 'dec': [78.901, 19.1, 20.2, 21.3]}
df = pd.DataFrame(data)

##### Perform cross-match with dr2/stack catalog and filter specific columns
result_df = cross_panstarrs(df, radius=0.001, relevant_columns=['_ra_', '_dec_', 'gPSFMag', 'rPSFMag'], catalog="dr2/stack")

print(result_df)

##### Perform cross-match with dr2/stack catalog and have all columns from Pan-STARRS
result_df = cross_panstarrs(df, radius=0.001, relevant_columns= None, catalog="dr2/stack")
print(result_df)

##### Perform cross-match with dr2/stack catalog and have all columns from Pan-STARRS
result_df = cross_panstarrs(df, radius=0.001, relevant_columns= "Default", catalog="dr2/stack")
print(result_df)


#### Parameters:

* !df (pandas.DataFrame): Input DataFrame containing source positions: R.A., Dec. (J2000), in degrees.
    * !The name of the columns must be 'ra' and 'dec' (i.e.: df['ra','dec'] ) 
* radius (float): Search radius in degrees for the cross-match.
* num_workers (int, optional): Number of worker processes for parallel HTTP requests execution.
    Defaults to 30. Recommendation: Do not go above 40, otherwise the PanSTARRS server can block your request.
* relevant_columns (list, optional): List of specific columns to retrieve from Pan-STARRS. If "Default",
    a default list of relevant columns is used. Defaults to "Default".

* batch size (int, optional): the number of sources that goes into each HTTP request (each worker) 
* catalog (str, optional): The Pan-STARRS catalog to query. Available options include:
    - "dr1/mean" (DR1 Mean)
    - "dr1/stack" (DR1 Stack)
    - "dr2/mean" (DR2 Mean)  (Default)
    - "dr2/stack" (DR2 Stack)
    - "dr2/detection" (DR2 Detection)
    - "dr2/forced_mean" (DR2 Forced Mean)
    - check for the latest available catalogs at: https://catalogs.mast.stsci.edu/docs/panstarrs.html 

#### Return Value:

A pandas DataFrame containing the cross-matched results with relevant information from Pan-STARRS.
Additional Notes:

This function uses ThreadPoolExecutor for parallel processing.
In case of errors, the function currently prints error messages to the console.
For further details on the Pan-STARRS catalogs and API, refer to the documentation: https://catalogs.mast.stsci.edu/docs/panstarrs.html




### --> crossmatch_radius() function:
(still to share)

This function will help visualise what is the best crossmatch radius to use when combining multi-mission archives. 

Also, it will be possible to estimate the level of contamination based on the trends in number-counts that are associated to real-associations and spurious-associations. 


### --> fits_to_parquet() function: 
This function converts .fits and .fit files to .parquet files using the astropy and pandas libraries. The resulting .parquet files are compressed and can be read faster than uncompressed .fits files.


Usage examples:
Call the fits_to_parquet function and pass in the path to the .fits file:

python
```
# import library
import astrocat
from astrocat.fits_to_parquet import fits_to_parquet
```

``` 
# convert a .fits file to a .parquet file
fits_to_parquet('path/to/fits/file.fits')
```

```
# convert multiple .fits files to .parquet files
fits_list = ['path/to/fits/file1.fits', 'path/to/fits/file2.fits', 'path/to/fits/file3.fits']
for fits_file in fits_list:
    fits_to_parquet(fits_file)
```

The resulting .parquet file will be saved in the same directory as the input .fits file.
If the resulting file_name.praquet already exist, a warning message will be shown.



### --> csv_to_parquet() function: 
This function converts .csv files to .parquet files using the astropy and pandas libraries. The resulting .parquet files are compressed and can be read faster than uncompressed .csv files.

Usage examples:
Call the csv_to_parquet function and pass in the path to the .csv file:

python
```
# import library
import astrocat
from astrocat.csv_to_parquet import csv_to_parquet
```

``` 
# convert a .csv file to a .parquet file
csv_to_parquet('path/to/csv/file.csv')
```

```
# convert multiple .csv files to .parquet files
csv_list = ['path/to/csv/file1.csv', 'path/to/csv/file2.csv', 'path/to/csv/file3.csv']
for csv_file in csv_list:
    csv_to_parquet(csv_file)
```

The resulting .parquet file will be saved in the same directory as the input .csv file.
If the resulting file_name.parquet already exist, a warning message will be shown.


## Contributing

Contributions are welcome. To contribute, please follow these steps:

1.Fork the repository.

2.Create a new branch.

3.Make your changes and commit them.

4.Push changes to GitHub.

5.Submit a pull request.



## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
