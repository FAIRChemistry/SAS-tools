"""Module for parsing AnIMLDocument objects for Series elements by their
seriesID attribute and create Pandas DataFrames from them.
"""

import pandas as pd

from enum import Enum
from pyaniml import AnIMLDocument, Series, IndividualValueSet
from typing import List, Any
from collections.abc import Iterable


class SeriesReader:
    """Read an AnIML document and create a `pandas.DataFrame` from any
    Series element within.
    """

    def __init__(self, animl_doc: AnIMLDocument):
        """Pass an AnIMLDocument object from which one or more Series
        elements should be read.
        Args:
            animl_doc (AnIMLDocument): AnIML document containing one or more Series to be read.
        """
        self._animl_doc = animl_doc
        self._available_seriesIDs = self._parse_available_seriesIDs()
        self._selected_seriesIDs = []
        
        print(self._available_seriesIDs)

    def __repr__(self):
        return "AnIML Series-element Reader"

    def _parse_available_seriesIDs(self) -> List[str]:
        """Parse AnIMLDocument object and return the seriesID attribute from every Series element within the document."""
        return [
            series.id.rstrip("__")
            for series in self.traverse_model_by_type(self._animl_doc, Series)
        ]

    def create_dataframe(self) -> pd.DataFrame:
        """Create `pandas.DataFrame` from `selected_seriesID` property
        and return it.

        Returns:
            pandas.DataFrame: DataFrame containing all Series elements selected by their seriesID attribute.
        """

        # Get all series that comply to the IDs
        selected_series = list(
            filter(
                lambda series: series.id.rstrip("__") in self.selected_seriesIDs,
                self.traverse_model_by_type(self._animl_doc, Series),
            )
        )

        return pd.DataFrame(
            {
                series.id: pd.Series(self._get_series_data(series).data)
                for series in selected_series
            }
        )

    def _get_series_data(self, series: Series) -> IndividualValueSet:
        """
        Due to xsData 3.7 != ^3.7 differences, data within IndividualValueSets
        are nested twice. This function extracts the values for both versions.
        """

        try:
            return next(
                filter(
                    lambda value_set: isinstance(value_set.data, list),
                    self.traverse_model_by_type(series, IndividualValueSet),
                )
            )
        except StopIteration:
            raise ValueError(f"Series '{series.id}' has no valid IndividualValueSet")

    def traverse_model_by_type(self, obj, target_type) -> List:
        """Traverses through an object and retrieves all sub-objects of the target_type"""

        results = []

        if isinstance(obj, target_type):
            # Grab the object if its of the searched type
            results += [obj]
        elif not hasattr(obj, "__dict__"):
            # Cannot harvest non-objects
            return []
        elif isinstance(obj, Enum):
            # No need to harvest Enums
            return []

        # Traverse the rest
        for attribute in obj.__dict__.values():
            if isinstance(attribute, Iterable):
                for subobj in attribute:
                    results += self.traverse_model_by_type(subobj, target_type)
                    continue

            results += self.traverse_model_by_type(attribute, target_type)

        return results

    @property
    def available_seriesIDs(self) -> List[str]:
        """Get SeriesID elements available in the AnIML document."""
        self._available_seriesIDs = self._parse_available_seriesIDs()
        return self._available_seriesIDs

    @property
    def selected_seriesIDs(self) -> List[str]:
        """Get list of seriesID selected so far."""
        return self._selected_seriesIDs

    @selected_seriesIDs.setter
    def selected_seriesIDs(self, list_of_ids: List[str]) -> None:
        for series_id in list_of_ids:
            self._selected_seriesIDs.append(series_id)
