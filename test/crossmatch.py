# intall astrocat package
!pip install git+https://github.com/BrunoArsioli/astrocat.git
  
# in tests/test_crossmatch.py
import pandas as pd
import numpy as np
import astrocat 
from pandas.testing import assert_frame_equal


def test_crossmatch_astrocats():
    df_main = pd.DataFrame({'RA': [1, 2, 3, 5], 'DEC': [1, 2, 3, 5]})
    df_ext = pd.DataFrame({'RA': [1, 2, 3, 4], 'DEC': [1, 2, 3, 4], 'DATA': ['a', 'b', 'c', 'd']})

    result = crossmatch_astrocat(df_main, df_ext, 'RA', 'DEC', 'RA', 'DEC', ['DATA'], 1)
    
    print("df_main after the crossmatch:")
    display(result)

    expected_result = pd.DataFrame({'RA':[1, 2, 3, 5], 'DEC':[1, 2, 3, 5], 'DATA':['a', 'b', 'c', np.nan]}) 

    print("The expected df_main after the crossmatch:")
    display(expected_result)

    # use the function assert_frame_equal() that correctly handles comparisons with np.nan values. 
    assert_frame_equal(result, expected_result)

    print("All tests passed!")


test_crossmatch_astrocats()
