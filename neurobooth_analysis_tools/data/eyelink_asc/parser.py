"""
Code for parsing EyeLink ASCII files generated by edf2asc.
"""

import pandas as pd
from neurobooth_analysis_tools.preprocess.gaze.href import calc_eye_velocity


NA_VALUES = ('...', '   .', '... ')


def parse_href(asc_file: str) -> pd.DataFrame:
    """
    Parses an EDF file with HREF coordinates generated by edf2asc -t -sh -s
    :return: A DataFrame with HREF eye coordinates
    """
    df = pd.read_csv(
        asc_file,
        sep='\t', na_values=NA_VALUES, header=None,
        usecols=(0, 1, 2, 4, 5),
        names=(  # See EyeLink Portable Duo manual pg. 91: "Binocular"
            'Time_EDF', 'L_GazeX_HREF', 'L_GazeY_HREF', 'R_GazeX_HREF', 'R_GazeY_HREF',
        ),
        dtype='float64',
    )
    return df


def parse_gaze(asc_file: str) -> pd.DataFrame:
    """
    Parses an EDF file with gaze coordinates and resolution generated by edf2asc -t -s -res
    :return: A DataFrame with eye coordinates (screen pixels) and resolution (pixels per degree)
    """
    df = pd.read_csv(
        asc_file,
        sep='\t', na_values=NA_VALUES, header=None,
        usecols=(0, 1, 2, 4, 5, 7, 8),
        names=(  # See EyeLink Portable Duo manual pg. 92: "Binocular, with resolution"
            'Time_EDF', 'L_GazeX', 'L_GazeY', 'R_GazeX', 'R_GazeY', 'ResolutionX', 'ResolutionY'
        ),
        dtype='float64',
    )
    return df


def href_velocity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute velocity from HREF position data. Assumes column headers produced by parse_href.
    :param df: A DataFrame with HREF eye coordinates
    :return: The same DataFrame, augmented with new velocity columns.
    """
    ts = df['Time_EDF'].to_numpy() / 1e3  # ms -> s

    x, y = df['L_GazeX_HREF'].to_numpy(), df['L_GazeY_HREF'].to_numpy()
    df['L_GazeX_HREF_Vel'], df['L_GazeY_HREF_Vel'] = calc_eye_velocity(x, y, ts)

    x, y = df['R_GazeX_HREF'].to_numpy(), df['R_GazeY_HREF'].to_numpy()
    df['R_GazeX_HREF_Vel'], df['R_GazeY_HREF_Vel'] = calc_eye_velocity(x, y, ts)

    return df


