"""Different space groups and their properties needed for analyzers."""

import numpy as np

from typing import List, Tuple, Dict

from sastools.analyzer.enums import LLCPhases, LLCSpaceGroups, LLCMillerIndices
from sastools.analyzer.llcphase import LLCPhase


class HexagonalPhase(LLCPhase):
    """Container for properties of hexagonal LLC phases."""

    def __init__(self) -> None:
        self._exact_phase = None
        self._space_group = LLCSpaceGroups.P6MM
        self._miller_indices = ()
        self._lattice_parameters = []
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Hexagonal LLC Phase"

    def _calculate_a_H1(self, d: float, h: int, k: int) -> float:
        # Calculate and return the lattice parameter for a given lattice
        # plane distance d, miller index h, and miller index k.
        a_H1 = d * np.sqrt((4 / 3) * ((h**2 + k**2 + (h * k))))
        return a_H1

    def calculate_lattice_parameters(
        self, d_meas: List[float], phase: LLCPhases = LLCPhases.H1
    ) -> None:
        """Calculate lattice parameters of hexagonal phase using a list
        of measured lattice plane distances `d_meas`.

        Args:
            d_meas (List[float]): Measured lattice plane distances.
            phase (LLCPhases, optional): The hexagonal phase of the system. Defaults to LLCPhases.H1.

        Raises:
            NotImplementedError: If phase provided is not yet implemented.
        """
        if not phase == LLCPhases.H1:
            raise NotImplementedError(
                f"Chosen LLC phase '{phase}' is not (yet) supported."
            )
        self._exact_phase = phase
        for i, _ in enumerate(d_meas):
            a_i = self._calculate_a_H1(
                d_meas[i], self.miller_indices[0][i], self.miller_indices[1][i]
            )
            self.lattice_parameters.append(a_i)

    @property
    def exact_phase(self) -> LLCPhases:
        """Get hexagonal phase."""
        return self._exact_phase

    @exact_phase.setter
    def exact_phase(self, phase: LLCPhases) -> None:
        self._exact_phase = phase

    @property
    def space_group(self) -> LLCSpaceGroups:
        """Get space group of hexagonal phase."""
        return self._space_group

    @property
    def miller_indices(self) -> Tuple[List[int], List[int], List[int]]:
        """Get miller indices of hexagonal phase."""
        self._miller_indices = LLCMillerIndices[self._space_group.name].value
        return self._miller_indices

    @property
    def lattice_parameters(self) -> List[float]:
        """Get lattice parameters of hexagonal phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> Dict:
        """Get full phase information of hexagonal phase."""
        self._phase_information = dict(
            phase=self.exact_phase.value,
            lattice_parameter=np.mean(self.lattice_parameters),
        )
        return self._phase_information


class CubicPhase(LLCPhase):
    """Container for properties of cubic LLC phases."""

    def __init__(self) -> None:
        self._exact_phase = None
        self._space_group = None
        self._miller_indices = ()
        self._lattice_parameters = []
        self._phase_information = {}
        self._d_reciprocal = []
        self._sqrt_miller = []

    def __repr__(self) -> str:
        return f"Cubic LLC Phase"

    def _calculate_a_V1(self, d: float, h: int, k: int, l: int) -> float:
        # Calculate and return the lattice parameter for a given lattice
        # plane distance d, miller index h, k, and l.
        a_V1 = d * (np.sqrt((h**2) + (k**2) + (l**2)))
        return a_V1

    def calculate_lattice_parameters(
        self,
        d_meas: List[float],
        phase: LLCPhases = LLCPhases.V1,
        space_group: LLCSpaceGroups = LLCSpaceGroups.IA3D,
    ) -> None:
        """Calculate lattice parameters of cubic phase using a list of
        measured lattice plane distances `d_meas`.

        Args:
            d_meas (List[float]): Measured lattice plane distances.
            phase (LLCPhases, optional): The cubic phase of the system. Defaults to LLCPhases.V1.
            space_group (LLCSpaceGroups, optional): The space group corresponding to the cubic phase. Defaults to LLCSpaceGroups.IA3D.

        Raises:
            NotImplementedError: If phase provided is not yet implemented.
        """
        if not phase == LLCPhases.V1:
            raise NotImplementedError(
                f"Chosen LLC phase '{phase}' is not (yet) supported."
            )
        self._exact_phase = phase
        self._space_group = space_group
        for i, j in enumerate(d_meas):
            a_i = self._calculate_a_V1(
                d_meas[i],
                self.miller_indices[0][i],
                self.miller_indices[1][i],
                self.miller_indices[2][i],
            )
            self._lattice_parameters.append(a_i)

    def calculate_d_reciprocal(self, peak_center: List[float]) -> None:
        """Calculate the reciprocal lattice plane distances
        `d_reciprocal` from the `peak_centers` determined through
        lorentzian fitting.

        Args:
            peak_center (List[float]): Peak centers determined by lorentzian fitting for the cubic phase.
        """
        self._d_reciprocal = [peak / (2 * np.pi) for peak in peak_center]

    def calculate_sqrt_miller(self) -> None:
        """Calculate the square roots `sq_root` of the `miller_indices`
        corresponding to the peaks of the cubic phase.
        """

        self._sqrt_miller = [
            np.sqrt(
                self.miller_indices[0][i] ** 2
                + self.miller_indices[1][i] ** 2
                + self.miller_indices[2][i] ** 2
            )
            for i in range(len(self.d_reciprocal))
        ]

    @property
    def exact_phase(self) -> LLCPhases:
        """Get cubic phase."""
        return self._exact_phase

    @exact_phase.setter
    def exact_phase(self, phase: LLCPhases) -> None:
        self._exact_phase = phase

    @property
    def space_group(self) -> LLCSpaceGroups:
        """Get space group of cubic phase."""
        return self._space_group

    @space_group.setter
    def space_group(self, space_group: LLCSpaceGroups) -> None:
        self._space_group = space_group

    @property
    def miller_indices(self) -> Tuple[List[int], List[int], List[int]]:
        """Get miller indices of cubic phase."""
        if self.space_group is None:
            raise ValueError("space_group property has to be provided first.")
        self._miller_indices = LLCMillerIndices[self._space_group.name].value
        return self._miller_indices

    @property
    def lattice_parameters(self) -> List[float]:
        """Get lattice parameters of cubic phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> Dict:
        """Get full phase information of cubic phase."""
        self._phase_information = dict(
            phase=self.exact_phase.value,
            lattice_parameter=np.mean(self.lattice_parameters),
        )
        return self._phase_information

    @property
    def d_reciprocal(self) -> List[float]:
        """Get reciprocal lattice plane distances of cubic phase."""
        return self._d_reciprocal

    @property
    def sqrt_miller(self) -> List[int]:
        """Get square roots of miller indices of cubic phase."""
        return self._sqrt_miller


