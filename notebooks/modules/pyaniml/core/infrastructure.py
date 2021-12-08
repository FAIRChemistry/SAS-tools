from dataclasses import dataclass
from pyaniml.utility.utils import SchemaBase, element
from pyaniml.core.sample import Sample
from pyaniml.core.sets import SampleReferenceSet


@dataclass
class Infrastructure(SchemaBase):
    """Container for sample references and infrastructure"""

    sample_references: SampleReferenceSet = element(
        name='SampleReferenceSet', default=SampleReferenceSet
    )

    def add_sample_reference(self, sample: Sample, role: str, sample_purpose: str):
        self.sample_references.add_reference(
            sample=sample, role=role, sample_purpose=sample_purpose
        )