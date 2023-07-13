import sdRDM

from typing import List, Optional
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .instrument import Instrument
from .diffractogram import Diffractogram
from .measurementtype import MeasurementType


@forge_signature
class Measurement(sdRDM.DataModel):

    """tba"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("measurementINDEX"),
        xml="@id",
    )

    measurement_type: List[MeasurementType] = Field(
        multiple=True,
        description="tba",
        default_factory=ListPlus,
    )

    instrument: Instrument = Field(
        ...,
        description="tba",
    )

    diffractogram: Diffractogram = Field(
        ...,
        description="tba",
    )
