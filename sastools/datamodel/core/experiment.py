import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .diffractiontype import DiffractionType
from .instrument import Instrument
from .diffractogram import Diffractogram
from .sasunit import SASUnit
from .measurement import Measurement
from .measurementtype import MeasurementType
from .analysis import Analysis


@forge_signature
class Experiment(sdRDM.DataModel):

    """Container for SAS measurements and analyses."""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    name: str = Field(
        ...,
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

    analyses: List[Analysis] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    def add_to_measurements(
        self,
        instrument: Instrument,
        diffractogram: Diffractogram,
        measurement_type: List[MeasurementType] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            instrument (): tba.
            diffractogram (): tba.
            measurement_type (): tba. Defaults to ListPlus()
        """

        params = {
            "instrument": instrument,
            "diffractogram": diffractogram,
            "measurement_type": measurement_type,
        }

        if id is not None:
            params["id"] = id

        self.measurements.append(Measurement(**params))

        return self.measurements[-1]

    def add_to_analyses(
        self,
        name: str,
        method_description: Optional[str] = None,
        input_data_id: List[str] = ListPlus(),
        result: List[Union[str, int, float, bool]] = ListPlus(),
        unit: Optional[SASUnit] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Analysis' to attribute analyses

        Args:
            id (str): Unique identifier of the 'Analysis' object. Defaults to 'None'.
            name (): tba.
            method_description (): tba. Defaults to None
            input_data_id (): tba. Defaults to ListPlus()
            result (): tba. Defaults to ListPlus()
            unit (): tba. Defaults to None
        """

        params = {
            "name": name,
            "method_description": method_description,
            "input_data_id": input_data_id,
            "result": result,
            "unit": unit,
        }

        if id is not None:
            params["id"] = id

        self.analyses.append(Analysis(**params))

        return self.analyses[-1]
