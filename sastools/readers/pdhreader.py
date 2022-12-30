"""Module for reading PDH files and separating data and metadata."""


import os
import re
import tempfile
import pandas as pd

from lxml import etree
from typing import Union, List, Dict
from pathlib import Path


class PDHReader:
    """Separate data block and XML metadata footer of PDH files."""

    def __init__(self, path_to_directory: Union[str, bytes, os.PathLike]):
        """Pass the path to a directory containing PDH-type files to be
        read.

        Args:
            path_to_directory (str | bytes | os.PathLike): Path to a directory containing PDH-type files.
        """
        path = list(Path(path_to_directory).glob("*.pdh"))
        self._available_files = {file.stem: file for file in path if file.is_file()}

    def __repr__(self):
        return "PDH Reader"

    def _line_is_xml(self, line_in_file):
        # Match n whitespaces, followed by an XML opening tag `<`.
        any_whitespace = re.compile(r"\s*<").match(line_in_file)
        return any_whitespace

    def enumerate_available_files(self) -> Dict[int, str]:
        """Enumerate the PDH files available in the given directory and
        return a dictionary with their index and name.

        Returns:
            Dict[int, str]: Indices and names of available files.
        """
        return {count: value for count, value in enumerate(self.available_files)}

    def extract_data(self, filestem: str) -> pd.DataFrame:
        """Extract only data block as a `pandas.DataFrame`.

        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.

        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        dataframe = pd.read_table(
            self._available_files[filestem],
            delimiter="   ",
            usecols=[0, 1],
            names=["scattering_vector", "counts_per_area"],
            header=5,
            skipfooter=496,
            engine="python",
        )
        return dataframe

    def extract_metadata(self, filestem: str) -> etree._ElementTree:
        """Extract XML metadata footer as an `etree.ElementTree`.

        Args:
            filestem (str): Name of the file (only stem) of which the metadata is to be extracted.

        Returns:
            etree.ElementTree: ElementTree containing only the metadata from the file.
        """
        with tempfile.NamedTemporaryFile(mode="r+") as tmp:
            with self._available_files[filestem].open("r") as f:
                for line in f:
                    if self._line_is_xml(line) is not None:
                        tmp.write(line)
            tmp.seek(0)
            XML_tree = etree.parse(tmp)
        return XML_tree

    @property
    def available_files(self) -> List[str]:
        """Get file available in directory."""
        return self._available_files
