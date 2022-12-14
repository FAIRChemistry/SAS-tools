"""Implementation of SAXS Analyzer interface."""

import numpy as np

from enums import SAXSStandards
from llcphase import LLCPhase
from llcphases import (
    CubicPhase,
    HexagonalPhase,
    IndeterminatePhase,
    LamellarPhase,
)


class PrepareStandard:
    """Contains methods for preparing the calibration of measured data
    using a standard.
    """

    def __init__(
        self, standard: SAXSStandards = None, q_std_lit: list[float] = None
    ) -> None:
        """Select standard for calibration of SAXS data from
        `SAXSStandards` enum. If no standard is given, `q_std_lit`
        values have to be provided directly or calculated from
        `d_std_lit` manually using `calculate_scattering_vector()`.

        Args:
            standard (SAXSStandards, optional): Common SAXS standard used in experiment. Defaults to None.
            q_std_lit (list[float], optional): Literature values for scattering vector of standard used in experiment. Defaults to None.

        Raises:
            ValueError: If both standard and q_std_lit are provided.
            NotImplementedError: If not yet implemented SAXS standard is passed.
        """
        self._standard = standard
        self._q_std_lit = q_std_lit

        if self._standard and self._q_std_lit:
            raise ValueError(
                f"Both a standard = '{self.standard.name}' and a custom q_std_lit = '{self.q_std_lit}' were given. These arguments are mutually exclusive, please choose only one!"
            )
        elif self._standard == SAXSStandards.CHOLESTERYL_PALMITATE:
            self.calculate_scattering_vector()
        elif self._standard is None and self._q_std_lit:
            pass
        elif self._standard is None and self._q_std_lit is None:
            pass
        else:
            raise NotImplementedError(
                f"SAXS Standard {standard.name} is not yet implemented."
            )

    def calculate_scattering_vector(
        self, d_std_lit: list[float] = None
    ) -> list[float]:
        """Calculate scattering vector `q_std_lit` (nm^-1) for
        calibration from literature lattice plane distance `d_std_lit`
        (nm).

        Args:
            d_std_lit (list[float], optional): Lattice plane distance from literature. Defaults to None.

        Raises:
            ValueError: If d_std_lit is not given and neither a standard nor q_std_lit have been initialized.
            ValueError: If d_std_lit list is empty.

        Returns:
            list[float]: Scattering vector q_std_lit.
        """
        if self._q_std_lit:
            print(
                f"INFO: q_std_lit = {self._q_std_lit} has already been provided or calculated. Passing method call."
            )
            return self._q_std_lit
        elif self._standard == SAXSStandards.CHOLESTERYL_PALMITATE:
            d_std_lit = [5.249824535, 2.624912267, 1.749941512]
            # Reference: D. L. Dorset, Journal of Lipid Research 1987,
            # 28, 993-1005.
        else:
            if d_std_lit is None:
                raise ValueError(
                    "d_std_lit has to be given, as neither a SAXS standard nor q_std_lit have been initialized!"
                )
            elif len(d_std_lit) < 1:
                raise ValueError(
                    f"d_std_lit = {d_std_lit} cannot be an empty list!"
                )

        self._q_std_lit = [(2 * np.pi) / d for d in d_std_lit]
        return self._q_std_lit

    def calculate_linear_regression(
        self, q_std_meas: list[float]
    ) -> tuple[float, float]:
        """Calculate the linear regression from `q_std_meas` against
        `q_std_lit` using `numpy.polyfit()` and return `slope` and
        `intercept` as a tuple.

        Args:
            q_std_meas (list): List of measured q values for standard.

        Returns:
            tuple: Tuple of slope and intercept from linear regression.
        """
        slope, intercept = np.polyfit(x=q_std_meas, y=self._q_std_lit, deg=1)
        return (slope, intercept)

    @property
    def standard(self) -> SAXSStandards:
        """Get standard used for this preparation."""
        return self._standard

    @property
    def q_std_lit(self) -> list[float]:
        """Get lscattering vectors of standard from literature used."""
        return self._q_std_lit


