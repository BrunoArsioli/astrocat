import requests
import io
from io import StringIO
import pandas as pd


def cross_panstarrs(df, radius, num_workers=30, relevant_columns=None, catalog="dr2/stack"):
    """
    Performs parallel cross-matching with a specified Pan-STARRS catalog using a specified radius.

    Args:
        * df (pandas.DataFrame): Input DataFrame containing source positions: RA, Dec (J2000), in degrees.
        * radius (float): Search radius in degrees for the cross-match.
        * num_workers (int, optional): Number of worker processes for parallel HTTP requests execution.
            Defaults to 30. Recommendation: Do not go above 40, otherwise the PanSTARRS server can block your request.
        * relevant_columns (list, optional): List of specific columns to retrieve from Pan-STARRS. If None,
            a default list of relevant columns is used. Defaults to None.
        * catalog (str, optional): The Pan-STARRS catalog to query. Available options include:
            - "dr1/mean" (DR1 Mean)
            - "dr1/stack" (DR1 Stack)
            - "dr2/mean" (DR2 Mean)  (Default)
            - "dr2/stack" (DR2 Stack)
            - "dr2/detection" (DR2 Detection)
            - "dr2/forced_mean" (DR2 Forced Mean)
            - check for the latest available catalogs at: https://catalogs.mast.stsci.edu/docs/panstarrs.html 

    Returns:
        pandas.DataFrame: The cross-matched DataFrame containing relevant information from Pan-STARRS.
    """

    base_url = 'https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/'
    url = f"{base_url}{catalog}/crossmatch/upload.csv"

    # Reference for available catalogs: https://catalogs.mast.stsci.edu/docs/panstarrs.html
    default_columns = [
        '_ra_', '_dec_', 'qualityFlag', 'nDetections', 'MatchRA', 'MatchDEC',
        'dstArcSec', 'objName', 'primaryDetection',
        'gPSFMag', 'gApMag', 'rPSFMag', 'rApMag', 'iPSFMag', 'iApMag',
        'zPSFMag', 'zApMag', 'yPSFMag', 'yApMag'
    ]

    # Use default columns if none provided
    if relevant_columns is None:
        relevant_columns = default_columns

    def get_data(idx):
        try:
            file_obj = StringIO()
            df.loc[idx].to_csv(file_obj, index=False)
            file_obj.seek(0)

            response = requests.post(url, params={'radius': radius}, files={'file': file_obj})
            response.raise_for_status()

            data = StringIO(response.text)
            df_temp = pd.read_csv(data, sep=",")
            return df_temp[relevant_columns].copy()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        finally:
            file_obj.close()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        dfps = pd.concat(executor.map(get_data, df.index.to_numpy().reshape(-1, 100)), ignore_index=True)

    return dfps
