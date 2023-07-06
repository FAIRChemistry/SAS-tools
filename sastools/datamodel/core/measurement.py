import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


from .measurementtype import MeasurementType


@forge_signature
class Measurement(sdRDM.DataModel):

    """instrument (settings, parameters, ...)"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("measurementINDEX"),
        xml="@id",
    )

    measurement_type: Optional[MeasurementType] = Field(
        default=None,
        description="tba",
    )