class LLCAnalyzer:
    """Contains methods for analyzing SAXS data of LLC phases."""

    def __init__(self) -> None:
        self._q_corr = []
        self._d = []
        self._d_ratio = []

    def _calculate_lattice_plane_distances(self) -> None:
        # Calculate and return the lattice planes `d` from list of
        # calibrated scattering vectors `q_corr`.
        self._d = [(2 * np.pi) / q for q in self.q_corr]

    def _calculate_lattice_ratio(self) -> None:
        # Calculate and return the lattice plane ratios `d_ratio` from
        # list of lattice planes `d`.
        self._d_ratio = [d / self.d[0] for d in self.d[1:]]

    def calibrate_data(
        self, slope: float, q_meas: list[float], intercept: float
    ) -> None:
        """Calibrate list of measured scattering vectors `q_meas` with
        `(slope, intercept)` tuple from `calculate_linear_regression()`
        method of `PrepareStandard` class and return list of calibrated
        scattering vectors `q_corr`.

        Args:
            slope (float): Slope of calculated linear regression from measured standard against literature values.
            q_meas (list[float]): List of scattering vectors from raw measured data.
            intercept (float): Intercept of calculated linear regression from measured standard against literature values.
        """
        self._q_corr = [slope * q + intercept for q in q_meas]
        self._calculate_lattice_plane_distances()
        self._calculate_lattice_ratio()

    def determine_phase(self) -> LLCPhase:
        """Determine the LLC phase of the sample from `d_ratios` and
        return the appropriate `LLCPhase` object.

        Returns:
            LLCPhase: Class holding relevant phase information of corresponding LLC phase.
        """
        H1 = [
            (1 / np.sqrt(3)),
            (1 / np.sqrt(4)),
            (1 / np.sqrt(7)),
            (1 / np.sqrt(9)),
        ]
        V1 = [
            (1 / np.sqrt(2)),
            (1 / np.sqrt(3)),
            (1 / np.sqrt(4)),
            (1 / np.sqrt(5)),
        ]
        La = [(1 / 2), (1 / 3), (1 / 4), (1 / 5)]

        for i, _ in enumerate(self.d_ratio):
            if (abs(self.d_ratio[i] - H1[i])) < 0.03:
                return HexagonalPhase
            elif (abs(self.d_ratio[i] - V1[i])) < 0.03:
                return CubicPhase
            elif (abs(self.d_ratio[i] - La[i])) < 0.03:
                return LamellarPhase
            else:
                return IndeterminatePhase

    def calculate_d_reciprocal(
        self, cubic_phase: CubicPhase, peak_center: list[float]
    ) -> list[float]:
        """Calculate the reciprocal lattice plane distances
        `d_reciprocal` from the `peak_centers` determined through
        lorentzian fitting and both set the corresponding property of
        the `cubic_phase` provided, and also return the list of
        `d_reciprocal` directly.

        Args:
            cubic_phase (CubicPhase): Cubic phase of which d_reciprocal should be calculated.
            peak_center (list[float]): Peak centers determined by lorentzian fitting for the cubic phase.

        Returns:
            list[float]: List of reciprocal lattice plane distances of cubic phase.
        """
        d_reciprocal = [i / (2 * np.pi) for i in peak_center]
        cubic_phase.d_reciprocal = d_reciprocal
        return d_reciprocal

    def calculate_sqrt_miller(
        self,
        cubic_phase: CubicPhase,
        miller_indices: tuple[list[int], list[int], list[int]],
    ) -> list[int]:
        """Calculate the square roots `sq_root` of the `miller_indices`
        passed to this method and both set the corresponding property of
        the `cubic_phase` provided, and also return the list of
        `sq_root` directly.

        Args:
            cubic_phase (CubicPhase): Cubic phase of which the square root of miller indices should be calculated.
            miller_indices (tuple[list[int], list[int], list[int]]): Miller indices of the cubic phase of which the square root should be calculated.

        Returns:
            list[int]: List of square roots of miller indices of cubic phase.
        """
        sq_root = [
            np.sqrt(
                miller_indices[0][i] ** 2
                + miller_indices[1][i] ** 2
                + miller_indices[2][i] ** 2
            )
            for i, _ in enumerate(miller_indices[0])
        ]
        cubic_phase.sqrt_miller = sq_root
        return sq_root

    @property
    def q_corr(self) -> list[float]:
        """Get calibrated scattering vectors."""
        return self._q_corr

    @property
    def d(self) -> list[float]:
        """Get lattice plane distances."""
        return self._d

    @property
    def d_ratio(self) -> list[float]:
        """Get lattice plane ratios."""
        return self._d_ratio
