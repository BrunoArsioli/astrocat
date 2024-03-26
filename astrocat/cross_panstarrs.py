import requests
import io
from io import StringIO
import pandas as pd


def cross_panstarrs(df, radius, num_workers=30, relevant_columns="Default", batch_size=100, catalog="dr2/stack"):
    """
    Performs parallel cross-matching with a specified Pan-STARRS catalog using a specified radius.

    Args:
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

    Returns:
        pandas.DataFrame: The cross-matched DataFrame containing relevant information from Pan-STARRS.
    """

    # Build the PanSTARRS API URL for cross-match
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
        FILTER = False
    else: 
        # if the user provides a list, or uses "Default"
        FILTER = True
        # in case "Defaut" is given
        if relevant_columns is "Default": 
            relevant_columns = default_columns
        # in case the user provides a list, FILTER = True, 
        # and relevant_columns = [the  list provided by the user]

    # Function that will be run in parallel
    def get_data(idx):
        try:
            # reset file_obj for each iteration
            file_obj = StringIO()
            df.loc[idx].to_csv(file_obj, index=False)
            file_obj.seek(0)

            # Send the POST request with the input data and radius
            response = requests.post(url, params={'radius': radius}, files={'file': file_obj})

            # raise an error if the HTTP request returned an unsuccessful status code
            response.raise_for_status()

            # Convert response to dataframe
            data = StringIO(response.text)
            df_temp = pd.read_csv(data, sep=",")

            # filter relevant columns?
            if FILTER == True:
                df_batch = df_temp[relevant_columns].copy()
            if FILTER == False:
                df_batch = df_temp.copy() 

            return df_batch
        
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        finally:
            file_obj.close() # ensure that file_obj is closed even if an error occurs

    # Create iterator that provides indices for each batch of batch_size sources
    indices = np.array_split(df.index, np.ceil(len(df) / batch_size))

    # print main parameters before execution
    print(f"Your input sample has {df.shape[0]} sources.")
    print(f"The cross-match radius is set to {radius} degrees; i.e. {radius * 3600} arcsecons.")
    print(f"You submited {num_workers} HTTP requests to the server, in parallel.")

    with ThreadPoolExecutor(max_workers = num_workers) as executor:
        for dfps_batch in executor.map(get_data, indices):
            dfps = pd.concat([dfps, dfps_batch], ignore_index=True)

    # reset index 
    dfps.reset_index(drop=True, inplace=True)

    return dfps
