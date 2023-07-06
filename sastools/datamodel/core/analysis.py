import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Analysis(sdRDM.DataModel):

    """tba"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("analysisINDEX"),
        xml="@id",
    )

    name: Optional[str] = Field(
        default=None,
        description="tba",
    )
