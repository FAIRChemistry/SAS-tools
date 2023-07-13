import sdRDM

from typing import List, Optional
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .sasunit import SASUnit


@forge_signature
class Diffractogram(sdRDM.DataModel):

    """preprocessing steps"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("diffractogramINDEX"),
        xml="@id",
    )

    scattering_vector_array: List[float] = Field(
        multiple=True,
        description="tba",
        default_factory=ListPlus,
    )

    counts_per_area_array: List[float] = Field(
        multiple=True,
        description="tba",
        default_factory=ListPlus,
    )

    scattering_vector_unit: Optional[SASUnit] = Field(
        default=None,
        description="tba",
    )

    counts_per_area_unit: Optional[SASUnit] = Field(
        default=None,
        description="tba",
    )
