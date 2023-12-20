"""
Code for parsing EyeLink ASCII files generated by edf2asc.
"""

import pandas as pd


def parse_href(asc_file: str) -> pd.DataFrame:
    """
    Parses an HREF file with resolution generated by edf2asc -t -sh -s
    :return: A DataFrame HREF eye coordinates
    """
    df = pd.read_csv(
        asc_file,
        sep='\t', na_values=['...', '   .'], header=None,
        usecols=(0, 1, 2, 4, 5),
        names=(  # See EyeLink Portable Duo manual pg. 92: "Binocular, with resolution"
            'Time_EDF', 'L_GazeX_HREF', 'L_GazeY_HREF', 'R_GazeX_HREF', 'R_GazeY_HREF',
        ),
        dtype='float64',
    )
    df['Time_EDF'] /= 1e3  # ms -> s
    return df