class LamellarPhase(LLCPhase):
    """Container for properties of lamellar LLC phases."""

    def __init__(self) -> None:
        self._exact_phase = None
        self._space_group = None
        self._miller_indices = None
        self._lattice_parameters = []
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Lamellar LLC Phase"

    def calculate_lattice_parameters(
        self, d_meas: List[float], phase: LLCPhases = LLCPhases.LA
    ) -> None:
        """Calculate lattice parameters of lamellar phase using a list
        of measured lattice plane distances `d_meas`.

        Args:
            d_meas (List[float]): Measured lattice plane distances.
            phase (LLCPhases, optional): The lamellar phase of the system. Defaults to LLCPhases.LA.

        Raises:
            NotImplementedError: If phase provided is not yet implemented.
        """
        if not phase == LLCPhases.LA:
            raise NotImplementedError(
                f"Chosen LLC phase '{phase}' is not (yet) supported."
            )
        self._exact_phase = phase
        self._lattice_parameters.append(d_meas[0])

    @property
    def exact_phase(self) -> LLCPhases:
        """Get lamellar phase."""
        return self._exact_phase

    @exact_phase.setter
    def exact_phase(self, phase: LLCPhases) -> None:
        self._exact_phase = phase

    @property
    def space_group(self) -> None:
        """Get space group of lamellar phase."""
        return self._space_group

    @property
    def miller_indices(self) -> None:
        """Get miller indices of lamellar phase."""
        return self._miller_indices

    @property
    def lattice_parameters(self) -> List[float]:
        """Get lattice parameters of lamellar phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> Dict:
        """Get full phase information of lamellar phase."""
        self._phase_information = dict(
            phase=self.exact_phase.value,
            lattice_parameter=self.lattice_parameters[0],
        )
        return self._phase_information


class IndeterminatePhase(LLCPhase):
    """Container for properties of indeterminate LLC phases."""

    def __init__(self) -> None:
        self._exact_phase = LLCPhases.INDETERMINATE
        self._space_group = None
        self._miller_indices = None
        self._lattice_parameters = None
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Indeterminate LLC Phase"

    def calculate_lattice_parameters(
        self, d_meas: List[float], phase: LLCPhases = LLCPhases.INDETERMINATE
    ) -> None:
        """Do not use this method! Indeterminate phases have no lattice
        parameters.

        Args:
            d_meas (List[float]): Measured lattice plane distances.
            phase (LLCPhases, optional): Indeterminate phase. Defaults to LLCPhases.INDETERMINATE.

        Raises:
            NotImplementedError: If this method is called.
        """
        raise NotImplementedError(
            f"No lattice parameter in indeterminate phases!"
        )

    @property
    def exact_phase(self) -> LLCPhases:
        """Get indeterminate phase."""
        return self._exact_phase

    @property
    def space_group(self) -> None:
        """Get space group of indeterminate phase."""
        return self._space_group

    @property
    def miller_indices(self) -> None:
        """Get miller indices of indeterminate phase."""
        return self._miller_indices

    @property
    def lattice_parameters(self) -> None:
        """Get lattice parameters of indeterminate phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> Dict:
        """Get full phase information of indeterminate phase."""
        self._phase_information = dict(
            phase=self.exact_phase.value,
            lattice_parameter="-",
        )
        return self._phase_information
