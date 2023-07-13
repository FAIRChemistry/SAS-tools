import sdRDM

from typing import Optional, Union
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class InstrumentSetting(sdRDM.DataModel):

    """tba"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("instrumentsettingINDEX"),
        xml="@id",
    )

    setting_name: str = Field(
        ...,
        description="tba",
    )

    value: Union[str, int, float, bool] = Field(
        ...,
        description="tba",
    )
