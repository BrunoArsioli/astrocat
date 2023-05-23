# Testing for Astrocat

This directory contains tests for the Astrocat project.

## Running the tests

To run the tests, navigate to the root directory of the project and run the command:

``` 
pytest
``` 

## Test files

### test_crossmatch.py

This file contains tests for the `crossmatch_astrocats` function in the `crossmatch.py` module. 

The tests use mock data to ensure the function correctly crossmatches two astronomical catalogs and updates the main catalog with data from the external catalog as expected.
