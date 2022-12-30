"""Reader for Origin TXT output files containing Lorentzian data."""

import os
import pandas as pd

from pathlib import Path
from typing import Union



class OriginReader:
    """Read Lorentzian data from Origin TXT file."""

    def __init__(self, file: Union[str, bytes, os.PathLike]) -> None:
        """Pass path to TXT file with Origin output.

        Args:
            file (str | bytes | os.PathLike): TXT file containing Lorentzian data created with Origin.
        """
        self._file = Path(file)
        with self._file.open("r") as txt:
            self._dataframe = pd.read_table(
                filepath_or_buffer=txt,
                header=0,
                names=[
                    "quantity",
                    "symbol",
                    "value",
                    "stddev",
                    "t-value",
                    "probabililty",
                    "dependency",
                ],
                engine="python",
            )
        self._xc_values = self._dataframe.loc[
            self._dataframe["symbol"] == "xc"
        ]

    def __repr__(self):
        return "Origin Reader"

    @property
    def full_dataframe(self) -> pd.DataFrame:
        """Get full Pandas DataFrame."""
        return self._dataframe

    @property
    def xc_dataframe(self) -> pd.DataFrame:
        """Get only 'xc' values of Pandas DataFrame."""
        return self._xc_values
