import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime as Datetime

from .experiment import Experiment
from .citation import Citation


@forge_signature
class SAStools(sdRDM.DataModel):

    """Root element of the SAS-tools data model."""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("sastoolsINDEX"),
        xml="@id",
    )

    datetime_created: Datetime = Field(
        ...,
        description="Date and time this dataset has been created.",
    )

    datetime_modified: Optional[Datetime] = Field(
        default=None,
        description="Date and time this dataset has last been modified.",
    )

    experiment: Optional[Experiment] = Field(
        default=None,
        description="A SAS experiment with measurements and analyses.",
    )

    citation: Optional[Citation] = Field(
        default=None,
        description=(
            "Relevant information regarding the publication and citation of this"
            " dataset."
        ),
    )
