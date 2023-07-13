import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .instrumentsetting import InstrumentSetting


@forge_signature
class Instrument(sdRDM.DataModel):

    """tba"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("instrumentINDEX"),
        xml="@id",
    )

    name: str = Field(
        ...,
        description="tba",
    )

    manufacturer: str = Field(
        ...,
        description="tba",
    )

    serial_number: Optional[str] = Field(
        default=None,
        description="tba",
    )

    firmware_version: Optional[str] = Field(
        default=None,
        description="tba",
    )

    instrument_settings: List[InstrumentSetting] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="tba",
    )

    def add_to_instrument_settings(
        self,
        setting_name: str,
        value: Union[str, int, float, bool],
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'InstrumentSetting' to attribute instrument_settings

        Args:
            id (str): Unique identifier of the 'InstrumentSetting' object. Defaults to 'None'.
            setting_name (): tba.
            value (): tba.
        """

        params = {
            "setting_name": setting_name,
            "value": value,
        }

        if id is not None:
            params["id"] = id

        self.instrument_settings.append(InstrumentSetting(**params))

        return self.instrument_settings[-1]
