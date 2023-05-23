# astrocat

This function will take two DataFrames (main and external), the column names for the R.A. and Dec. for each DataFrame, the list of column names to be added to the main DataFrame, and the maximum distance for a match between catalogs. It will add the new columns to the main df, fill in values for true matches (within max_distance), and return the updated main DataFrame.

