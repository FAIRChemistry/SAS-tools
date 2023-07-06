import sdRDM

from typing import List, Optional
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .measurement import Measurement
from .measurementtype import MeasurementType
from .diffractiontype import DiffractionType
from .analysis import Analysis
from .diffractogram import Diffractogram


@forge_signature
class Experiment(sdRDM.DataModel):

    """Container for SAS measurements and analyses."""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    name: Optional[str] = Field(
        default=None,
        description="tba",
    )

    diffraction_type: Optional[DiffractionType] = Field(
        default=None,
        description="tba",
    )

    measurements: List[Measurement] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    diffractograms: List[Diffractogram] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    analyses: List[Analysis] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    def add_to_measurements(
        self,
        measurement_type: Optional[MeasurementType] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            measurement_type (): tba. Defaults to None
        """

        params = {
            "measurement_type": measurement_type,
        }

        if id is not None:
            params["id"] = id

        self.measurements.append(Measurement(**params))

        return self.measurements[-1]

    def add_to_diffractograms(
        self, data_array: List[float] = ListPlus(), id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Diffractogram' to attribute diffractograms

        Args:
            id (str): Unique identifier of the 'Diffractogram' object. Defaults to 'None'.
            data_array (): tba. Defaults to ListPlus()
        """

        params = {
            "data_array": data_array,
        }

        if id is not None:
            params["id"] = id

        self.diffractograms.append(Diffractogram(**params))

        return self.diffractograms[-1]

    def add_to_analyses(
        self, name: Optional[str] = None, id: Optional[str] = None
    ) -> None:
        """
        This method adds an object of type 'Analysis' to attribute analyses

        Args:
            id (str): Unique identifier of the 'Analysis' object. Defaults to 'None'.
            name (): tba. Defaults to None
        """

        params = {
            "name": name,
        }

        if id is not None:
            params["id"] = id

        self.analyses.append(Analysis(**params))

        return self.analyses[-1]
