import sdRDM

from typing import List, Optional
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Diffractogram(sdRDM.DataModel):

    """preprocessing steps"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("diffractogramINDEX"),
        xml="@id",
    )

    data_array: List[float] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )
