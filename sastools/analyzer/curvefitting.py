"""Implementation of curve fitting for SAS experiments using Gaussian, 
Lorentzian, and Voigt models.
"""

import json
import random

from pathlib import Path
from typing import Tuple, Dict, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lmfit import models
from lmfit.model import save_modelresult, load_modelresult
from scipy import signal


class CurveFitting:
    """Tool for curve fitting"""

    def __init__(
        self,
        experimental_data: pd.DataFrame,
        file_name: str,
        path_plots: Path,
        path_fitting_data: Path,
    ) -> None:
        """Initialize parameters for the curve fitting class by passing
        experimental data whose curve is to be fitted, the file name,
        and the paths to where plots fitting data are to be saved.

        Args:
            experimental_data (pd.DataFrame): DataFrame of experimental data whose curve is to be fitted.
            file_name (str): Desired name for the files that are being saved.
            path_plots (Path): Path to where plots are to be saved.
            path_fitting_data (Path): Path to where fitting data is to be saved.
        """
        
        self.exp_data = experimental_data
        self.x = self.exp_data.iloc[:, 0].values.tolist()
        self.y = self.exp_data.iloc[:, 1].values.tolist()
        self.file_name = file_name
        self.path_plots = path_plots
        self.path_fitting_data = path_fitting_data

    def _pack_data_into_dict(self) -> Dict:
        # Stores the data in a dictionary
        data_dict = {"data": {"x": self.x, "y": self.y}}
        return data_dict

    def plot_raw_data(self) -> None:
        """Plot the data and save the plot"""
        exp_data_plot = sns.lineplot(
            x="scattering_vector", y="counts_per_area", data=self.exp_data
        )
        exp_data_fig = exp_data_plot.get_figure()
        exp_data_fig.savefig(
            self.path_plots / f"exp_data_plot_{self.file_name}.png",
            facecolor="white",
            transparent=False,
            dpi=600,
        )

    def find_peaks_cwt(
        self, peak_widths: Tuple = (20,), cutoff_amplitude: Optional[float] = None
    ) -> None:
        """Find peaks using the `find_peaks_cwt` method from signal.
        Prints number of found peaks. Figure with positions of found
        peaks is plotted and saved.

        Args:
            peak_widths (tuple, optional):  Expected peak widths for the algorithm to find. Defaults to (20,).
            cutoff_amplitude (float, optional): Cutoff below which peaks found are discarded. Defaults to None.
        """
        self.c = cutoff_amplitude
        self.w = peak_widths
        peak_indices = signal.find_peaks_cwt(self.y, self.w)
        x_val_peak = [self.x[peak_index] for peak_index in peak_indices]
        y_val_peak = [self.y[peak_index] for peak_index in peak_indices]
        self.peak_dict = {}
        for i in range(len(x_val_peak)):
            self.peak_dict[x_val_peak[i]] = y_val_peak[i]
        if self.c != None:
            self.peak_dict = {
                key: val
                for key, val in self.peak_dict.items()
                if val >= self.c
            }
        self.n_peaks = len(self.peak_dict)
        print("number of found peaks:", self.n_peaks)
        j = 1
        for key, value in self.peak_dict.items():
            print("peak number:", j, "x:", key, "y:", value)
            j = j + 1

    def plot_found_peak(self) -> None:
        """Plot peaks found and save the plot"""
        peak_fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        for i in self.peak_dict:
            ax.axvline(i, c="black", linestyle="dotted")
        peak_fig.savefig(
            self.path_plots / f"found_peaks_{self.file_name}.png",
            facecolor="white",
            transparent=False,
            dpi=600,
        )

    def set_specifications_manually(
        self, number_of_models: int, model_specifications: Dict
    ) -> None:
        """Manually sets the specifications for the individual model
        used for the fitting procedure. Stores the generated
        specifications in a json file.

        Args:
            number_of_models (int): Number of models to use for the fitting procedure
            model_specifications (dict): Fitting parameters for the models, each consisting of the initial values 'type', 'center',
            'height' and 'sigma' of the individual models as well as corresponding 'help' parameter which confines the position of
            the model center during the fitting procedure.
        """
        self.n_models = number_of_models
        self.models = model_specifications
        spec_dict = self._pack_data_into_dict()
        models_list = []
        for model in self.models:
            model_dict = {
                "type": model[0],
                "params": {
                    "center": model[1][0],
                    "height": model[1][1],
                    "sigma": model[1][2],
                },
                "help": {"center": {"min": model[2][0], "max": model[2][1]}},
            }
            models_list.append(model_dict)
        spec_dict.update({"models": models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open(
            self.path_fitting_data / f"models_dict_{self.file_name}.json", "w"
        ) as outfile:
            outfile.write(json_models_dict)

    def set_specifications_automatically(
        self, tolerance: float, model_type: str
    ) -> None:
        """Automatically sets the specifications for the individual
        model used for the fitting procedure. Stores the generated
        specifications in a json file.

        Args:
            tolerance (float): Tolerance within which the center positions of the models may deviate during the fitting procedure.
            model_type (str): Model type to be used for the fitting procedure.
        """
        self.model_type = model_type
        t = tolerance
        x_range = np.max(self.x) - np.min(self.x)
        spec_dict = self._pack_data_into_dict()
        models_list = []
        for x, y in self.peak_dict.items():
            model_dict = {
                "type": self.model_type,
                "params": {
                    "center": x,
                    "height": y,
                    "sigma": x_range / len(self.peak_dict) * np.min(self.w),
                },
                "help": {"center": {"min": (x - t), "max": (x + t)}},
            }
            models_list.append(model_dict)
        spec_dict.update({"models": models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open(
            self.path_fitting_data / f"models_dict_{self.file_name}.json", "w"
        ) as outfile:
            outfile.write(json_models_dict)

    def generate_model(self, speci: Dict) -> tuple:
        """Generates a composite model and corresponding parameters
        based on the provided specifications using the `model` class
        of the python library `lmfit`.

        Args:
            dict: Contains all the initial specification for the fitting procedure.

        Raises:
            NotImplemented: If a provided model type is not implemented in the algorithm.

        Returns:
            tuple: Generated compostite model and corresponding fitting parameters.
        """
        composite_model = None
        params = None
        x_min = np.min(speci["data"]["x"])
        x_max = np.max(speci["data"]["x"])
        x_range = x_max - x_min
        y_max = np.max(speci["data"]["y"])
        for i, basis_func in enumerate(speci["models"]):
            prefix = f"model{i}_"
            model = getattr(models, basis_func["type"])(prefix=prefix)
            if basis_func["type"] in [
                "GaussianModel",
                "LorentzianModel",
                "VoigtModel",
            ]:  # for VoigtModel gamma is constrained to sigma
                model.set_param_hint("sigma", min=1e-6, max=x_range)
                model.set_param_hint("center", min=x_min, max=x_max)
                model.set_param_hint("height", min=1e-6, max=1.1 * y_max)
                model.set_param_hint("amplitude", min=1e-6)
                default_params = {
                    prefix + "center": x_min + x_range * random.random(),
                    prefix + "height": y_max * random.random(),
                    prefix + "sigma": x_range * random.random(),
                }
            else:
                raise NotImplemented(
                    f'model {basis_func["type"]} not implemented yet'
                )
            if "help" in basis_func:  # allow override of settings in parameter
                for param, options in basis_func["help"].items():
                    model.set_param_hint(param, **options)
            model_params = model.make_params(
                **default_params, **basis_func.get("params", {})
            )
            if params is None:
                params = model_params
            else:
                params.update(model_params)
            if composite_model is None:
                composite_model = model
            else:
                composite_model = composite_model + model
        return composite_model, params

    def fit(self) -> None:
        """Executes the fitting algorithm starting from the generated
        model and the corresponding parameters. Saves the output as
        `model_result`, which is as a class of `lmfit`.
        """
        with open(
            self.path_fitting_data / f"models_dict_{self.file_name}.json", "r"
        ) as outfile:
            speci = json.load(outfile)
        model, params = self.generate_model(speci)
        model_result = model.fit(
            speci["data"]["y"], params, x=speci["data"]["x"]
        )
        save_modelresult(
            model_result,
            self.path_fitting_data / f"model_result_{self.file_name}.sav",
        )

    def save_list_of_peak_centers(self) -> None:
        """Stores the determined peak centers in a text file."""
        model_result = load_modelresult(
            self.path_fitting_data / f"model_result_{self.file_name}.sav"
        )
        list_peak_center = []
        for i in range(self.n_peaks):
            list_peak_center.append(
                model_result.best_values[f"model{i}_center"]
            )
        with open(
            self.path_fitting_data / f"list_xc_{self.file_name}.txt", "w"
        ) as f:
            for line in list_peak_center:
                f.write(f"{line}\n")

    def plot_fitting_result(self) -> None:
        """Load the `model_result` and creating a plot using the `plot`
        method of the `model_result` class, which shows the fit along
        with the corresponding residual values. Prints the positions of
        the individual fitted models along with their heights.
        """
        model_result = load_modelresult(
            self.path_fitting_data / f"model_result_{self.file_name}.sav"
        )
        # print(model_result.fit_report())
        fig = model_result.plot(data_kws={"markersize": 0.5})
        fig.axes[0].set_title("")
        fig.savefig(
            self.path_plots / f"model_result_{self.file_name}.png",
            facecolor="white",
            dpi=600,
        )
        for key, value in model_result.best_values.items():
            print(key, ":", value)
