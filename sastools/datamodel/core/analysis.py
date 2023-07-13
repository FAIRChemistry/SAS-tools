import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .sasunit import SASUnit


@forge_signature
class Analysis(sdRDM.DataModel):

    """tba"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("analysisINDEX"),
        xml="@id",
    )

    name: str = Field(
        ...,
        description="tba",
    )

    method_description: Optional[str] = Field(
        default=None,
        description="tba",
    )

    input_data_id: List[str] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    result: List[Union[str, int, float, bool]] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    unit: Optional[SASUnit] = Field(
        default=None,
        description="tba",
    )
