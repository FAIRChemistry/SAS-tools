"""ABC defining properties of different LLC phases."""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from sastools.analyzer.enums import LLCPhases, LLCSpaceGroups


class LLCPhase(ABC):
    """ABC defining the properties of an LLC Phase."""

    @abstractmethod
    def calculate_lattice_parameters(self, d_meas: List[float]):
        ...

    @property
    @abstractmethod
    def exact_phase(self) -> LLCPhases:
        ...

    @property
    @abstractmethod
    def space_group(self) -> LLCSpaceGroups:
        ...

    @property
    @abstractmethod
    def miller_indices(self) -> Tuple[List[int], List[int], List[int]]:
        ...

    @property
    @abstractmethod
    def lattice_parameters(self) -> List[float]:
        ...

    @property
    @abstractmethod
    def phase_information(self) -> Dict:
        ...
